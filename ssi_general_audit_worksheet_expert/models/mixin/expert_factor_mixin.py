# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class MixinExpertFactor(models.AbstractModel):
    _name = "mixin.expert.factor"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Abstract Base for Expert Factors"
    _abstract = True
    _order = "sequence, id"

    name = fields.Char(
        translate=True,
        help="Display name of the expert factor shown on forms and reports.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help="Ordering number controlling the display order (lower comes first).",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="mixin.expert.category",
        required=True,
        help="Expert Category.",
    )
