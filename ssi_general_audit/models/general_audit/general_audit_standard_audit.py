# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import models


class GeneralAuditStandardAudit(models.Model):
    """
    Standar Audit yang Berlaku (Audit Standard).

    Master data yang merepresentasikan standar audit yang dirujuk dalam
    prosedur audit, mis. ISA 200, ISA 315, SA 200, SA 500. Digunakan
    sebagai referensi untuk mendokumentasikan standar yang menjadi dasar
    setiap prosedur atau temuan audit (ISA 230 / SA 230 - Audit Documentation).
    """

    _name = "general_audit_standard_audit"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Standard Audit"
    # No field updates required
