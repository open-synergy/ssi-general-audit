# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestGeneralAuditWSControlRisk(TransactionCase):
    """Covers the "Medium" option added to the existing ``risk`` field on
    ``general_audit_ws_eabdaad`` and ``general_audit_ws_ba9b2f0`` in this
    module (Phase 2 of the Account Level ROMM configuration work) -
    upgrading it from Low/High to Low/Medium/High so it can double as the
    Control Risk input for the Account Level ROMM Matrix A ("Audit Risk").
    No new field is introduced; the existing ``risk`` field is reused as-is.
    """

    def setUp(self):
        super().setUp()
        env = self.env
        admin = env.ref("base.user_admin")
        self.admin = admin

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - Control Risk", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - Control Risk"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-CONTROL-RISK-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - Control Risk", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - Control Risk", "code": "/"})
        )
        self.audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - Control Risk",
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
        self.audit.with_user(admin).action_open()

        self.cycle = env.ref("ssi_general_audit.client_business_process_2_ef83aa88")
        account_group = (
            env["client_account_group"]
            .with_user(admin)
            .create({"name": "Test Account Group - Control Risk", "code": "/"})
        )
        self.account_type = (
            env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type - Control Risk",
                    "code": "/",
                    "group_id": account_group.id,
                    "python_code": "result = 0.0",
                }
            )
        )

        eabdaad_ws_type = env.ref(
            "ssi_general_audit_worksheet_control_risk.worksheet_type_eabdaad"
        )
        self.eabdaad_worksheet = (
            env["general_audit_ws_eabdaad"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": self.audit.id,
                    "type_id": eabdaad_ws_type.id,
                    "business_cycle_id": self.cycle.id,
                }
            )
        )

        ba9b2f0_ws_type = env.ref(
            "ssi_general_audit_worksheet_control_risk.worksheet_type_ba9b2f0"
        )
        self.ba9b2f0_worksheet = (
            env["general_audit_ws_ba9b2f0"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": self.audit.id,
                    "type_id": ba9b2f0_ws_type.id,
                    "account_type_id": self.account_type.id,
                }
            )
        )

    def test_risk_defaults_blank_on_eabdaad(self):
        self.assertFalse(self.eabdaad_worksheet.risk)

    def test_risk_medium_writable_on_eabdaad(self):
        # "medium" is the option added by this module on top of the
        # original Low/High selection.
        self.eabdaad_worksheet.write({"risk": "medium"})
        self.assertEqual(self.eabdaad_worksheet.risk, "medium")

    def test_risk_low_high_still_writable_on_eabdaad(self):
        self.eabdaad_worksheet.write({"risk": "low"})
        self.assertEqual(self.eabdaad_worksheet.risk, "low")
        self.eabdaad_worksheet.write({"risk": "high"})
        self.assertEqual(self.eabdaad_worksheet.risk, "high")

    def test_risk_defaults_blank_on_ba9b2f0(self):
        self.assertFalse(self.ba9b2f0_worksheet.risk)

    def test_risk_medium_writable_on_ba9b2f0(self):
        self.ba9b2f0_worksheet.write({"risk": "medium"})
        self.assertEqual(self.ba9b2f0_worksheet.risk, "medium")
