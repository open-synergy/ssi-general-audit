# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAudit(models.Model):
    _name = "general_audit"
    _description = "General Audit"
    _inherit = [
        "general_audit",
    ]

    business_cycle_ids = fields.Many2many(
        string="Business Cycles",
        comodel_name="client_business_process",
        relation="rel_general_audit_2_business_cycle",
        column1="general_audit_id",
        column2="business_process_id",
    )
    other_report_ids = fields.Many2many(
        string="Other Reports",
        comodel_name="general_audit_other_report",
        relation="rel_general_audit_2_other_report",
        column1="general_audit_id",
        column2="other_report_id",
    )
    ws_ae11f7e_expert_ids = fields.One2many(
        string="WS AE11F7E Details",
        comodel_name="general_audit_ws_ae11f7e.expert",
        inverse_name="general_audit_id",
    )
    expert_type_ids = fields.Many2many(
        string="Expert Needed",
        comodel_name="general_audit_expert_type",
        relation="rel_general_audit_2_expert_type",
        column1="general_audit_id",
        column2="expert_type_id",
        compute="_compute_expert_type_ids",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "ws_ae11f7e_expert_ids",
        "ws_ae11f7e_expert_ids.type_id",
    )
    def _compute_expert_type_ids(self):
        for record in self:
            result = []
            if record.ws_ae11f7e_expert_ids:
                result = record.mapped("ws_ae11f7e_expert_ids.type_id.id")
            record.expert_type_ids = result
