# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class MixinChecklistItem(models.AbstractModel):
    """
    Abstract Base untuk Master Item Checklist.

    Model abstrak yang menjadi landasan bagi model-model master item
    checklist pada masing-masing worksheet. Setiap item mendefinisikan
    satu pertanyaan atau titik kontrol (control point) beserta set opsi
    jawaban yang tersedia. Model konkret yang mewarisi mixin ini dibuat
    secara terpisah per tipe worksheet (mis. item checklist acceptance &
    continuance, item checklist engagement letter).
    """

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
        ondelete="restrict",
        help="Option set that defines the allowed options for this item.",
    )
