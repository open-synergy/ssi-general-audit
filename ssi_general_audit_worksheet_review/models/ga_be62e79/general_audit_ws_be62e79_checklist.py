# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbe62e79Checklist(models.Model):
    _name = "general_audit_ws_be62e79.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Financial Statement Disclosure Review (be62e79) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_be62e79",
        required=True,
        ondelete="cascade",
        help="Parent worksheet to which this checklist line belongs.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_be62e79.item",
        required=True,
        help="Checklist item that must be answered on this line.",
    )
    checklist_type = fields.Selection(
        related="item_id.checklist_type",
        help="Type/category of the checklist item, inherited from the item.",
    )
