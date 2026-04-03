# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ChecklistOption(models.Model):
    """
    Opsi Jawaban Checklist.

    Master data yang merepresentasikan satu pilihan jawaban yang dapat
    dipilih dalam checklist audit (mis. "Ya", "Tidak", "Tidak Berlaku",
    "Dalam Proses"). Opsi-opsi ini dikelompokkan dalam ``checklist.option_set``
    dan ditampilkan sebagai pilihan pada setiap baris checklist worksheet.
    """

    _name = "checklist.option"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Available options for a custom property"

    code = fields.Char(
        default="/",
        help="Unique short code for the option (e.g., Yes/No/N/A). Use '/' to auto-generate.",
    )
