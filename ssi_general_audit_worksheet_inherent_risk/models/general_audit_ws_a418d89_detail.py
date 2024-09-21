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
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="general_audit.standard_detail",
        required=True,
    )
    type_id = fields.Many2one(
        string="Account Type",
        related="standard_detail_id.type_id",
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        related="standard_detail_id.currency_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="standard_detail_id.sequence",
        store=True,
    )
    inherent_risk_factor_a = fields.Boolean(
        string="Inherent Risk Factor A",
        default=False,
    )
    inherent_risk_factor_b = fields.Boolean(
        string="Inherent Risk Factor B",
        default=False,
    )
    inherent_risk_factor_c = fields.Boolean(
        string="Inherent Risk Factor C",
        default=False,
    )
    inherent_risk_factor_d = fields.Boolean(
        string="Inherent Risk Factor D",
        default=False,
    )
    inherent_risk_factor_e = fields.Boolean(
        string="Inherent Risk Factor E",
        default=False,
    )
    inherent_risk_factor_f = fields.Boolean(
        string="Inherent Risk Factor F",
        default=False,
    )
    inherent_risk_factor_g = fields.Boolean(
        string="Inherent Risk Factor G",
        default=False,
    )
    inherent_risk_factor_h = fields.Boolean(
        string="Inherent Risk Factor H",
        default=False,
    )
    inherent_risk_factor_i = fields.Boolean(
        string="Inherent Risk Factor I",
        default=False,
    )
    inherent_risk_factor_j = fields.Boolean(
        string="Inherent Risk Factor J",
        default=False,
    )
    fraud_risk = fields.Boolean(
        string="Fraud Risk", related="standard_detail_id.fraud_impacted", store=True
    )
    likelihood_risk_occuring = fields.Selection(
        string="Likelihood of Risk Occuring",
        selection=[
            ("low", "Low"),
            ("high", "High"),
        ],
    )
    impact_of_risk = fields.Selection(
        string="Magnitude/Impact of Risk",
        selection=[
            ("low", "Low"),
            ("high", "High"),
        ],
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
    )
    significant_risk = fields.Boolean(
        string="Significant Risk",
        compute="_compute_risk",
        inverse="_inverse_to_standard_detail",
        store=True,
    )
    other_significant_risk_factor = fields.Boolean(
        string="Other Significant Risk Factor",
        default=False,
    )
    note = fields.Char(
        string="Note",
    )

    @api.depends(
        "likelihood_risk_occuring",
        "impact_of_risk",
        "inherent_risk_factor_f",
        "inherent_risk_factor_g",
        "inherent_risk_factor_h",
        "inherent_risk_factor_i",
        "inherent_risk_factor_j",
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
                        record.inherent_risk_factor_f
                        or record.inherent_risk_factor_g
                        or record.inherent_risk_factor_h
                        or record.inherent_risk_factor_i
                        or record.inherent_risk_factor_j
                        or record.fraud_risk
                    ) or record.other_significant_risk_factor:
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
