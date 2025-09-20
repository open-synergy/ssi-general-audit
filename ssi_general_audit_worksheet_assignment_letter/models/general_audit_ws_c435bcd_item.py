# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc435bcdItem(models.Model):
    _name = "general_audit_ws_c435bcd.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Assignment Letter (c435bcd) - " "Checklist Item"

    code = fields.Char(
        default="/",
    )
