# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc94e287Checklist(models.Model):
    """
    Communication With TCWG — Checklist Line (c94e287)

    A single assessed checklist item within the Communication With TCWG
    worksheet (WS.050.3).  The ``communication_type`` field (derived from
    the item master) groups lines by the nature of the communication
    activity with those charged with governance.

    Child of ``general_audit_ws_c94e287``.  Cascades on parent delete.
    """

    _name = "general_audit_ws_c94e287.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Communication With TCWG (c94e287) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_c94e287",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent Communication With TCWG worksheet. "
            "Deleting the worksheet cascades to its checklist lines."
        ),
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_c94e287.item",
        required=True,
        help="The checklist item template this line refers to.",
    )
    communication_type = fields.Selection(
        related="item_id.communication_type",
        help="Type of communication derived from the related checklist item.",
    )
