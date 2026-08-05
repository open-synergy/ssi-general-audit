# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditRommScoringConfig(models.Model):
    """
    Account Level ROMM — Risk Configuration

    Holds the configurable weights and thresholds used to compute the
    Account Level ROMM (``general_audit_ws_d66d87a.detail.romm``) from
    Inherent Risk, Control Risk, Fraud Risk and Significant Risk, replacing
    the values that used to be hardcoded in the client's risk-matrix
    spreadsheet.

    Two results are configured here, per the client's "Configurasi terkait
    ROMM Risk" document:

    * **ROMM Risk Initial** — ``score = IR weight x CR weight``, classified
      into High/Medium/Low using ``romm_risk_initial_threshold_upper``/
      ``_lower``.
    * **ROMM Risk Further** — ``score = FR weight x Significant Risk
      weight x ROMM Risk Initial weight``, classified using
      ``romm_risk_further_threshold_upper``/``_lower``.

    Singleton-style: a single record is seeded via data XML and consumed
    through :meth:`_get_config`. Fraud Risk and Significant Risk only have
    High/Medium weights (no Low) per the client's configuration document —
    there is intentionally no ``*_weight_low`` for either.
    """

    _name = "general_audit_romm_scoring_config"
    _description = "Account Level ROMM - Risk Configuration"

    name = fields.Char(
        string="Name",
        default="Risk Configuration",
        help="Label for this configuration record.",
    )

    # ROMM Risk Initial (Inherent Risk x Control Risk)
    ir_weight_high = fields.Float(
        string="Inherent Risk Weight - High",
        default=0.90,
        help="Weight applied when Inherent Risk is High.",
    )
    ir_weight_medium = fields.Float(
        string="Inherent Risk Weight - Medium",
        default=0.65,
        help="Weight applied when Inherent Risk is Medium.",
    )
    ir_weight_low = fields.Float(
        string="Inherent Risk Weight - Low",
        default=0.35,
        help="Weight applied when Inherent Risk is Low.",
    )
    cr_weight_high = fields.Float(
        string="Control Risk Weight - High",
        default=0.90,
        help="Weight applied when Control Risk is High.",
    )
    cr_weight_medium = fields.Float(
        string="Control Risk Weight - Medium",
        default=0.65,
        help="Weight applied when Control Risk is Medium.",
    )
    cr_weight_low = fields.Float(
        string="Control Risk Weight - Low",
        default=0.35,
        help="Weight applied when Control Risk is Low.",
    )
    romm_risk_initial_threshold_upper = fields.Float(
        string="ROMM Risk Initial Threshold - Upper",
        default=0.8,
        help=(
            "Minimum score (IR weight x CR weight) classified as High. "
            "Scores between the lower and upper threshold are Medium."
        ),
    )
    romm_risk_initial_threshold_lower = fields.Float(
        string="ROMM Risk Initial Threshold - Lower",
        default=0.4,
        help="Minimum score classified as Medium; below this is Low.",
    )

    # ROMM Risk Further (Fraud Risk x Significant Risk x ROMM Risk Initial)
    fr_weight_high = fields.Float(
        string="Fraud Risk Weight - High",
        default=1.2,
        help="Weight applied when the account is impacted by fraud risk.",
    )
    fr_weight_medium = fields.Float(
        string="Fraud Risk Weight - Medium",
        default=0.8,
        help="Weight applied when the account is not impacted by fraud risk.",
    )
    significant_risk_weight_high = fields.Float(
        string="Significant Risk Weight - High",
        default=0.9,
        help="Weight applied when the account is flagged as a significant risk.",
    )
    significant_risk_weight_medium = fields.Float(
        string="Significant Risk Weight - Medium",
        default=0.6,
        help="Weight applied when the account is not flagged as a significant risk.",
    )
    romm_risk_initial_weight_high = fields.Float(
        string="ROMM Risk Initial Result Weight - High",
        default=0.8,
        help="Weight applied when the ROMM Risk Initial result is High.",
    )
    romm_risk_initial_weight_medium = fields.Float(
        string="ROMM Risk Initial Result Weight - Medium",
        default=0.55,
        help="Weight applied when the ROMM Risk Initial result is Medium.",
    )
    romm_risk_initial_weight_low = fields.Float(
        string="ROMM Risk Initial Result Weight - Low",
        default=0.3,
        help="Weight applied when the ROMM Risk Initial result is Low.",
    )
    romm_risk_further_threshold_upper = fields.Float(
        string="ROMM Risk Further Threshold - Upper",
        default=0.4,
        help=(
            "Minimum score (FR weight x Significant Risk weight x ROMM Risk "
            "Initial weight) classified as High."
        ),
    )
    romm_risk_further_threshold_lower = fields.Float(
        string="ROMM Risk Further Threshold - Lower",
        default=0.3,
        help="Minimum score classified as Medium; below this is Low.",
    )

    @api.model
    def _get_config(self):
        """Return the Risk Configuration record used to compute ROMM.

        The record picked in Settings > General Audit
        (``res.config.settings.romm_scoring_config_id``, stored as
        ``ir.config_parameter``) takes precedence. If that setting is
        empty or points to a deleted record, falls back to the first
        available record (auto-creating one with defaults if none exists),
        so ROMM still computes correctly before anyone visits Settings.
        """
        param = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("ssi_general_audit_worksheet_romm.romm_scoring_config_id")
        )
        if param:
            config = self.browse(int(param)).exists()
            if config:
                return config

        config = self.search([], limit=1)
        if not config:
            config = self.create({})
        return config

    def _weight(self, prefix, level):
        self.ensure_one()
        return getattr(self, "%s_weight_%s" % (prefix, level))

    def _classify(self, score, upper, lower):
        if score >= upper:
            return "high"
        if score >= lower:
            return "medium"
        return "low"

    def get_romm_risk_initial(self, inherent_risk, control_risk):
        """Classify ROMM Risk Initial from Inherent Risk x Control Risk."""
        self.ensure_one()
        if not inherent_risk or not control_risk:
            return False
        score = self._weight("ir", inherent_risk) * self._weight("cr", control_risk)
        return self._classify(
            score,
            self.romm_risk_initial_threshold_upper,
            self.romm_risk_initial_threshold_lower,
        )

    def get_romm_risk_further(
        self, fraud_risk, significant_risk_level, romm_risk_initial
    ):
        """Classify ROMM Risk Further from FR x Significant Risk x ROMM Risk Initial."""
        self.ensure_one()
        if not romm_risk_initial:
            return False
        score = (
            self._weight("fr", fraud_risk)
            * self._weight("significant_risk", significant_risk_level)
            * self._weight("romm_risk_initial", romm_risk_initial)
        )
        return self._classify(
            score,
            self.romm_risk_further_threshold_upper,
            self.romm_risk_further_threshold_lower,
        )
