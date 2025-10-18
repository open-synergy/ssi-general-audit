# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc8740d4Checklist(models.Model):
    _name = "general_audit_ws_c8740d4.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Preliminary Analytic Procedure (c8740d4) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_c8740d4",
        required=True,
        ondelete="cascade",
        help="Worksheet document that this checklist value belongs to.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_c8740d4.item",
        required=True,
        help="Checklist item being answered on this worksheet.",
    )
