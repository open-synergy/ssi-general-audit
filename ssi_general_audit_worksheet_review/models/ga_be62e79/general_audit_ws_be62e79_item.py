# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbe62e79Item(models.Model):
    _name = "general_audit_ws_be62e79.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Financial Statement Disclosure Review (be62e79) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="Item code or number. Use '/' to auto-generate the code.",
    )
    checklist_type = fields.Selection(
        string="Type of Checklist",
        selection=[
            ("primary", "Primary Disclosure"),
            ("additional", "Additional Disclosure"),
            ("new", "New Disclosure"),
        ],
        required=True,
        help="Defines the category of checklist where this item is used.",
    )
