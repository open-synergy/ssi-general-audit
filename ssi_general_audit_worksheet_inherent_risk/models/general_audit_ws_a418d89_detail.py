# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSA418D89Detail(models.Model):
    """
    Account Level Inherent Risk — Detail Line (a418d89)

    One risk-assessment line within the Account Level Inherent Risk
    worksheet (WS.060.2), corresponding to a single standard detail
    (account / disclosure area) of the engagement.

    The auditor selects:

    - **Inherent risk factors without direct impact** — risk
      considerations that provide context but do not alone change the
      assessed risk level.
    - **Inherent risk factors with direct impact** — factors whose
      presence directly elevates the risk, potentially to significant risk.
    - **Likelihood of risk occurring** (low / high).
    - **Impact of risk** (low / high).
    - **Other significant risk factor** flag for additional considerations.

    ``inherent_risk`` and ``significant_risk`` are computed from the
    above inputs and written back to the parent
    ``general_audit.standard_detail`` via the inverse method, keeping
    the canonical standard detail in sync.

    Child of ``general_audit_ws_a418d89``.  Cascades on parent delete.
    """

    _name = "general_audit_ws_a418d89.detail"
    _description = "Worksheet a418d89 - Detail"
    _order = "worksheet_id, standard_detail_id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_a418d89",
        required=True,
        ondelete="cascade",
        help="Parent Account Level Inherent Risk worksheet for this line.",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="general_audit.standard_detail",
        required=True,
        ondelete="restrict",
        help="Linked standard detail (account) being evaluated.",
    )
    type_id = fields.Many2one(
        string="Account Type",
        related="standard_detail_id.type_id",
        store=True,
        help="Derived account type from the linked standard detail.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        related="standard_detail_id.currency_id",
        store=True,
        help="Derived currency from the linked standard detail.",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="standard_detail_id.sequence",
        store=True,
        help="Display order derived from the linked standard detail.",
    )
    inherent_risk_factor_without_impact_ids = fields.Many2many(
        string="Inherent Risk Factor Without Direct Impact",
        comodel_name="general_audit_inherent_risk_factor",
        relation="rel_general_audit_ws_a418d89_detail_2_without_impact",
        column1="detail_id",
        column2="inherent_risk_factor_id",
        domain=[
            ("direct_impact", "=", False),
        ],
        help=(
            "Inherent risk factors considered that "
            "do not directly impact the risk assessment."
        ),
    )
    inherent_risk_factor_with_impact_ids = fields.Many2many(
        string="Inherent Risk Factor With Direct Impact",
        comodel_name="general_audit_inherent_risk_factor",
        relation="rel_general_audit_ws_a418d89_detail_2_with_impact",
        column1="detail_id",
        column2="inherent_risk_factor_id",
        domain=[
            ("direct_impact", "=", True),
        ],
        help="Inherent risk factors that directly impact the risk assessment.",
    )
    fraud_risk = fields.Boolean(
        string="Fraud Risk",
        related="standard_detail_id.fraud_impacted",
        store=True,
        help="Indicates whether the area is impacted by identified fraud risk (derived).",
    )
    likelihood_risk_occuring = fields.Selection(
        string="Likelihood of Risk Occuring",
        selection=[
            ("low", "Low"),
            ("high", "High"),
        ],
        help="Assessed likelihood that the risk will occur.",
    )
    impact_of_risk = fields.Selection(
        string="Magnitude/Impact of Risk",
        selection=[
            ("low", "Low"),
            ("high", "High"),
        ],
        help="Assessed magnitude/impact should the risk occur.",
    )
    inherent_risk = fields.Selection(
        string="Inherent Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        compute="_compute_risk",
        store=True,
        help="Resulting inherent risk derived from likelihood and impact assessments.",
    )
    significant_risk = fields.Boolean(
        string="Significant Risk",
        compute="_compute_risk",
        compute_sudo=True,
        inverse="_inverse_to_standard_detail",
        store=True,
        help=(
            "Derived flag indicating significant risk. "
            "Updates the linked standard detail on change."
        ),
    )
    other_significant_risk_factor = fields.Boolean(
        string="Other Significant Risk Factor",
        default=False,
        help="Enable if there are other considerations that make this a significant risk.",
    )
    note = fields.Char(
        string="Note",
        help="Additional notes, rationale, or context for the assessment.",
    )

    @api.depends(
        "likelihood_risk_occuring",
        "impact_of_risk",
        "inherent_risk_factor_with_impact_ids",
        "fraud_risk",
        "other_significant_risk_factor",
    )
    def _compute_risk(self):
        for record in self:
            inherent_risk = significant_risk = False
            if record.likelihood_risk_occuring == "high":
                if record.impact_of_risk == "high":
                    inherent_risk = "high"
                    if (
                        record.inherent_risk_factor_with_impact_ids
                        or record.other_significant_risk_factor
                    ):
                        significant_risk = True
                elif record.impact_of_risk == "low":
                    inherent_risk = "medium"
            elif record.likelihood_risk_occuring == "low":
                if record.impact_of_risk == "high":
                    inherent_risk = "high"
                elif record.impact_of_risk == "low":
                    inherent_risk = "low"
            record.inherent_risk = inherent_risk
            record.significant_risk = significant_risk

    def _inverse_to_standard_detail(self):
        for record in self:
            record.standard_detail_id.write(
                {
                    "inherent_risk": self.inherent_risk,
                    "significant_risk": self.significant_risk,
                }
            )
