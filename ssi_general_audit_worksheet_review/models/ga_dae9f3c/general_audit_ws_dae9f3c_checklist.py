# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSdae9f3cChecklist(models.Model):
    _name = "general_audit_ws_dae9f3c.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Audit Evidence Evaluation (dae9f3c) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_dae9f3c",
        required=True,
        ondelete="cascade",
        help="Parent worksheet to which this checklist line belongs.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_dae9f3c.item",
        required=True,
        help="Checklist item that must be answered on this line.",
    )
