# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWsB4f7d9c(YamlTransactionCase):
    def test_ws_b4f7d9c(self):
        self.run_yaml_scenario("test_data_ws_b4f7d9c.yaml")

    def _create_worksheet_fixture(self):
        """Build the minimal general_audit + worksheet fixture needed by the
        Python-only tests below, entirely through the ORM (no demo data).
        """
        env = self.env
        admin = env.ref("base.user_admin")

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - B4F7D9C Python", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - B4F7D9C Python"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-B4F7D9C-PYTHON-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - B4F7D9C Python", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - B4F7D9C Python", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - B4F7D9C Python",
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
            .create({"name": "Test Account Group - B4F7D9C Python", "code": "/"})
        )
        account_type = (
            env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type - B4F7D9C Python",
                    "code": "/",
                    "group_id": account_group.id,
                    # No general_audit.standard_detail is created against this
                    # account type in this fixture, so the crashing default
                    # ("result = document.balance") is never evaluated here.
                    # Set explicitly anyway per the repo-wide convention of
                    # never leaving client_account_type.python_code at its
                    # default when general_audit.standard_detail could ever
                    # end up depending on it.
                    "python_code": "result = 0.0",
                }
            )
        )

        ws_type = env.ref(
            "ssi_general_audit_worksheet_audit_procedure_vouching.worksheet_type_b4f7d9c"
        )
        ws_type_e51bb1c = env.ref(
            "ssi_general_audit_worksheet_lead_schedule.worksheet_type_e51bb1c"
        )
        ws_e51bb1c = (
            env["general_audit_ws_e51bb1c"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type_e51bb1c.id})
        )
        worksheet = (
            env["general_audit_ws_b4f7d9c"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type.id})
        )
        return admin, worksheet, account_type, ws_e51bb1c

    def test_onchange_general_audit_id_clears_account_type(self):
        """``onchange_account_type_id`` is declared
        ``@api.onchange("general_audit_id")``, but ``account_type_id`` is only
        editable (``readonly=False``) while ``state == "open"``, and
        ``general_audit_id`` is only editable while ``state == "draft"`` -- the
        two conditions never overlap on the same record. Driving this through
        ``Form`` (the documented way to test onchange, see ``action: form`` in
        the odoo-yaml-test YAML DSL) is therefore impossible: setting
        ``account_type_id`` on a draft-state Form raises because the field is
        readonly at that state, and even if it could be set, ``Form.save()``
        explicitly does not persist readonly fields, so the onchange's
        in-memory clearing would be silently discarded on save whenever
        ``general_audit_id`` is actually editable. This exact limitation was
        already found and documented for the sibling ``general_audit_ws_c6c86fd``
        worksheet in ``ssi_general_audit_worksheet_audit_procedure_recompute``
        -- it is a pre-existing pattern of the shared worksheet mixin's
        ``states`` design, not specific to this module. The onchange method is
        called directly here instead, to verify its own body does what it
        claims.
        """
        _admin, worksheet, account_type, _ws_e51bb1c = self._create_worksheet_fixture()

        worksheet.sudo().write({"account_type_id": account_type.id})
        self.assertTrue(worksheet.account_type_id)

        worksheet.onchange_account_type_id()

        self.assertFalse(worksheet.account_type_id)

    def test_onchange_general_audit_id_clears_ws_e51bb1c(self):
        """See ``test_onchange_general_audit_id_clears_account_type`` for why
        this onchange is verified by calling the method directly instead of
        through ``Form``.
        """
        _admin, worksheet, _account_type, ws_e51bb1c = self._create_worksheet_fixture()

        worksheet.sudo().write({"ws_e51bb1c_id": ws_e51bb1c.id})
        self.assertTrue(worksheet.ws_e51bb1c_id)

        worksheet.onchange_ws_e51bb1c_id()

        self.assertFalse(worksheet.ws_e51bb1c_id)

    def test_action_open_data_comparisons_returns_window_action(self):
        """``action_open_data_comparisons`` returns a client-side
        ``ir.actions.act_window`` dict. ``odoo-yaml-test``'s ``action: call``
        step (see ``yaml-actions.md`` section 6.3) discards the method's
        return value -- it only supports asserting on the *target record's*
        fields afterwards, not on the returned dict -- so there is no way to
        express "assert the returned action dict" purely in YAML. The method
        is therefore called directly here.
        """
        _admin, worksheet, _account_type, _ws_e51bb1c = self._create_worksheet_fixture()

        action = worksheet.action_open_data_comparisons()

        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(
            action["res_model"], "general_audit_ws_b4f7d9c.data_comparison"
        )
        self.assertEqual(action["domain"], [("worksheet_id", "=", worksheet.id)])
        self.assertEqual(action["context"]["default_worksheet_id"], worksheet.id)

    def test_action_open_vouching_lines_returns_window_action(self):
        """See ``test_action_open_data_comparisons_returns_window_action`` for
        why this action method is verified directly instead of through YAML.
        """
        _admin, worksheet, _account_type, _ws_e51bb1c = self._create_worksheet_fixture()

        action = worksheet.action_open_vouching_lines()

        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "general_audit_ws_b4f7d9c.vouching")
        self.assertEqual(action["domain"], [("worksheet_id", "=", worksheet.id)])
        self.assertEqual(action["context"]["default_worksheet_id"], worksheet.id)
