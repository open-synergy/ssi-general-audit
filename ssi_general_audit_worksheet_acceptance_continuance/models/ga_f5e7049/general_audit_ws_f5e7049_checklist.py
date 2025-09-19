# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSf5e7049Checklist(models.Model):
    _name = "general_audit_ws_f5e7049.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Management Integrity (f5e7049) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_f5e7049",
        required=True,
        ondelete="cascade",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_f5e7049.item",
        required=True,
    )
