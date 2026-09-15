# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWsF3ed115Checklist(models.Model):
    """
    Checklist answer line for Final Communication With TCWG (f3ed115).

    Each record stores the auditor's response to one checklist item
    from ``general_audit_ws_f3ed115.item``. Carries ``category_id``
    (from the item master) for grouping in the form view.

    Child of ``general_audit_ws_f3ed115``. Cascades on parent delete.
    """

    _name = "general_audit_ws_f3ed115.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Final Communication With TCWG (f3ed115) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_f3ed115",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent Final Communication With TCWG "
            "worksheet. Deleting the worksheet cascades to its "
            "checklist lines."
        ),
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_f3ed115.item",
        required=True,
        help="The checklist item template this line refers to.",
    )
    category_id = fields.Many2one(
        related="item_id.category_id",
        help="Category of the checklist item, inherited from the item.",
    )
