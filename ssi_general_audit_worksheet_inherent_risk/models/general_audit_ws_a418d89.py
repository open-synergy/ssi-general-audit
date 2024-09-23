# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSA418D89(models.Model):
    _name = "general_audit_ws_a418d89"
    _description = "Account Level Inherent Risk (a418d89)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_inherent_risk." "worksheet_type_a418d89"

    # risk_material_missstatement = fields.Selection(
    #     string="Risk Material Misstatement",
    #     selection=[
    #         ("low", "Low"),
    #         ("medium", "Medium"),
    #         ("high", "High"),
    #     ],
    #     readonly=True,
    #     required=False,
    #     states={
    #         "open": [
    #             ("readonly", False),
    #         ],
    #     },
    # )
    # auditor_respons = fields.Text(
    #     string="Auditor Respons",
    #     readonly=True,
    #     states={
    #         "open": [
    #             ("readonly", False),
    #         ],
    #     },
    # )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_a418d89.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @ssi_decorator.post_open_action()
    def _01_compute_detail(self):
        self.detail_ids.unlink()
        Detail = self.env["general_audit_ws_a418d89.detail"]
        for detail in self.general_audit_id.standard_detail_ids:
            data = {
                "worksheet_id": self.id,
                "standard_detail_id": detail.id,
            }
            Detail.create(data)
