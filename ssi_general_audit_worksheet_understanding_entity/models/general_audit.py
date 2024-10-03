# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


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
