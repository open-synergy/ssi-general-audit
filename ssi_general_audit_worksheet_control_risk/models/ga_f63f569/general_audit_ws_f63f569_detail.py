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
        help="Parent IT Control Evaluation worksheet.",
    )
    control_id = fields.Many2one(
        string="IT Control",
        comodel_name="general_audit_it_control",
        required=True,
        help="IT control being evaluated.",
    )
    category_id = fields.Many2one(
        string="Category",
        related="control_id.category_id",
        store=True,
        help="Category of the selected IT control (auto-filled).",
    )
    allowed_option_ids = fields.Many2many(
        string="Options",
        related="control_id.option_set_id.option_ids",
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
        help="Rationale, observations, or notes supporting the result.",
    )
    indicator_ids = fields.One2many(
        string="Indicators",
        comodel_name="general_audit_ws_f63f569.indicator",
        inverse_name="detail_id",
        help="Indicator lines used to assess this IT control.",
    )
