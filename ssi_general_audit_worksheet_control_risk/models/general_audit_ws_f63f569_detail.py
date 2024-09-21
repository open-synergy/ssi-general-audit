# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSF63F569Detail(models.Model):
    _name = "general_audit_ws_f63f569.detail"
    _description = "Worksheet f63f569 - Detail"
    _order = "worksheet_id, category_id, control_id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_f63f569",
        required=True,
        ondelete="cascade",
    )
    control_id = fields.Many2one(
        string="General Control",
        comodel_name="general_audit_general_control",
        required=True,
    )
    category_id = fields.Many2one(
        string="Category",
        related="control_id.category_id",
        store=True,
    )
    result = fields.Selection(
        string="Result",
        selection=[
            ("adequate", "Adequate"),
            ("inadequate", "Inadequate"),
        ],
    )
    explanation = fields.Text(
        string="Explanation",
    )
    indicator_ids = fields.One2many(
        string="Indicators",
        comodel_name="general_audit_ws_f63f569.indicator",
        inverse_name="detail_id",
    )
