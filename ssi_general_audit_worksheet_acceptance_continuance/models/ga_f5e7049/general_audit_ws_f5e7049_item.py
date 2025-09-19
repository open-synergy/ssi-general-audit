# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSf5e7049Item(models.Model):
    _name = "general_audit_ws_f5e7049.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Management Integrity (f5e7049) - " "Checklist Item"

    code = fields.Char(
        default="/",
    )
