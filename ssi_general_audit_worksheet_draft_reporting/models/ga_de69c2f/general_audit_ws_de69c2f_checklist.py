# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSde69c2fChecklist(models.Model):
    _name = "general_audit_ws_de69c2f.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Final Discussion (de69c2f) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_de69c2f",
        required=True,
        ondelete="cascade",
        help="Parent worksheet to which this checklist line belongs.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_de69c2f.item",
        required=True,
        help="Checklist item that must be answered on this line.",
    )
    checklist_type = fields.Selection(
        related="item_id.checklist_type",
        help="Type/category of the checklist item, inherited from the item.",
    )
