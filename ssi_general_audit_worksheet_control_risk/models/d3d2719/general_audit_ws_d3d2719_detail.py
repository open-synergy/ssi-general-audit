# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSD3D2719Detail(models.Model):
    _name = "general_audit_ws_d3d2719.detail"
    _description = "Worksheet d3d2719 - Detail"
    _order = "worksheet_id, category_id, control_id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_d3d2719",
        required=True,
        ondelete="cascade",
        help="Parent General Control Evaluation worksheet.",
    )
    control_id = fields.Many2one(
        string="General Control",
        comodel_name="general_audit_general_control",
        required=True,
        help="General control being evaluated.",
    )
    category_id = fields.Many2one(
        string="Category",
        related="control_id.category_id",
        store=True,
        help="Category of the selected control (auto-filled).",
    )
    result = fields.Selection(
        string="Result",
        selection=[
            ("adequate", "Adequate"),
            ("inadequate", "Inadequate"),
        ],
        help="Conclusion for this control based on the indicators and evidence.",
    )
    explanation = fields.Text(
        string="Explanation",
        help="Rationale, observations, or notes supporting the result.",
    )
    indicator_ids = fields.One2many(
        string="Indicators",
        comodel_name="general_audit_ws_d3d2719.indicator",
        inverse_name="detail_id",
        help="Indicator lines used to assess this control.",
    )
