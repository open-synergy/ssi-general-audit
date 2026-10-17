# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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

    @api.constrains("mapping_id", "account_id")
    def _check_duplicate_account(self):
        """Refuse a second line with the same account code in one mapping.

        Two lines count as duplicates when their accounts share a code,
        which covers the same account added twice and an account of
        another client that carries the same code.

        :raises ValidationError: when another line of the same mapping
            has an account with the same code
        """
        for record in self:
            code = record.account_id.code
            if not code:
                continue
            criteria = [
                ("mapping_id", "=", record.mapping_id.id),
                ("account_id.code", "=", code),
                ("id", "!=", record.id),
            ]
            if self.search_count(criteria) > 0:
                error_message = """
                Context: Add account to client account mapping
                Database ID: %s
                Problem: Account code %s is already in this mapping
                Solution: Remove the duplicate line or pick another account
                """ % (
                    record.mapping_id.id,
                    code,
                )
                raise ValidationError(_(error_message))
