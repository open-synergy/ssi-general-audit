# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestGeneralAuditWSd66d87aControlRisk(TransactionCase):
    """Covers ``general_audit_ws_d66d87a.detail.control_risk`` (computed
    lookup, ba9b2f0 takes precedence over eabdaad) and ``significant_risk``
    (related mirror of ``standard_detail_id.significant_risk``) - both
    displayed next to ``inherent_risk`` per the user's request, ahead of
    wiring the full ROMM formula (still manual ``romm`` at this point).
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
            .create({"name": "Test Audit Client - d66d87a CR", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - d66d87a CR"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-D66D87A-CR-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - d66d87a CR", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - d66d87a CR", "code": "/"})
        )
        self.audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - d66d87a CR",
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
            .create({"name": "Test Account Group - d66d87a CR", "code": "/"})
        )
        self.account_type = (
            env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type - d66d87a CR",
                    "code": "/",
                    "group_id": account_group.id,
                    "python_code": "result = 0.0",
                }
            )
        )
        self.standard_detail = (
            env["general_audit.standard_detail"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": self.audit.id,
                    "type_id": self.account_type.id,
                }
            )
        )

        d66d87a_ws_type = env.ref(
            "ssi_general_audit_worksheet_romm.worksheet_type_d66d87a"
        )
        self.d66d87a_worksheet = (
            env["general_audit_ws_d66d87a"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": self.audit.id,
                    "type_id": d66d87a_ws_type.id,
                }
            )
        )
        self.detail = (
            env["general_audit_ws_d66d87a.detail"]
            .with_user(admin)
            .create(
                {
                    "worksheet_id": self.d66d87a_worksheet.id,
                    "standard_detail_id": self.standard_detail.id,
                }
            )
        )

    def _create_eabdaad(self, risk):
        eabdaad_ws_type = self.env.ref(
            "ssi_general_audit_worksheet_control_risk.worksheet_type_eabdaad"
        )
        worksheet = (
            self.env["general_audit_ws_eabdaad"]
            .with_user(self.admin)
            .create(
                {
                    "general_audit_id": self.audit.id,
                    "type_id": eabdaad_ws_type.id,
                    "business_cycle_id": self.cycle.id,
                    "risk": risk,
                }
            )
        )
        key_internal_control = self.env.ref(
            "ssi_general_audit_worksheet_control_risk"
            ".general_audit_key_internal_control_86_8b14c4f6"
        )
        self.env["general_audit_ws_eabdaad.detail"].with_user(self.admin).create(
            {
                "worksheet_id": worksheet.id,
                "key_internal_control_id": key_internal_control.id,
                "name": "Test control activity",
                "frequency": "Monthly",
                "related_account_type_ids": [(6, 0, [self.account_type.id])],
                "rely_on_control": "yes",
            }
        )
        return worksheet

    def _create_ba9b2f0(self, risk):
        ba9b2f0_ws_type = self.env.ref(
            "ssi_general_audit_worksheet_control_risk.worksheet_type_ba9b2f0"
        )
        return (
            self.env["general_audit_ws_ba9b2f0"]
            .with_user(self.admin)
            .create(
                {
                    "general_audit_id": self.audit.id,
                    "type_id": ba9b2f0_ws_type.id,
                    "account_type_id": self.account_type.id,
                    "risk": risk,
                }
            )
        )

    def test_control_risk_blank_when_no_source(self):
        self.assertFalse(self.detail.control_risk)

    def test_control_risk_falls_back_to_eabdaad(self):
        self._create_eabdaad("high")
        self.d66d87a_worksheet.action_load_detail()
        detail = self.d66d87a_worksheet.detail_ids.filtered(
            lambda d: d.standard_detail_id == self.standard_detail
        )
        self.assertEqual(detail.control_risk, "high")

    def test_control_risk_prefers_ba9b2f0_over_eabdaad(self):
        self._create_eabdaad("high")
        self._create_ba9b2f0("low")
        self.d66d87a_worksheet.action_load_detail()
        detail = self.d66d87a_worksheet.detail_ids.filtered(
            lambda d: d.standard_detail_id == self.standard_detail
        )
        self.assertEqual(detail.control_risk, "low")

    def test_control_risk_resyncs_on_load_detail(self):
        eabdaad = self._create_eabdaad("high")
        self.d66d87a_worksheet.action_load_detail()
        detail = self.d66d87a_worksheet.detail_ids.filtered(
            lambda d: d.standard_detail_id == self.standard_detail
        )
        self.assertEqual(detail.control_risk, "high")

        eabdaad.write({"risk": "medium"})
        self.d66d87a_worksheet.action_load_detail()
        detail = self.d66d87a_worksheet.detail_ids.filtered(
            lambda d: d.standard_detail_id == self.standard_detail
        )
        self.assertEqual(detail.control_risk, "medium")

    def test_significant_risk_mirrors_standard_detail(self):
        self.assertFalse(self.detail.significant_risk)
        self.standard_detail.write({"significant_risk": True})
        self.assertTrue(self.detail.significant_risk)
