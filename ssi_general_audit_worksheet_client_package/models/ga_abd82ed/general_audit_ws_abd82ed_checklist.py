# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSabd82edChecklist(models.Model):
    """Checklist value line for the Client Assistance Package worksheet (abd82ed).

    Stores the auditor's response (yes / no / N/A) and any comments for one
    checklist item.  The set of items is driven by the related ``item`` master
    and the ``mixin.checklist`` mixin that auto-populates this one2many.
    """

    _name = "general_audit_ws_abd82ed.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Client Assistance Package (abd82ed) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_abd82ed",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the related worksheet. "
            "Deleting the worksheet will remove its checklist entries."
        ),
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_abd82ed.item",
        required=True,
        help="Checklist item being answered or evaluated.",
    )
