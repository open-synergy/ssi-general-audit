# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd66d87a(models.Model):
    _name = "general_audit_ws_d66d87a"
    _description = "Account Level ROMM (d66d87a)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_romm." "worksheet_type_d66d87a"

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_d66d87a.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Lines generated for each standard detail to capture assertion-level ROMM "
            "and planned responses at the account level."
        ),
    )

    def action_load_detail(self):
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        self.ensure_one()
        self.detail_ids.unlink()
        StandardDetail = self.env["general_audit.standard_detail"]
        Detail = self.env["general_audit_ws_d66d87a.detail"]
        for standard_detail in StandardDetail.search([]):
            data = {
                "worksheet_id": self.id,
                "standard_detail_id": standard_detail.id,
            }
            Detail.create(data)
