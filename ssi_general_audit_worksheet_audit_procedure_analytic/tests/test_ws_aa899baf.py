# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWsAa899baf(YamlTransactionCase):
    def test_general_audit_ws_aa899baf(self):
        self.run_yaml_scenario("test_data_ws_aa899baf.yaml")

    def _create_worksheet(self):
        """Minimal ``general_audit`` + worksheet fixture, built directly via
        the ORM -- functionally equivalent to ``action: create`` in YAML (no
        demo data involved).

        Only used by the two tests below, which assert on the *return
        value* of ``action_open_variables`` / ``action_open_relations`` (a
        plain ``ir.actions.act_window`` dict). ``odoo-yaml-test``'s
        ``action: call`` does not capture a method's return value -- its
        ``asserts`` run against the *target record* afterwards, not against
        whatever the method returned -- so there is no way to express this
        assertion in YAML. This is exactly the "genuinely cannot be
        declared in YAML" escape hatch documented for this framework.
        """
        self.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )
        client = self.env["res.partner"].create(
            {"name": "Test AA899BAF Action Client", "is_company": True}
        )
        accountant = self.env["res.partner"].create(
            {"name": "Test AA899BAF Action Accountant"}
        )
        account_type_set = self.env["client_account_type_set"].create(
            {"name": "Test AA899BAF Action Type Set", "code": "/"}
        )
        standard = self.env["accountant.financial_accounting_standard"].create(
            {"name": "Test AA899BAF Action Standard", "code": "/"}
        )
        audit = self.env["general_audit"].create(
            {
                "title": "Test General Audit - AA899BAF Action",
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
        ws_type = self.env.ref(
            "ssi_general_audit_worksheet_audit_procedure_analytic"
            ".worksheet_type_aa899baf"
        )
        return self.env["general_audit_ws_aa899baf"].create(
            {"general_audit_id": audit.id, "type_id": ws_type.id}
        )

    def test_action_open_variables_returns_act_window(self):
        worksheet = self._create_worksheet()
        action = worksheet.action_open_variables()
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertIn(("worksheet_id", "=", worksheet.id), action["domain"])
        self.assertEqual(action["context"].get("default_worksheet_id"), worksheet.id)

    def test_action_open_relations_returns_act_window(self):
        worksheet = self._create_worksheet()
        action = worksheet.action_open_relations()
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertIn(("worksheet_id", "=", worksheet.id), action["domain"])
        self.assertEqual(action["context"].get("default_worksheet_id"), worksheet.id)
