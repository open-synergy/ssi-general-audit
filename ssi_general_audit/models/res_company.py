# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ResCompany(models.Model):
    """
    Extension Model Perusahaan (KAP) untuk Konfigurasi Audit.

    Menambahkan konfigurasi default pada ``res.company`` untuk keperluan
    komputasi materialitas (ISA 320 / SA 320). KAP dapat mengonfigurasi:
    - ``ta_computation_item_id``: item komputasi untuk Total Aset, yang
      digunakan sebagai basis materialitas untuk entitas yang berfokus pada
      aset (mis. perbankan, perusahaan properti)
    - ``tr_computation_item_id``: item komputasi untuk Total Pendapatan,
      yang digunakan sebagai basis materialitas untuk entitas yang berfokus
      pada pendapatan (mis. perusahaan manufaktur, perdagangan, jasa)
    """

    _inherit = "res.company"
    _ta_computation_item_id = (
        "ssi_general_audit." "trial_balance_computation_item_1_d0b0cb3e"
    )
    _tr_computation_item_id = (
        "ssi_general_audit." "trial_balance_computation_item_5_2a8e8641"
    )

    @api.model
    def _default_ta_computation_item_id(self):
        # ✅ hindari env.ref saat registry belum siap (saat instalasi awal)
        if not self.env.registry.ready:
            return False
        try:
            return self.env.ref(
                self._ta_computation_item_id,
                raise_if_not_found=False,
            )
        except ValueError:
            return False

    ta_computation_item_id = fields.Many2one(
        string="Total Asset Computation",
        comodel_name="trial_balance_computation_item",
        default=lambda self: self._default_ta_computation_item_id(),
        ondelete="restrict",
        help="Default trial balance computation item used to derive Total Assets.",
    )

    @api.model
    def _default_tr_computation_item_id(self):
        if not self.env.registry.ready:
            return False
        try:
            return self.env.ref(
                self._tr_computation_item_id,
                raise_if_not_found=False,
            )
        except ValueError:
            return False

    tr_computation_item_id = fields.Many2one(
        string="Total Revenue Computation",
        comodel_name="trial_balance_computation_item",
        default=lambda self: self._default_tr_computation_item_id(),
        ondelete="restrict",
        help="Default trial balance computation item used to derive Total Revenue.",
    )
