# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSC0E0EEC(models.Model):
    _name = "general_audit_ws_c0e0eec"
    _description = "Fraud Factor Analysis (c0e0eec)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_c0e0eec"
    )

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_c0e0eec.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @ssi_decorator.post_open_action()
    def _01_reload_item(self):
        self.ensure_one()
        self.detail_ids.unlink()
        Indicator = self.env["general_audit_fraud_factor_indicator"]
        Detail = self.env["general_audit_ws_c0e0eec.detail"]
        for indicator in Indicator.search([]):
            data = {
                "indicator_id": indicator.id,
                "worksheet_id": self.id,
            }
            Detail.create(data)
