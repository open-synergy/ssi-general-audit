# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ClientAccountMappingDetail(models.Model):
    """
    Baris Pemetaan Akun Klien.

    Satu baris dalam dokumen ``client_account_mapping`` yang menyatakan
    bahwa satu akun klien (``client_account``) dipetakan ke tipe akun
    standar tertentu (``client_account_type``). Field ``type_id`` dapat
    dikustomisasi per baris untuk mengakomodasi pemetaan yang lebih
    spesifik dari default tipe akun.
    """

    _name = "client_account_mapping.detail"
    _description = "Account Mapping Detail"
    _order = "mapping_id, type_id, account_id, id"

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
        compute_sudo=True,
        store=True,
        help="Sequence taken from the client account for ordering.",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="client_account",
        required=True,
        ondelete="restrict",
        help="Client account being mapped to a standard type.",
    )
    code = fields.Char(
        string="Code",
        related="account_id.code",
        compute_sudo=True,
        help="Client account code.",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="client_account_type",
        related="account_id.type_id",
        compute_sudo=True,
        store=True,
        readonly=False,
        help="Standard account type mapped to this client account.",
    )
    normal_balance = fields.Selection(
        string="Normal Balance",
        related="type_id.normal_balance",
        compute_sudo=True,
        help="Normal balance derived from the mapped type.",
    )
