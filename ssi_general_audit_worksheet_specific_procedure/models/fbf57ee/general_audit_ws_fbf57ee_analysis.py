# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSfbf57eeAnalysis(models.Model):
    _name = "general_audit_ws_fbf57ee.analysis"
    _description = "Going Concern (fbf57ee) - Analysis"
    _order = "worksheet_id, going_concern_category_id, going_concern_id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_fbf57ee",
        string="Worksheet",
        required=True,
        ondelete="cascade",
        index=True,
        help="Parent Going Concern worksheet for this analysis line.",
    )
    going_concern_id = fields.Many2one(
        string="Going Concern",
        comodel_name="general_audit_going_concern",
        required=True,
        ondelete="restrict",
        help="Specific going concern indicator/condition being assessed.",
    )
    going_concern_category_id = fields.Many2one(
        string="Going Concern Category",
        related="going_concern_id.category_id",
        store=True,
        help="Category of the going concern indicator (derived).",
    )
    risk_assessment = fields.Selection(
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        string="Risk Assessment",
        default="medium",
        required=True,
        help="Indicates the risk assessment level for this procedure.",
    )
    explanation = fields.Text(
        string="Explanation",
        help="Provide additional details or explanations regarding the procedure.",
    )
    reference = fields.Char(
        string="Reference",
        help="Reference document or note related to this procedure.",
    )
