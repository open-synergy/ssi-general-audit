# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class MixinChecklistValue(models.AbstractModel):
    _name = "mixin.checklist.value"
    _description = "Abstract Base for Checklist"

    worksheet_id = fields.Many2one(
        string="Worksheet",
        comodel_name="mixin.checklist",
        required=True,
        ondelete="cascade",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="mixin.checklist.item",
        required=True,
        ondelete="restrict",
    )
    allowed_option_ids = fields.Many2many(
        string="Options", related="item_id.option_set_id.option_ids"
    )
    option_id = fields.Many2one(
        string="Option",
        comodel_name="checklist.option",
        required=False,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="item_id.sequence",
        store=True,
        readonly=False,
    )
    checklist_ok = fields.Boolean(
        string="Passed?",
        required=True,
        default=True,
    )
