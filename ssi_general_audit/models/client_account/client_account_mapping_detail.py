# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ClientAccountMappingDetail(models.Model):
    _name = "client_account_mapping.detail"
    _description = "Account Mapping Detail"

    mapping_id = fields.Many2one(
        string="# Mapping",
        comodel_name="client_account_mapping",
        required=True,
        ondelete="cascade",
        help="Parent client account mapping document.",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="account_id.sequence",
        help="Sequence taken from the client account for ordering.",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="client_account",
        required=True,
        help="Client account being mapped to a standard type.",
    )
    code = fields.Char(
        string="Code",
        related="account_id.code",
        help="Client account code.",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="client_account_type",
        related="account_id.type_id",
        store=True,
        readonly=False,
        help="Standard account type mapped to this client account.",
    )
    normal_balance = fields.Selection(
        string="Normal Balance",
        related="type_id.normal_balance",
        help="Normal balance derived from the mapped type.",
    )
