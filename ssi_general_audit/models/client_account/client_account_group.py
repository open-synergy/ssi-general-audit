# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ClientAccountGroup(models.Model):
    """
    Grup Akun Klien.

    Master data yang mengelompokkan tipe-tipe akun klien ke dalam kelompok
    akun yang lebih tinggi (mis. Aset Lancar, Aset Tidak Lancar, Liabilitas
    Jangka Pendek, Ekuitas, Pendapatan, Beban). Digunakan untuk penyajian
    laporan keuangan dan analisis material per kelompok akun dalam audit.
    """

    _name = "client_account_group"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Client Account Group"
    _order = "sequence, id"
    _show_code_on_display_name = False

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
    report_category = fields.Selection(
        string="Report Category",
        selection=[
            ("asset", "Asset"),
            ("liability", "Liability"),
            ("equity", "Equity"),
            ("profit_loss", "Profit & Loss"),
        ],
        required=False,
        help="Financial statement category of the accounts under this "
        "group. Used to summarise the impact of adjustment entries "
        "(AJE Summaries). Leave empty to exclude the group from the "
        "impact columns.",
    )
