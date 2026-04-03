# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ClientAccountType(models.Model):
    """
    Tipe Akun Standar Klien.

    Master data yang mendefinisikan klasifikasi akun standar yang digunakan
    dalam audit (mis. Kas & Setara Kas, Piutang Usaha, Persediaan, Utang
    Usaha). Setiap tipe akun:
    - diklasifikasikan ke dalam satu ``client_account_group``
    - memiliki saldo normal (debit atau kredit)
    - dapat memiliki kode Python untuk menghitung nilai audit tertentu
    - dapat dikaitkan dengan item prosedur analitis (ISA 520 / SA 520)

    Digunakan sebagai standar pemetaan antara akun klien dan tipe akun
    yang ditetapkan KAP untuk keperluan analisis dan pelaporan audit.
    """

    _name = "client_account_type"
    _inherit = ["mixin.master_data"]
    _description = "Client Account Type"
    _order = "sequence, id"
    _show_code_on_display_name = False

    group_id = fields.Many2one(
        string="Client Account Group",
        comodel_name="client_account_group",
        required=True,
        ondelete="restrict",
        help="Account group that this type belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Ordering of the account type.",
    )
    normal_balance = fields.Selection(
        string="Normal Balance",
        selection=[
            ("dr", "Debit"),
            ("cr", "Credit"),
        ],
        required=True,
        default="dr",
        help="Default normal balance for accounts of this type.",
    )
    analytic_procedure_computation_item_id = fields.Many2one(
        string="Computation Item for Analytic Procedure",
        comodel_name="trial_balance_computation_item",
        ondelete="restrict",
        help="Computation item used to calculate analytic procedure for this type.",
    )
    python_code = fields.Text(
        string="Python Code",
        required=True,
        default="result = document.balance",
        help=(
            "Python code to compute the balance for this type. The variable "
            "'document' refers to the trial balance line."
        ),
    )
