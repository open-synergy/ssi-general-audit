# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS0427d28Checklist(models.Model):
    _name = "general_audit_ws_0427d28.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Communication With Previous Auditor (0427d28) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_0427d28",
        required=True,
        ondelete="cascade",
        help="Reference to the parent worksheet (Previous Financial Reporting Issues).\n"
        "Links this checklist line to its worksheet and ensures cascading deletion.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_0427d28.item",
        required=True,
        help="The checklist definition/question represented by this line.\n"
        "Items contain predefined criteria to be assessed in this worksheet.",
    )
