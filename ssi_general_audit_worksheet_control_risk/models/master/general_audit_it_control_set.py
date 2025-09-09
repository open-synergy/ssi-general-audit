# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditITControlSet(models.Model):
    _name = "general_audit_it_control_set"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit IT Control Set"

    it_control_indicator_ids = fields.Many2many(
        string="General Control Indicators",
        comodel_name="general_audit_it_control_indicator",
        relation="rel_general_audit_it_control_set_2_indicator",
        column1="set_id",
        column2="indicator_id",
    )
    it_control_ids = fields.Many2many(
        string="General Controls",
        comodel_name="general_audit_it_control",
        compute="_compute_it_control_ids",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "it_control_indicator_ids",
    )
    def _compute_it_control_ids(self):
        for record in self:
            result = []
            if record.it_control_indicator_ids:
                result = record.mapped("it_control_indicator_ids.control_id").ids
            record.it_control_ids = result
