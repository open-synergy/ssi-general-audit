# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class MixinChecklistItem(models.AbstractModel):
    _name = "mixin.checklist.item"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Abstract Base for Checklist Items"
    _abstract = True
    _order = "sequence, id"

    name = fields.Char(
        translate=True,
        help="Display name of the checklist item shown on forms and reports.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help="Ordering number controlling the display order (lower comes first).",
    )
    option_set_id = fields.Many2one(
        string="Option Set",
        comodel_name="checklist.option_set",
        required=True,
        help="Option set that defines the allowed options for this item.",
    )
