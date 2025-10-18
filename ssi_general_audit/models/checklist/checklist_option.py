# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ChecklistOption(models.Model):
    _name = "checklist.option"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Available options for a custom property"

    code = fields.Char(
        default="/",
        help="Unique short code for the option (e.g., Yes/No/N/A). Use '/' to auto-generate.",
    )
