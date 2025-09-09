# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ClientBusinessProcess(models.Model):
    _name = "client_business_process"
    _inherit = [
        "client_business_process",
    ]

    key_internal_control_ids = fields.Many2many(
        string="Business Cycle Key Internal Controls",
        comodel_name="general_audit_key_internal_control",
        relation="rel_key_internal_control_2_business_cycle",
        column1="business_cycle_id",
        column2="key_internal_control_id",
    )
