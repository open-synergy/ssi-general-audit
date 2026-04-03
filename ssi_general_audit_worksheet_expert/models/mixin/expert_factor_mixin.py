# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class MixinExpertFactor(models.AbstractModel):
    """
    Abstract base class for Expert Evaluation Factors.

    Provides the common fields for a master-data evaluation factor used in
    expert worksheets.  Concrete models (``general_audit_ws_bab9d32.factor``
    for Auditor's Expert and ``general_audit_ws_cda3a68.factor`` for
    Management's Expert) inherit this mixin.  Each factor belongs to one
    category and appears as one evaluation line on the worksheet.

    Factors are translatable so their names can be adapted to local language
    requirements.
    """

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
