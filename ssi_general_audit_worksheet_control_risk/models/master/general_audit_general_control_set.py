# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditGeneralControlSet(models.Model):
    _name = "general_audit_general_control_set"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit General Control Set"

    general_control_indicator_ids = fields.Many2many(
        string="General Control Indicators",
        comodel_name="general_audit_general_control_indicator",
        relation="rel_general_audit_general_control_set_2_indicator",
        column1="set_id",
        column2="indicator_id",
    )
    general_control_ids = fields.Many2many(
        string="General Controls",
        comodel_name="general_audit_general_control",
        compute="_compute_general_control_ids",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "general_control_indicator_ids",
    )
    def _compute_general_control_ids(self):
        for record in self:
            result = []
            if record.general_control_indicator_ids:
                result = record.mapped("general_control_indicator_ids.control_id").ids
            record.general_control_ids = result
