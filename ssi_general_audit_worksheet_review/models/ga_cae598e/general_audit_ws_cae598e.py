# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWScae598e(models.Model):
    _name = "general_audit_ws_cae598e"
    _description = "Audit Evidence Evaluation Detail (cae598e)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_review." "worksheet_type_cae598e"

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_cae598e.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
    )

    def action_populate(self):
        for record in self.sudo():
            record._populate()

    def _populate(self):
        Detail = self.env["general_audit_ws_cae598e.detail"]
        Worksheet = self.env["general_audit_ws_bcc0d76.detail"]

        worksheets = Worksheet.search(
            [
                ("worksheet_id.general_audit_id", "=", self.general_audit_id.id),
            ]
        )
        mapping = {chk.detail_id.id: chk for chk in self.detail_ids}

        for ws in worksheets:
            if ws.id not in mapping:
                Detail.create(
                    {
                        "worksheet_id": self.id,
                        "detail_id": ws.id,
                    }
                )

        worksheet_ids = set(worksheets.ids)
        for chk in self.detail_ids:
            if chk.detail_id.id not in worksheet_ids:
                chk.unlink()

    @ssi_decorator.post_open_action()
    def _10_populate_data(self):
        self.ensure_one()
        self.action_populate()
