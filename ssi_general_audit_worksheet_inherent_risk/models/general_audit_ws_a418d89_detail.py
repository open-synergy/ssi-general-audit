# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSA418D89Detail(models.Model):
    _name = "general_audit_ws_a418d89.detail"
    _description = "Worksheet a418d89 - Detail"
    _order = "worksheet_id, standard_detail_id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_a418d89",
        required=True,
        ondelete="cascade",
        help="""Parent Account Level Inherent Risk worksheet.
Deleting the worksheet will remove its detail lines.""",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="general_audit.standard_detail",
        required=True,
        help="Linked standard detail (account/line) being evaluated in this worksheet.",
    )
    type_id = fields.Many2one(
        string="Account Type",
        related="standard_detail_id.type_id",
        store=True,
        help="Account type automatically derived from the linked standard detail.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        related="standard_detail_id.currency_id",
        store=True,
        help="Currency automatically derived from the linked standard detail.",
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
        help="""Inherent risk factors considered that
do not directly impact the risk assessment.""",
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
        help="""Indicates whether the area is impacted by "
identified fraud risk (from the standard detail).""",
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

    @api.depends(
        "likelihood_risk_occuring",
        "impact_of_risk",
        "inherent_risk_factor_with_impact_ids",
        "fraud_risk",
    )
    def _compute_risk(self):
        for record in self:
            inherent_risk = False
            if record.likelihood_risk_occuring == "high":
                if record.impact_of_risk == "high":
                    inherent_risk = "high"
                elif record.impact_of_risk == "low":
                    inherent_risk = "medium"
            elif record.likelihood_risk_occuring == "low":
                if record.impact_of_risk == "high":
                    inherent_risk = "high"
                elif record.impact_of_risk == "low":
                    inherent_risk = "low"
            record.inherent_risk = inherent_risk
