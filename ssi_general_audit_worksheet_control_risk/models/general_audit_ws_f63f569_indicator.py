# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSF63F569Indicator(models.Model):
    _name = "general_audit_ws_f63f569.indicator"
    _description = "Worksheet f63f569 - Indicator"

    detail_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_f63f569.detail",
        required=True,
        ondelete="cascade",
    )
    worksheet_id = fields.Many2one(
        related="detail_id.worksheet_id",
        store=True,
    )
    control_id = fields.Many2one(
        related="detail_id.control_id",
        store=True,
    )
    category_id = fields.Many2one(
        related="detail_id.control_id.category_id",
        store=True,
    )
    indicator_id = fields.Many2one(
        string="Indicator",
        comodel_name="general_audit_general_control_indicator",
        required=True,
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
