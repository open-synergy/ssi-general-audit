# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb3ff42fChecklist(models.Model):
    """
    Communication With Management — Checklist Line (b3ff42f)

    A single assessed checklist item within the Communication With
    Management worksheet (WS.050.2).  The ``communication_type`` field
    (derived from the item master) groups lines by the nature of the
    communication activity.

    Child of ``general_audit_ws_b3ff42f``.  Cascades on parent delete.
    """

    _name = "general_audit_ws_b3ff42f.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Communication With Management (b3ff42f) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_b3ff42f",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent Communication With Management worksheet. "
            "Deleting the worksheet cascades to its checklist lines."
        ),
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_b3ff42f.item",
        required=True,
        help="The checklist item template this line refers to.",
    )
    communication_type = fields.Selection(
        related="item_id.communication_type",
        help="Type of communication derived from the related checklist item.",
    )
