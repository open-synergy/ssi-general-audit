# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ClientAccountGroup(models.Model):
    _name = "client_account_group"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Client Account Group"
    _order = "sequence, id"
    _show_code_on_display_name = True

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Ordering of the account group in lists and reports.",
    )
    normal_balance = fields.Selection(
        string="Normal Balance",
        selection=[
            ("dr", "Debit"),
            ("cr", "Credit"),
        ],
        required=True,
        default="dr",
        help="Default normal balance for accounts under this group.",
    )
