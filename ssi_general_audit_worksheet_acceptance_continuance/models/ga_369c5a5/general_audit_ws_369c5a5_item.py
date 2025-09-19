# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS0427d28Item(models.Model):
    _name = "general_audit_ws_0427d28.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Previous Financial Reporting Issues (0427d28) - " "Checklist Item"

    code = fields.Char(
        default="/",
    )
