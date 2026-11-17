# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from unittest.mock import patch

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWorksheetParentSync(YamlTransactionCase):
    """Test how a worksheet keeps its parent worksheet in sync."""

    def setUp(self):
        """Create an open audit and a worksheet that is linked to it.

        :return: ``None``
        """
        super().setUp()
        env = self.env
        env["ir.config_parameter"].set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )
        client = env["res.partner"].create(
            {"name": "Test Audit Client - psync py", "is_company": True}
        )
        accountant = env["res.partner"].create(
            {"name": "Test Audit Accountant - psync py"}
        )
        env["res.partner.id_number"].create(
            {
                "partner_id": accountant.id,
                "category_id": env.ref(
                    "ssi_partner_identification_cpa_license."
                    "partner_identification_accountant_cpa_license"
                ).id,
                "name": "CPA-PSYNC-PY-0001",
            }
        )
        audit = env["general_audit"].create(
            {
                "title": "Test General Audit - psync py",
                "partner_id": client.id,
                "accountant_id": accountant.id,
                "account_type_set_id": env["client_account_type_set"]
                .create({"name": "Test Account Type Set - psync py", "code": "/"})
                .id,
                "financial_accounting_standard_id": env[
                    "accountant.financial_accounting_standard"
                ]
                .create({"name": "Test Standard - psync py", "code": "/"})
                .id,
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
                "need_interim": False,
                "need_previous": False,
                "num_of_consecutive_audit_firm": 1,
                "num_of_consecutive_audit_accountant": 1,
            }
        )
        audit.action_open()
        audit.invalidate_cache()
        self.worksheet = env["general_audit_ws_a753ab9"].create(
            {
                "general_audit_id": audit.id,
                "type_id": env.ref(
                    "ssi_general_audit_worksheet_planning_memorandum."
                    "worksheet_type_a753ab9"
                ).id,
                "reviewer_id": env.ref("base.user_admin").id,
            }
        )

    def _count_parent_writes(self, values):
        """Write on the worksheet and count the writes on its parent.

        :param dict values: values written on the worksheet
        :return: tuple of the write result and the number of parent writes
        :rtype: tuple
        """
        parent_model = type(self.env["general_audit_worksheet"])
        original = parent_model.write
        calls = []

        def _spy(records, vals):
            """Record the write on the parent worksheet, then run it.

            :param records: parent worksheet records being written
            :param dict vals: values of the write
            :return: result of the original ``write``
            """
            calls.append((records.ids, dict(vals)))
            return original(records, vals)

        with patch.object(parent_model, "write", _spy):
            result = self.worksheet.write(values)
        parent_id = self.worksheet.worksheet_id.id
        return result, [c for c in calls if parent_id in c[0]]

    def test_write_unshared_field_skips_parent(self):
        """A write without a changed shared value does not write the parent.

        Pure Python test: counting the writes on the parent model needs a
        mock. Trigger P6, limitation L-15 (no mock or stub in the YAML
        DSL).

        :return: ``None``
        """
        _result, parent_calls = self._count_parent_writes(
            {"checklist_ids": [(5, 0, 0)]}
        )
        self.assertEqual(parent_calls, [])

    def test_write_returns_true(self):
        """The worksheet ``write`` returns the result of the parent class.

        Pure Python test: the YAML ``write`` action discards the return
        value. Trigger P1, limitation L-01.

        :return: ``None``
        """
        result, _parent_calls = self._count_parent_writes(
            {"checklist_ids": [(5, 0, 0)]}
        )
        self.assertIs(result, True)

    def test_write_heals_parent_drift(self):
        """Any write restores the parent to the shared values of the child.

        Pure Python test: the parent record is changed behind the child,
        which the YAML DSL cannot target. Trigger P6, limitation L-15
        (no mock or stub in the YAML DSL, no alias for the parent).

        :return: ``None``
        """
        parent = self.worksheet.worksheet_id
        parent.write({"reviewer_id": False})
        self.assertFalse(parent.reviewer_id)
        _result, parent_calls = self._count_parent_writes(
            {"checklist_ids": [(5, 0, 0)]}
        )
        self.assertEqual(len(parent_calls), 1)
        self.assertEqual(
            parent_calls[0][1], {"reviewer_id": self.env.ref("base.user_admin").id}
        )
        self.assertEqual(parent.reviewer_id, self.env.ref("base.user_admin"))

    def test_parent_sync_scenario(self):
        """Run the scenario of the shared fields of the parent worksheet.

        :return: ``None``
        """
        self.run_yaml_scenario("test_data_worksheet_parent_sync.yaml")
