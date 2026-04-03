# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ClientBusinessProcess(models.Model):
    """
    Siklus Bisnis Klien (Business Process / Business Cycle).

    Master data yang mendefinisikan siklus-siklus bisnis utama klien yang
    diaudit (mis. Siklus Pendapatan, Siklus Pembelian, Siklus Penggajian,
    Siklus Produksi). Digunakan dalam proses pemahaman entitas dan
    lingkungannya (ISA 315 / SA 315) serta penilaian risiko inherent
    per siklus bisnis dalam risk assessment worksheet.
    """

    _name = "client_business_process"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Client Business Cycle"
