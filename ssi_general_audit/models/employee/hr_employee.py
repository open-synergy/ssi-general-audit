# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class HrEmployee(models.Model):
    """
    Extension Model Karyawan untuk Kebutuhan Audit.

    Menambahkan flag ``audit_ok`` ke model ``hr.employee`` standar Odoo
    untuk menandai karyawan yang memiliki kualifikasi/wewenang untuk
    melakukan pekerjaan audit. Flag ini digunakan sebagai filter saat
    memilih anggota tim audit dalam engagement general audit.
    """

    _inherit = "hr.employee"

    audit_ok = fields.Boolean(
        string="Can Audit",
        default=False,
        help="If checked, this employee can audit.",
    )
