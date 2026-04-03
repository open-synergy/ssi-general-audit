# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSbcc0d76(models.Model):
    """
    WS: Audit Quality Review (bcc0d76) — ISA 220 / SA 220.

    Provides a **consolidated quality review summary** for all main worksheets
    included in the engagement.  The reviewer (typically the Engagement
    Partner or Manager) assesses whether each worksheet meets quality
    standards before the audit opinion is issued.

    For each main worksheet the detail line captures:

    * The **state** of the worksheet (Draft / Open / Confirmed / Done).
    * The worksheet's **conclusion** and **review notes**.
    * A reviewer-assigned **review result** (e.g., Satisfactory / Needs
      Improvement / Unsatisfactory).
    * Any **quality issues** identified and the required follow-up actions.

    Use ``action_populate`` to auto-populate detail lines from all worksheets
    where ``parent_type_id.main_worksheet = True``; the method avoids
    duplicates and creates only one line per worksheet type.

    The detail lines from this worksheet feed the Audit Evidence Evaluation
    worksheet (``general_audit_ws_cae598e``).
    """

    _name = "general_audit_ws_bcc0d76"
    _description = "Audit Quality (bcc0d76)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_review." "worksheet_type_bcc0d76"

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_bcc0d76.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Review details generated for each main worksheet under this audit. "
            "Records are populated automatically and kept in sync with the source worksheets."
        ),
    )

    def action_populate(self):
        for record in self.sudo():
            record._populate()

    def _populate(self):
        self.ensure_one()
        Detail = self.env["general_audit_ws_bcc0d76.detail"]
        Worksheet = self.env["general_audit_worksheet"]

        # Ambil semua worksheet yang terkait dengan general audit
        worksheets = Worksheet.search([("parent_type_id.main_worksheet", "=", True)])

        # Mapping existing detail untuk mencegah duplikasi create
        mapping = {chk.general_worksheet_id.id: chk for chk in self.detail_ids}

        # --- Tambahan logika untuk hanya ambil satu per type ---
        # Gunakan dict agar otomatis hanya menyimpan satu per type
        unique_by_type = {}
        for ws in worksheets:
            if ws.parent_type_id.id not in unique_by_type:
                unique_by_type[ws.parent_type_id.id] = ws

        # Gunakan hanya satu record per type
        unique_worksheets = list(unique_by_type.values())

        # --- Create jika belum ada ---
        for ws in unique_worksheets:
            if ws.id not in mapping:
                Detail.create(
                    {
                        "worksheet_id": self.id,
                        "general_worksheet_id": ws.id,
                    }
                )

        # --- Hapus detail yang tidak ada lagi di worksheet ---
        worksheet_ids = {w.id for w in unique_worksheets}
        for chk in self.detail_ids:
            if chk.general_worksheet_id.id not in worksheet_ids:
                chk.unlink()
