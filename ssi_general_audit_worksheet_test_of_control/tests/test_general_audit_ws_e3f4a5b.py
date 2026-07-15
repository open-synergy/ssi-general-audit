# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSe3f4a5b(YamlTransactionCase):
    def test_general_audit_ws_e3f4a5b(self):
        self.run_yaml_scenario("test_data_general_audit_ws_e3f4a5b.yaml")

    def _create_worksheet_fixture(self):
        """Build the minimal general_audit + worksheet fixture needed by the
        Python-only test below, entirely through the ORM (no demo data).
        """
        env = self.env
        admin = env.ref("base.user_admin")

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - E3F4A5B Python", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - E3F4A5B Python"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-E3F4A5B-PYTHON-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - E3F4A5B Python", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - E3F4A5B Python", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - E3F4A5B Python",
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
            .create({"name": "Test Account Group - E3F4A5B Python", "code": "/"})
        )
        account_type = (
            env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type - E3F4A5B Python",
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
            "ssi_general_audit_worksheet_test_of_control.worksheet_type_e3f4a5b"
        )
        worksheet = (
            env["general_audit_ws_e3f4a5b"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type.id})
        )
        return admin, worksheet, account_type

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
        already found and documented for the sibling ``general_audit_ws_b4f7d9c``
        worksheet in ``ssi_general_audit_worksheet_audit_procedure_vouching``
        -- it is a pre-existing pattern of the shared worksheet mixin's
        ``states`` design, not specific to this module. The onchange method is
        called directly here instead, to verify its own body does what it
        claims.
        """
        _admin, worksheet, account_type = self._create_worksheet_fixture()

        worksheet.sudo().write({"account_type_id": account_type.id})
        self.assertTrue(worksheet.account_type_id)

        worksheet.onchange_account_type_id()

        self.assertFalse(worksheet.account_type_id)
