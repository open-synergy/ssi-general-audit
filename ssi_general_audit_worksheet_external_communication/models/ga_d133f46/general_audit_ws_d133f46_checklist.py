# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd133f46Checklist(models.Model):
    _name = "general_audit_ws_d133f46.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Use of Internal Auditor's Work Results (d133f46) " "- Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_d133f46",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent 'Use of Internal Auditor's Work Results' worksheet. "
            "Deleting the worksheet cascades to its checklist lines."
        ),
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_d133f46.item",
        required=True,
        help="The checklist item template this line refers to.",
    )
    communication_type = fields.Selection(
        related="item_id.communication_type",
        help="Type/category derived from the related checklist item.",
    )
