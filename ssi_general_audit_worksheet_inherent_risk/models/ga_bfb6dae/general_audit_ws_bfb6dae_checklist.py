# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbfb6daeChecklist(models.Model):
    _name = "general_audit_ws_bfb6dae.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Inherent Risk (bfb6dae) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_bfb6dae",
        required=True,
        ondelete="cascade",
        help="Parent Inherent Risk worksheet for this checklist line.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_bfb6dae.item",
        required=True,
        help="Checklist item/question being evaluated on this line.",
    )
