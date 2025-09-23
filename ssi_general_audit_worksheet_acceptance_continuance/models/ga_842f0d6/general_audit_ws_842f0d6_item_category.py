# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS842f0d6Item(models.Model):
    _name = "general_audit_ws_842f0d6.item_categ"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Money Laudring Issues (842f0d6) - " "Checklist Item Category"

    code = fields.Char(
        default="/",
    )
    categ = fields.Selection(
        string="Category",
        selection=[
            ("profile", "Profile"),
            ("country", "Country"),
            ("business", "Business"),
            ("product", "Product/Service"),
        ],
    )
