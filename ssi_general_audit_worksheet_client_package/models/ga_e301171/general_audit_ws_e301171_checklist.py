# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSe301171Checklist(models.Model):
    _name = "general_audit_ws_e301171.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Journal Entry Testing (e301171) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_e301171",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the related Journal Entry Testing worksheet. "
            "Removing the worksheet will delete its checklist entries."
        ),
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_e301171.item",
        required=True,
        help="Checklist item for journal entry testing.",
    )
