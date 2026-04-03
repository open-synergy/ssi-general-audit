# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSfc75636Checklist(models.Model):
    """
    Checklist answer line for the Independent Auditor's Report Review (fc75636).

    Each record stores the auditor's response (Yes / No / N-A) to one
    report-review item from ``general_audit_ws_fc75636.item``.  Carries
    ``checklist_type`` (opinion type) and ``category_id`` (report section)
    from the item master for grouping in the form view.
    """

    _name = "general_audit_ws_fc75636.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Independen Auditor Report (fc75636) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_fc75636",
        required=True,
        ondelete="cascade",
        help="Parent worksheet to which this checklist line belongs.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_fc75636.item",
        required=True,
        help="Checklist item that must be answered on this line.",
    )
    checklist_type = fields.Selection(
        related="item_id.checklist_type",
        help="Type of the checklist item, inherited from the item.",
    )
    category_id = fields.Many2one(
        related="item_id.category_id",
        help="Category of the checklist item, inherited from the item.",
    )
