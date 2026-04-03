# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditEvidence(models.Model):
    """
    Tipe Bukti Audit (Audit Evidence).

    Master data yang mendefinisikan jenis-jenis bukti audit yang dapat
    diperoleh auditor, seperti inspeksi (inspection), konfirmasi
    (confirmation), observasi (observation), tanya-jawab (inquiry),
    komputasi ulang (recomputation), dan reperformansi (reperformance).
    Mengacu pada ISA 500 / SA 500 (Audit Evidence).
    """

    _name = "general_audit_evidence"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Evidence"

    code = fields.Char(
        default="/",
        help="Unique short code for the evidence. Use '/' to auto-generate.",
    )
