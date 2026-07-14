# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWsAa899baf(YamlTransactionCase):
    def test_general_audit_ws_aa899baf(self):
        self.run_yaml_scenario("test_data_ws_aa899baf.yaml")

    def test_action_open_variables_and_relations(self):
        """``action_open_variables``/``action_open_relations`` only matter for
        the ``ir.actions.act_window`` dict they return (scoped ``domain``/
        ``context``) -- the odoo-yaml-test DSL's ``action: call`` invokes the
        method but discards its return value and only supports asserting on
        the *target record* afterward (see ``_action_call`` in
        ``odoo_yaml_test/case.py``), so the returned dict itself cannot be
        expressed as a YAML scenario. Verified directly here instead, with
        all fixtures still built through the ORM (no demo data).
        """
        env = self.env
        admin = env.ref("base.user_admin")

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - AA899BAF Action", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - AA899BAF Action"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-AA899BAF-ACTION-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - AA899BAF Action", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - AA899BAF Action", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
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
        )
        audit.with_user(admin).action_open()

        ws_type = env.ref(
            "ssi_general_audit_worksheet_audit_procedure_analytic.worksheet_type_aa899baf"
        )
        worksheet = (
            env["general_audit_ws_aa899baf"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type.id})
        )

        variables_action = worksheet.with_user(admin).action_open_variables()
        self.assertEqual(variables_action["type"], "ir.actions.act_window")
        self.assertIn(("worksheet_id", "=", worksheet.id), variables_action["domain"])
        self.assertEqual(
            variables_action["context"]["default_worksheet_id"], worksheet.id
        )

        relations_action = worksheet.with_user(admin).action_open_relations()
        self.assertEqual(relations_action["type"], "ir.actions.act_window")
        self.assertIn(("worksheet_id", "=", worksheet.id), relations_action["domain"])
        self.assertEqual(
            relations_action["context"]["default_worksheet_id"], worksheet.id
        )
