# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditITControlIndicator(models.Model):
    _name = "general_audit_it_control_indicator"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit General Control Indicator"
    _order = "category_id, control_id, sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Ordering of indicators under the same IT control.",
    )
    control_id = fields.Many2one(
        string="Control",
        comodel_name="general_audit_it_control",
        required=True,
        help="IT control this indicator evaluates.",
    )
    category_id = fields.Many2one(
        related="control_id.category_id",
        store=True,
        help="Auto-filled category derived from the selected IT control.",
    )
    option_set_id = fields.Many2one(
        string="Option Set",
        comodel_name="checklist.option_set",
        required=True,
        ondelete="restrict",
        help="Option set that defines the allowed options for this item.",
    )
    procedure = fields.Char()
