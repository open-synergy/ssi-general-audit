# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ClientAccountType(models.Model):
    _name = "client_account_type"
    _inherit = ["client_account_type"]

    account_key_internal_control_ids = fields.Many2many(
        string="Significant Account Key Internal COntrols",
        comodel_name="general_audit_account_key_internal_control",
        relation="rel_account_key_internal_control_2_standard_account",
        column1="standard_account_id",
        column2="key_internal_control_id",
    )
