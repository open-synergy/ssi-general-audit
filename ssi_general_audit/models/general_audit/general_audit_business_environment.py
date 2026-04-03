# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditBusinessEnvironment(models.Model):
    """
    Lingkungan Bisnis Audit (Business Environment).

    Master data yang mengklasifikasikan lingkungan bisnis klien yang diaudit
    (mis. manufaktur, jasa, perdagangan, keuangan). Digunakan dalam proses
    pemahaman entitas dan lingkungannya sesuai ISA 315 / SA 315 (Identifying
    and assessing the risk of material misstatement).
    """

    _name = "general_audit_business_environment"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Business Environment"
    # No field updates required
