# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditGeneralControlIndicator(models.Model):
    _name = "general_audit_general_control_indicator"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit General Control Indicator"
    _order = "category_id, control_id, sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    control_id = fields.Many2one(
        string="Factor",
        comodel_name="general_audit_general_control",
        required=True,
    )
    category_id = fields.Many2one(
        related="control_id.category_id",
        store=True,
    )
