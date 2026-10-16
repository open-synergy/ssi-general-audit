# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWsA8c54f3Checklist(models.Model):
    """
    Checklist answer line for Audit Final Memorandum (a8c54f3).

    Each record stores the auditor's response to one checklist item
    from ``general_audit_ws_a8c54f3.item``. Carries ``category_id``
    (from the item master) for grouping in the form view.

    Child of ``general_audit_ws_a8c54f3``. Cascades on parent delete.
    """

    _name = "general_audit_ws_a8c54f3.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Audit Final Memorandum (a8c54f3) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_a8c54f3",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent Audit Final Memorandum "
            "worksheet. Deleting the worksheet cascades to its "
            "checklist lines."
        ),
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_a8c54f3.item",
        required=True,
        help="The checklist item template this line refers to.",
    )
    category_id = fields.Many2one(
        related="item_id.category_id",
        help="Category of the checklist item, inherited from the item.",
    )
