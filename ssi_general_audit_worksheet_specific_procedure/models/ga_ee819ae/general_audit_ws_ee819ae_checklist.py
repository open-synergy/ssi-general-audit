# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSee819aeChecklist(models.Model):
    _name = "general_audit_ws_ee819ae.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Commitment and Contingent (ee819ae) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ee819ae",
        required=True,
        ondelete="cascade",
        help="Parent Commitment and Contingent worksheet for this checklist line.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_ee819ae.item",
        required=True,
        help="Checklist item/question being evaluated on this line.",
    )
    explanation = fields.Text(
        string="Explanation/Reference",
        help="Additional explanation or reference supporting the checklist response.",
    )
