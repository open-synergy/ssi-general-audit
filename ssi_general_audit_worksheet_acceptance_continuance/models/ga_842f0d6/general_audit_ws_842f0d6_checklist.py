# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS842f0d6Checklist(models.Model):
    _name = "general_audit_ws_842f0d6.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Money Laudring Issues (842f0d6) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_842f0d6",
        required=True,
        ondelete="cascade",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_842f0d6.item",
        required=True,
    )
