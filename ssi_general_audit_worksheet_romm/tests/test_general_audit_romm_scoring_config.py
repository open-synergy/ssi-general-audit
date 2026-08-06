# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo.tests.common import TransactionCase


class TestGeneralAuditRommScoringConfig(TransactionCase):
    def setUp(self):
        super().setUp()
        self.config = self.env.ref(
            "ssi_general_audit_worksheet_romm.general_audit_romm_scoring_config_default"
        )

    def test_get_config_returns_seeded_record(self):
        self.assertEqual(self.config._get_config(), self.config)

    def test_get_config_returns_empty_when_none_exists(self):
        # Deliberately does NOT auto-create a replacement here - doing so
        # used to race this module's own seed data during a fresh
        # install/upgrade (the backfill of general_audit_ws_d66d87a
        # .romm_scoring_config_id's default ran before the seed XML had
        # loaded, so the table was briefly empty) and left a duplicate,
        # xml_id-less config record behind alongside the real seeded one.
        self.env["general_audit_romm_scoring_config"].search([]).unlink()
        config = self.env["general_audit_romm_scoring_config"]._get_config()
        self.assertFalse(config)

    def test_get_config_respects_settings_parameter(self):
        # Settings > General Audit > Risk Configuration (res.config.settings
        # romm_scoring_config_id) overrides the "first record" fallback.
        other_config = self.env["general_audit_romm_scoring_config"].create(
            {"name": "Other Config", "ir_weight_high": 0.5}
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit_worksheet_romm.romm_scoring_config_id",
            other_config.id,
        )
        self.assertEqual(
            self.env["general_audit_romm_scoring_config"]._get_config(),
            other_config,
        )

    def test_get_config_falls_back_when_parameter_points_to_deleted_record(self):
        other_config = self.env["general_audit_romm_scoring_config"].create(
            {"name": "Other Config"}
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit_worksheet_romm.romm_scoring_config_id",
            other_config.id,
        )
        other_config.unlink()
        self.assertEqual(
            self.env["general_audit_romm_scoring_config"]._get_config(),
            self.config,
        )

    def test_romm_risk_initial_high(self):
        # IR High (0.90) x CR High (0.90) = 0.81 -> >= upper 0.8 -> high
        self.assertEqual(
            self.config.get_romm_risk_initial("high", "high"),
            "high",
        )

    def test_romm_risk_initial_medium(self):
        # IR Medium (0.65) x CR Medium (0.65) = 0.4225 -> >= lower 0.4 -> medium
        self.assertEqual(
            self.config.get_romm_risk_initial("medium", "medium"),
            "medium",
        )

    def test_romm_risk_initial_low(self):
        # IR Low (0.35) x CR Low (0.35) = 0.1225 -> < lower 0.4 -> low
        self.assertEqual(
            self.config.get_romm_risk_initial("low", "low"),
            "low",
        )

    def test_romm_risk_initial_false_when_missing_input(self):
        self.assertFalse(self.config.get_romm_risk_initial(False, "high"))
        self.assertFalse(self.config.get_romm_risk_initial("high", False))

    def test_romm_risk_further_high(self):
        # FR High (1.2) x SigRisk High (0.9) x Initial High (0.8) = 0.864 -> high
        self.assertEqual(
            self.config.get_romm_risk_further("high", "high", "high"),
            "high",
        )

    def test_romm_risk_further_medium(self):
        # FR Medium (0.8) x SigRisk High (0.9) x Initial Medium (0.55) = 0.396 -> medium
        self.assertEqual(
            self.config.get_romm_risk_further("medium", "high", "medium"),
            "medium",
        )

    def test_romm_risk_further_low(self):
        # FR Medium (0.8) x SigRisk Medium (0.6) x Initial Low (0.3) = 0.144 -> low
        self.assertEqual(
            self.config.get_romm_risk_further("medium", "medium", "low"),
            "low",
        )

    def test_romm_risk_further_false_when_initial_missing(self):
        self.assertFalse(self.config.get_romm_risk_further("high", "high", False))

    def test_custom_weights_change_classification(self):
        self.config.write(
            {
                "romm_risk_initial_threshold_upper": 0.9,
                "romm_risk_initial_threshold_lower": 0.5,
            }
        )
        # Same inputs that were "high" with default thresholds (0.81) now
        # fall under the raised upper threshold (0.9) -> medium.
        self.assertEqual(
            self.config.get_romm_risk_initial("high", "high"),
            "medium",
        )
