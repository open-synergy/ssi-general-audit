# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa033cc6Checklist(models.Model):
    """Checklist value instance for the Trial Balance worksheet.

    Each record represents an auditor's response to one checklist item within
    the ``general_audit_ws_a033cc6`` (Trial Balance) worksheet. Stores the
    actual value/response provided by the auditor for each verification
    checkpoint, linking the master item definition to the worksheet instance.

    Inherits from ``mixin.checklist.value`` which provides response fields
    (e.g., answer, notes, conclusion) standardised across all checklist models.
    """

    _name = "general_audit_ws_a033cc6.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Trial Balance (a033cc6) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_a033cc6",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent Trial Balance worksheet record. "
            "Links this checklist value to its worksheet and ensures it "
            "is deleted when the worksheet is removed."
        ),
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_a033cc6.item",
        required=True,
        help=(
            "Reference to the checklist item definition that this value "
            "corresponds to. Used to display the item label and properties "
            "associated with this checklist entry."
        ),
    )
