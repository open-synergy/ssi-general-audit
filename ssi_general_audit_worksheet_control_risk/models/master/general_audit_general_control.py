# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditGeneralControl(models.Model):
    _name = "general_audit_general_control"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit General Control"
    _order = "category_id, sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Ordering of controls within the category.",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_general_control_category",
        required=True,
        help="Category to which this general control belongs.",
    )
    option_set_id = fields.Many2one(
        string="Option Set",
        comodel_name="checklist.option_set",
        required=True,
        ondelete="restrict",
        help="Option set that defines the allowed options for this item.",
    )
