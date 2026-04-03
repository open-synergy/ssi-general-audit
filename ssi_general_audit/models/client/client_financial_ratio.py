# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ClientFinancialRatio(models.Model):
    """
    Rasio Keuangan Klien (Financial Ratio).

    Master data yang mendefinisikan formula (kode Python) untuk menghitung
    rasio keuangan klien yang digunakan dalam prosedur analitis
    (ISA 520 / SA 520). Setiap rasio dikategorikan ke dalam:
    - ``liquidity``     : likuiditas (Current Ratio, Quick Ratio)
    - ``activity``      : aktivitas (Receivable/Inventory Turnover)
    - ``solvency``      : solvabilitas (Debt to Equity, Interest Coverage)
    - ``profitability``  : profitabilitas (ROA, ROE, GPM, NPM)

    Hasil komputasi rasio ini dibandingkan antara periode interim,
    ekstrapolasi, dan periode sebelumnya untuk mengidentifikasi
    fluktuasi yang memerlukan penyelidikan lebih lanjut.
    """

    _name = "client_financial_ratio"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Client Financial Ratio"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Ordering number for displaying ratios.",
    )
    python_code = fields.Text(
        string="Python Code",
        required=True,
        default="result_interim = result_extrapolation = result_previous = 0.0",
        help=(
            "Python code that computes ratio values. Set variables: "
            "result_interim, result_extrapolation, and result_previous."
        ),
    )
    category = fields.Selection(
        string="Category",
        selection=[
            ("liquidity", "Liquidity Ratio"),
            ("activity", "Activity Ratio"),
            ("solvency", "Solvency Ratio"),
            ("profitability", "Profitability Ratio"),
        ],
        required=True,
        default="liquidity",
        help="Classification of the financial ratio for reporting.",
    )
