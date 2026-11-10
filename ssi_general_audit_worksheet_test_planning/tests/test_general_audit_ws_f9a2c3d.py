# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from unittest import mock

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged
from odoo.tests.common import Form


@tagged("post_install", "-at_install")
class TestGeneralAuditWSf9a2c3d(YamlTransactionCase):
    """Tests of the Test of Detail Planning worksheet (f9a2c3d)."""

    def test_general_audit_ws_f9a2c3d(self):
        """Run the YAML scenarios of the worksheet.

        The scenarios cover the Detail button, the nine columns of a line,
        the seeded master data and the document workflow.
        """
        self.run_yaml_scenario("test_data_general_audit_ws_f9a2c3d.yaml")

    def _create_worksheet_fixture(self):
        """Create an audit with one standard account and a worksheet.

        The worksheet is left in draft and has no line yet.

        :return: the worksheet created
        """
        env = self.env
        admin = env.ref("base.user_admin")
        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )
        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - F9A2C3D Python", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - F9A2C3D Python"})
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": env.ref(
                    "ssi_partner_identification_cpa_license"
                    ".partner_identification_accountant_cpa_license"
                ).id,
                "name": "CPA-F9A2C3D-PYTHON-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - F9A2C3D Python", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - F9A2C3D Python", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - F9A2C3D Python",
                    "partner_id": client.id,
                    "accountant_id": accountant.id,
                    "account_type_set_id": account_type_set.id,
                    "financial_accounting_standard_id": standard.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                    "need_interim": False,
                    "need_previous": False,
                    "num_of_consecutive_audit_firm": 1,
                    "num_of_consecutive_audit_accountant": 1,
                }
            )
        )
        audit.with_user(admin).action_open()
        account_group = (
            env["client_account_group"]
            .with_user(admin)
            .create({"name": "Test Account Group - F9A2C3D Python", "code": "/"})
        )
        account_type = (
            env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type - F9A2C3D Python",
                    "code": "/",
                    "group_id": account_group.id,
                    "normal_balance": "dr",
                    # The default python_code reads a field that
                    # general_audit.standard_detail does not have.
                    "python_code": "result = 0.0",
                }
            )
        )
        env["general_audit.standard_detail"].with_user(admin).create(
            {"general_audit_id": audit.id, "type_id": account_type.id}
        )
        return (
            env["general_audit_ws_f9a2c3d"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": env.ref(
                        "ssi_general_audit_worksheet_test_planning"
                        ".worksheet_type_f9a2c3d"
                    ).id,
                }
            )
        )

    def test_planning_columns_editable_only_when_open(self):
        """Columns 7 to 9 can be edited in the form only in state open.

        The readonly rule belongs to the view of the worksheet, which the
        YAML runner cannot select (``L-20``, ``P12``), so the form is
        driven with ``Form``.
        """
        admin = self.env.ref("base.user_admin")
        worksheet = self._create_worksheet_fixture()
        worksheet.with_user(admin).action_open()
        worksheet.with_user(admin).action_load_detail()
        timing = self.env["general_audit_ws_f9a2c3d_timing"].search([], limit=1)
        techniques = self.env["general_audit_ws_f9a2c3d_technique"].search([], limit=3)
        self.assertEqual(len(worksheet.detail_ids), 1)

        with Form(worksheet.with_user(admin)) as form:
            with form.detail_ids.edit(0) as line:
                line.timing_id = timing
                for technique in techniques:
                    line.technique_ids.add(technique)
        self.assertEqual(worksheet.detail_ids.timing_id, timing)
        self.assertEqual(worksheet.detail_ids.technique_ids, techniques)

        worksheet.with_user(admin).action_cancel()
        worksheet.invalidate_cache()
        self.assertNotEqual(worksheet.state, "open")
        with self.assertRaises(AssertionError):
            with Form(worksheet.with_user(admin)) as form:
                with form.detail_ids.edit(0) as line:
                    line.timing_id = timing

    def test_detail_removes_only_obsolete_lines(self):
        """Pressing Detail removes only the line of a dropped account.

        The criteria of the loader are patched to leave one standard
        account out, which cannot be done from YAML (``P6``, ``L-15``).
        The line of the account that stays keeps its id and its Timing.
        """
        admin = self.env.ref("base.user_admin")
        worksheet = self._create_worksheet_fixture()
        audit = worksheet.general_audit_id
        first = audit.standard_detail_ids[:1]
        account_type = (
            self.env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type 2 - F9A2C3D Python",
                    "code": "/",
                    "group_id": first.type_id.group_id.id,
                    "normal_balance": "dr",
                    "python_code": "result = 0.0",
                }
            )
        )
        second = (
            self.env["general_audit.standard_detail"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": account_type.id})
        )
        worksheet.with_user(admin).action_open()
        worksheet.with_user(admin).action_load_detail()
        self.assertEqual(len(worksheet.detail_ids), 2)
        kept_line = worksheet.detail_ids.filtered(
            lambda line: line.standard_detail_id == first
        )
        timing = self.env["general_audit_ws_f9a2c3d_timing"].search([], limit=1)
        kept_line.timing_id = timing

        criteria = [
            ("general_audit_id", "=", audit.id),
            ("id", "!=", second.id),
        ]
        with mock.patch.object(
            type(worksheet),
            "_get_standard_detail_criteria",
            return_value=criteria,
        ):
            worksheet.with_user(admin).action_load_detail()
        self.assertEqual(worksheet.detail_ids, kept_line)
        self.assertEqual(kept_line.timing_id, timing)
