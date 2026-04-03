# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSae48e68Checklist(models.Model):
    """
    External Communication Schedule — Checklist Line (ae48e68)

    A single assessed checklist item within the External Communication
    Schedule worksheet (WS.050.1).  Captures the auditor's Yes / No / N-A
    response for one specific communication-related procedure.

    Child of ``general_audit_ws_ae48e68``.  Cascades on parent delete.
    """

    _name = "general_audit_ws_ae48e68.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "External Communication (ae48e68) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae48e68",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent External Communication (ae48e68) worksheet. "
            "When the worksheet is deleted, "
            "its checklist lines are removed as well."
        ),
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_ae48e68.item",
        required=True,
        help="The checklist item template this line refers to.",
    )
