# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ChecklistOptionSet(models.Model):
    """
    Set Opsi Checklist.

    Master data yang mendefinisikan kumpulan opsi jawaban (``checklist.option``)
    yang dapat digunakan bersama-sama dalam sebuah checklist (mis. set
    "Ya/Tidak", set "Ya/Tidak/Tidak Berlaku", set "Sesuai/Tidak Sesuai/Pengecualian").
    Setiap item checklist (``mixin.checklist.item``) merujuk ke satu option_set
    untuk menentukan pilihan jawaban yang tersedia.
    """

    _name = "checklist.option_set"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Option Sets for Checklist"

    code = fields.Char(
        default="/",
        help="Unique code for the option set. Use '/' to auto-generate.",
    )
    option_ids = fields.Many2many(
        string="Options",
        comodel_name="checklist.option",
        relation="rel_checklist_option_set_2_option",
        column1="set_id",
        column2="option_id",
        help="Options included in this set and available to referencing items.",
    )
