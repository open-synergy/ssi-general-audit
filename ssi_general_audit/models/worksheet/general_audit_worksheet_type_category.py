# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWorksheetTypeCategory(models.Model):
    """
    Kategori Tipe Worksheet Audit.

    Master data untuk mengelompokkan tipe-tipe worksheet ke dalam kategori
    yang mencerminkan fase audit (mis. Perencanaan / Planning, Pelaksanaan /
    Fieldwork, Pelaporan / Reporting). Digunakan untuk navigasi dan pengelompokan
    tampilan worksheet dalam dashboard audit.
    """

    _name = "general_audit_worksheet_type_category"
    _inherit = ["mixin.master_data", "image.mixin"]
    _description = "General Audit Worksheet Type Category"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Ordering of the worksheet type category in lists and reports.",
    )
