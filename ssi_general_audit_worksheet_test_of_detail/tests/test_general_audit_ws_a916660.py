# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSa916660(YamlTransactionCase):
    def test_general_audit_ws_a916660(self):
        self.run_yaml_scenario("test_data_general_audit_ws_a916660.yaml")

    def _create_worksheet_fixture(self):
        """Build the minimal general_audit + GL + Subledger + worksheet
        fixture needed by the Python-only onchange tests below, entirely
        through the ORM (no demo data).
        """
        env = self.env
        admin = env.ref("base.user_admin")

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - A916660 Python", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - A916660 Python"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-A916660-PYTHON-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - A916660 Python", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - A916660 Python", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - A916660 Python",
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
            "ssi_general_audit_worksheet_test_of_detail.worksheet_type_a916660"
        )
        ws_type_d209914 = env.ref(
            "ssi_general_audit_worksheet_client_package.worksheet_type_d209914"
        )
        ws_type_b5e3d9f = env.ref(
            "ssi_general_audit_worksheet_client_package.worksheet_type_b5e3d9f"
        )
        gl = (
            env["general_audit_ws_d209914"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type_d209914.id})
        )
        subledger = (
            env["general_audit_ws_b5e3d9f"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type_b5e3d9f.id})
        )
        worksheet = (
            env["general_audit_ws_a916660"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type.id})
        )
        return admin, worksheet, gl, subledger

    def test_onchange_data_mode_clears_general_ledger_id(self):
        """``onchange_general_ledger_id`` is declared
        ``@api.onchange("data_mode")``. Unlike the sibling
        ``general_audit_ws_c6c86fd`` / ``general_audit_ws_b4f7d9c`` cases,
        ``data_mode`` and ``general_ledger_id`` are *not* mutually exclusive
        by state here -- both share the exact same
        ``states={"open": [("readonly", False)]}`` definition. Driving this
        through ``action: form`` in YAML was tried first, but CI proved it
        fails unconditionally on this model's form view with
        ``AssertionError: __len__ was not found in the view`` regardless of
        which field is touched -- caused by the mixin-level
        ``allowed_general_ledger_ids`` / ``allowed_subledger_ids`` Many2many
        fields being declared ``invisible="1"`` with no sub-view/tree arch,
        which the ``Form`` test helper cannot build editable metadata for.
        That is a pre-existing limitation of the shared worksheet mixin's
        view, not something this test suite is allowed to fix (production
        code is out of scope). The onchange method is called directly here
        instead, to verify its own body does what it claims.
        """
        _admin, worksheet, gl, _subledger = self._create_worksheet_fixture()

        worksheet.sudo().write({"data_mode": "gl", "general_ledger_id": gl.id})
        self.assertTrue(worksheet.general_ledger_id)

        worksheet.onchange_general_ledger_id()

        self.assertFalse(worksheet.general_ledger_id)

    def test_onchange_data_mode_clears_subledger_id(self):
        """See ``test_onchange_data_mode_clears_general_ledger_id`` for why
        this onchange is verified by calling the method directly instead of
        through ``Form``.
        """
        _admin, worksheet, _gl, subledger = self._create_worksheet_fixture()

        worksheet.sudo().write({"data_mode": "subledger", "subledger_id": subledger.id})
        self.assertTrue(worksheet.subledger_id)

        worksheet.onchange_subledger_id()

        self.assertFalse(worksheet.subledger_id)
