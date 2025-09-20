# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ChecklistOptionSet(models.Model):
    _name = "checklist.option_set"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Option Sets for Checklist"

    code = fields.Char(
        default="/",
    )
    option_ids = fields.Many2many(
        string="Options",
        comodel_name="checklist.option",
        relation="rel_checklist_option_set_2_option",
        column1="set_id",
        column2="option_id",
    )
