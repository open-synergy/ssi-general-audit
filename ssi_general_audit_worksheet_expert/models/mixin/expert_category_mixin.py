# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class MixinExpertCategory(models.Model):
    _name = "mixin.expert.category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Abstract Base for Expert Categories"

    code = fields.Char(
        default="/",
        help="Unique code for the option set. Use '/' to auto-generate.",
    )
