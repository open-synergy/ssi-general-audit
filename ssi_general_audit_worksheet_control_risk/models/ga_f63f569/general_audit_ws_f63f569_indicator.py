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
        help="Related detail line of the worksheet.",
    )
    worksheet_id = fields.Many2one(
        related="detail_id.worksheet_id",
        store=True,
        help="Parent worksheet, derived from the related detail.",
    )
    control_id = fields.Many2one(
        related="detail_id.control_id",
        store=True,
        help="IT control being evaluated (propagated from detail).",
    )
    category_id = fields.Many2one(
        related="detail_id.control_id.category_id",
        store=True,
        help="Category of the IT control (propagated).",
    )
    indicator_id = fields.Many2one(
        string="Indicator",
        comodel_name="general_audit_it_control_indicator",
        required=True,
        help="Control indicator to be evaluated.",
    )
    allowed_option_ids = fields.Many2many(
        string="Options",
        related="indicator_id.option_set_id.option_ids",
        help="Options allowed for this line, inherited from the item's option set.",
    )
    result = fields.Many2one(
        comodel_name="checklist.option",
        required=False,
        ondelete="restrict",
        help="Selected option for this checklist item.",
    )
    explanation = fields.Text(
        string="Explanation",
        help="Notes or justification for the indicator result.",
    )
