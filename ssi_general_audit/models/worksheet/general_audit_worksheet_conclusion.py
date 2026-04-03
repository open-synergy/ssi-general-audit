# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWorksheetConclusion(models.Model):
    """
    Kesimpulan Worksheet Audit.

    Master data yang mendefinisikan pilihan kesimpulan yang dapat dipilih
    auditor saat menyelesaikan sebuah worksheet (mis. "Bukti audit cukup
    diperoleh", "Terdapat keterbatasan ruang lingkup", "Risiko signifikan
    teridentifikasi"). Setiap kesimpulan terikat pada satu tipe worksheet
    tertentu (``type_id``) sesuai konteks prosedur audit yang dilakukan.
    """

    _name = "general_audit_worksheet_conclusion"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Worksheet Conclusion"
    _order = "type_id, sequence, code"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Ordering of the conclusion within its worksheet type.",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="general_audit_worksheet_type",
        required=True,
        ondelete="restrict",
        help="Worksheet type that this conclusion applies to.",
    )
