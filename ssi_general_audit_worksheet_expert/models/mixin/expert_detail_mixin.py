# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class MixinExpertDetail(models.AbstractModel):
    _name = "mixin.expert.detail"
    _description = "Abstract Base for Expert Details"
    _abstract = True
    _order = "sequence, category_id, id"

    expert_id = fields.Many2one(
        string="# Expert",
        comodel_name="mixin.expert",
        required=True,
        ondelete="cascade",
        help="Document (Expert) that owns this expert line.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help="Ordering number controlling the display order (lower comes first).",
    )
    factor_id = fields.Many2one(
        string="# Factor",
        comodel_name="mixin.expert.factor",
        required=True,
        ondelete="restrict",
        help="Master expert factor this line refers to.",
    )
    factor_name = fields.Char(
        string="Factor",
        related="factor_id.name",
    )
    category_id = fields.Many2one(
        related="factor_id.category_id",
    )
    explanation = fields.Text(
        string="Explanation/Reference",
    )
