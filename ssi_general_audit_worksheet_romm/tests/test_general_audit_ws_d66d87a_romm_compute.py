# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestGeneralAuditWSd66d87aRommCompute(TransactionCase):
    """Covers the Fase 3b compute chain on
    ``general_audit_ws_d66d87a.detail``: ``romm_risk_initial`` and ``romm``
    (ROMM Risk Further) are now computed (``general_audit_romm_scoring_config``),
    replacing the old manual ``related=...,readonly=False`` ``romm`` field.

    Most tests vary Inherent Risk / Control Risk / Significant Risk (all
    directly settable) and leave Fraud Risk at its "medium" default
    (``fraud_impacted=False``); the Boolean -> "high"/"medium" mapping for
    Fraud Risk is otherwise a one-line ternary already exercised indirectly
    through ``get_romm_risk_further`` in
    ``test_general_audit_romm_scoring_config.py``.
    ``test_fraud_impacted_true_via_c0e0eec_changes_romm`` additionally
    builds the real Fraud Factor Analysis (c0e0eec) fixture end-to-end, to
    cover ``fraud_impacted`` actually landing on the worksheet through the
    same path production data uses (found while setting up manual demo
    data: the ``fraud_impacted``/``significant_risk`` related mirrors on
    this detail model do not reliably refresh just from writing the
    upstream source in a separate transaction - re-running
    ``action_load_detail()`` is required, exactly like the already-known
    ``control_risk`` limitation).
    """

    def setUp(self):
        super().setUp()
        env = self.env
        admin = env.ref("base.user_admin")
        self.admin = admin
        self.config = env.ref(
            "ssi_general_audit_worksheet_romm.general_audit_romm_scoring_config_default"
        )

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - d66d87a ROMM", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - d66d87a ROMM"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-D66D87A-ROMM-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - d66d87a ROMM", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - d66d87a ROMM", "code": "/"})
        )
        self.audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - d66d87a ROMM",
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

        account_group = (
            env["client_account_group"]
            .with_user(admin)
            .create({"name": "Test Account Group - d66d87a ROMM", "code": "/"})
        )
        self.account_type = (
            env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type - d66d87a ROMM",
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
                    "inherent_risk": "high",
                }
            )
        )

        ba9b2f0_ws_type = env.ref(
            "ssi_general_audit_worksheet_control_risk.worksheet_type_ba9b2f0"
        )
        env["general_audit_ws_ba9b2f0"].with_user(admin).create(
            {
                "general_audit_id": self.audit.id,
                "type_id": ba9b2f0_ws_type.id,
                "account_type_id": self.account_type.id,
                "risk": "high",
            }
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

    def _get_detail(self):
        self.d66d87a_worksheet.action_load_detail()
        return self.d66d87a_worksheet.detail_ids.filtered(
            lambda d: d.standard_detail_id == self.standard_detail
        )

    def test_romm_risk_initial_high_from_ir_high_cr_high(self):
        # IR high (0.90) x CR high (0.90) = 0.81 >= upper 0.8 -> high
        detail = self._get_detail()
        self.assertEqual(detail.inherent_risk, "high")
        self.assertEqual(detail.control_risk, "high")
        self.assertEqual(detail.romm_risk_initial, "high")

    def test_romm_high_when_significant_risk_true(self):
        self.standard_detail.write({"significant_risk": True})
        # FR medium (0.8) x SigRisk high (0.9) x Initial high (0.8) = 0.576 -> high
        detail = self._get_detail()
        self.assertEqual(detail.romm, "high")

    def test_romm_medium_when_significant_risk_false(self):
        self.standard_detail.write({"significant_risk": False})
        # FR medium (0.8) x SigRisk medium (0.6) x Initial high (0.8) = 0.384 -> medium
        detail = self._get_detail()
        self.assertEqual(detail.romm, "medium")

    def test_romm_propagates_to_standard_detail(self):
        self.standard_detail.write({"significant_risk": True})
        detail = self._get_detail()
        # Read detail.romm FIRST: it is what triggers the lazy compute (and
        # its write-back to standard_detail_id) on first access. Passing
        # self.standard_detail.romm as assertEqual's first argument would
        # evaluate it before detail.romm forces the compute to run, and
        # would see the pre-write-back value instead.
        romm = detail.romm
        self.assertEqual(self.standard_detail.romm, romm)

    def test_romm_recomputes_on_load_detail_after_ir_change(self):
        self.standard_detail.write({"significant_risk": True})
        detail = self._get_detail()
        self.assertEqual(detail.romm_risk_initial, "high")
        self.assertEqual(detail.romm, "high")

        # IR low (0.35) x CR high (0.90) = 0.315 -> below lower 0.4 -> low
        self.standard_detail.write({"inherent_risk": "low"})
        detail = self._get_detail()
        self.assertEqual(detail.romm_risk_initial, "low")
        # romm_risk_initial low -> romm falls back to "false" branch guard is
        # not hit here (romm_risk_initial is truthy "low"); score = FR medium
        # (0.8) x SigRisk high (0.9) x Initial low (0.3) = 0.216 -> low
        self.assertEqual(detail.romm, "low")

    def test_romm_reflects_updated_config_after_load_detail(self):
        detail = self._get_detail()
        self.assertEqual(detail.romm_risk_initial, "high")

        # Raise the ROMM Risk Initial upper threshold above the current
        # score (0.81) so the same IR/CR combination now classifies as
        # medium instead.
        self.config.write({"romm_risk_initial_threshold_upper": 0.95})
        detail = self._get_detail()
        self.assertEqual(detail.romm_risk_initial, "medium")

    def test_worksheet_romm_scoring_config_id_defaults_to_active_config(self):
        self.assertEqual(self.d66d87a_worksheet.romm_scoring_config_id, self.config)

    def test_existing_worksheet_keeps_pinned_config_after_active_setting_changes(self):
        # Baseline under the original (pinned) config.
        detail = self._get_detail()
        self.assertEqual(detail.romm_risk_initial, "high")
        self.assertEqual(detail.romm, "medium")

        # A second config with very different weights becomes the active
        # one in Settings - simulating another engagement/user switching it
        # for their own worksheet later.
        other_config = self.env["general_audit_romm_scoring_config"].create(
            {
                "name": "Other Config",
                "ir_weight_high": 0.1,
                "cr_weight_high": 0.1,
            }
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit_worksheet_romm.romm_scoring_config_id",
            other_config.id,
        )

        # Reloading THIS worksheet must NOT pick up the newly active config -
        # it stays pinned to the one recorded when it was created, so past
        # ROMM assessments remain reproducible/historically accurate.
        self.assertEqual(self.d66d87a_worksheet.romm_scoring_config_id, self.config)
        detail = self._get_detail()
        self.assertEqual(detail.romm_risk_initial, "high")
        self.assertEqual(detail.romm, "medium")

    def test_new_worksheet_picks_up_currently_active_config(self):
        other_config = self.env["general_audit_romm_scoring_config"].create(
            {"name": "Other Config"}
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit_worksheet_romm.romm_scoring_config_id",
            other_config.id,
        )
        d66d87a_ws_type = self.env.ref(
            "ssi_general_audit_worksheet_romm.worksheet_type_d66d87a"
        )
        # .new() (in-memory, unsaved) applies the same field defaults as
        # create() without hitting the "one worksheet of this type per
        # General Audit" uniqueness check - self.audit already has one from
        # setUp.
        new_worksheet = (
            self.env["general_audit_ws_d66d87a"]
            .with_user(self.admin)
            .new(
                {
                    "general_audit_id": self.audit.id,
                    "type_id": d66d87a_ws_type.id,
                }
            )
        )
        self.assertEqual(new_worksheet.romm_scoring_config_id, other_config)
        # The older worksheet from setUp is unaffected.
        self.assertEqual(self.d66d87a_worksheet.romm_scoring_config_id, self.config)

    def test_manually_repinning_worksheet_config_changes_romm(self):
        detail = self._get_detail()
        self.assertEqual(detail.romm_risk_initial, "high")

        other_config = self.env["general_audit_romm_scoring_config"].create(
            {
                "name": "Other Config",
                "romm_risk_initial_threshold_upper": 0.95,
            }
        )
        # Auditor deliberately re-pins this specific worksheet (still
        # allowed - readonly only outside the "open" state).
        self.d66d87a_worksheet.write({"romm_scoring_config_id": other_config.id})
        detail = self._get_detail()
        # Same IR/CR (0.81) now falls under the raised upper threshold (0.95).
        self.assertEqual(detail.romm_risk_initial, "medium")

    def test_fraud_impacted_true_via_c0e0eec_changes_romm(self):
        env = self.env
        # Baseline: fraud_impacted is False by default (no c0e0eec link yet).
        detail = self._get_detail()
        self.assertFalse(detail.fraud_impacted)
        self.assertEqual(detail.romm_risk_initial, "high")
        # FR medium (0.8) x SigRisk medium (0.6) x Initial high (0.8) = 0.384 -> medium
        self.assertEqual(detail.romm, "medium")

        c0e0eec_ws_type = env.ref(
            "ssi_general_audit_worksheet_understanding_entity.worksheet_type_c0e0eec"
        )
        c0e0eec_worksheet = (
            env["general_audit_ws_c0e0eec"]
            .with_user(self.admin)
            .create(
                {
                    "general_audit_id": self.audit.id,
                    "type_id": c0e0eec_ws_type.id,
                }
            )
        )
        indicator = env.ref(
            "ssi_general_audit_worksheet_understanding_entity"
            ".general_audit_fraud_factor_indicator_1_19623fa0"
        )
        env["general_audit_ws_c0e0eec.detail"].with_user(self.admin).create(
            {
                "worksheet_id": c0e0eec_worksheet.id,
                "indicator_id": indicator.id,
                "related_account_type_ids": [(6, 0, [self.account_type.id])],
            }
        )

        self.assertTrue(self.standard_detail.fraud_impacted)

        # Re-running Load Detail is required for the worksheet's own
        # fraud_impacted mirror (and anything depending on it) to refresh -
        # see class docstring.
        detail = self._get_detail()
        self.assertTrue(detail.fraud_impacted)
        self.assertEqual(detail.romm_risk_initial, "high")
        # FR high (1.2) x SigRisk medium (0.6) x Initial high (0.8) = 0.576 -> high
        self.assertEqual(detail.romm, "high")
