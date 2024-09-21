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
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_general_control_category",
        required=True,
    )
