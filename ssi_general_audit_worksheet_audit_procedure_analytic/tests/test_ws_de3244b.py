# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWsDe3244b(YamlTransactionCase):
    def test_general_audit_ws_de3244b(self):
        self.run_yaml_scenario("test_data_ws_de3244b.yaml")

    def test_action_open_variables_and_comparatives(self):
        """Check the window actions returned by the open-action methods.

        Pure Python test, trigger ``P1`` (return value of a method), based
        on limitation ``L-01``: ``action: call`` discards the dict returned
        by ``action_open_variables``/``action_open_comparatives``, so the
        scoped ``domain``/``context`` cannot be asserted in YAML.
        """
        env = self.env
        admin = env.ref("base.user_admin")

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - DE3244B Action", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - DE3244B Action"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-DE3244B-ACTION-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - DE3244B Action", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - DE3244B Action", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - DE3244B Action",
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
            "ssi_general_audit_worksheet_audit_procedure_analytic.worksheet_type_de3244b"
        )
        worksheet = (
            env["general_audit_ws_de3244b"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type.id})
        )

        variables_action = worksheet.with_user(admin).action_open_variables()
        self.assertEqual(variables_action["type"], "ir.actions.act_window")
        self.assertIn(("worksheet_id", "=", worksheet.id), variables_action["domain"])
        self.assertEqual(
            variables_action["context"]["default_worksheet_id"], worksheet.id
        )

        comparatives_action = worksheet.with_user(admin).action_open_comparatives()
        self.assertEqual(comparatives_action["type"], "ir.actions.act_window")
        self.assertIn(
            ("worksheet_id", "=", worksheet.id), comparatives_action["domain"]
        )
        self.assertEqual(
            comparatives_action["context"]["default_worksheet_id"], worksheet.id
        )
