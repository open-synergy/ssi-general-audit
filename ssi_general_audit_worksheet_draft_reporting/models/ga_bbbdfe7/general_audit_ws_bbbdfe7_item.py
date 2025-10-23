# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbbbdfe7Item(models.Model):
    _name = "general_audit_ws_bbbdfe7.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Management Representation (bbbdfe7) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="Item code or number. Use '/' to auto-generate the code.",
    )
