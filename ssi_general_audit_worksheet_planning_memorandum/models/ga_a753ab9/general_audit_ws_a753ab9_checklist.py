# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa753ab9Checklist(models.Model):
    _name = "general_audit_ws_a753ab9.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Audit Planning Memorandum (a753ab9) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_a753ab9",
        required=True,
        ondelete="cascade",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_a753ab9.item",
        required=True,
    )
    checklist_type = fields.Selection(
        related="item_id.checklist_type",
        compute_sudo=True,
        help="Type/category of the checklist item, inherited from the item.",
    )
