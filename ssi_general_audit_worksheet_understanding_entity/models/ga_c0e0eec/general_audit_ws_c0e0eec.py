# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


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
        help=(
            "Fraud indicator assessment lines for this worksheet. "
            "Re-loaded from master indicators when the worksheet is opened."
        ),
    )

    def action_populate(self):
        for record in self:
            record._populate()

    def _populate(self):
        self.ensure_one()
        Detail = self.env["general_audit_ws_c0e0eec.detail"]
        Indicator = self.env["general_audit_fraud_factor_indicator"]

        indicator_ids = Indicator.search([])
        mapping = {chk.indicator_id.id: chk for chk in self.detail_ids}

        for indicator in indicator_ids:
            if indicator.id not in mapping:
                Detail.create(
                    {
                        "worksheet_id": self.id,
                        "indicator_id": indicator.id,
                    }
                )

        for chk in self.detail_ids:
            if chk.indicator_id.id not in indicator_ids.ids:
                chk.unlink()
