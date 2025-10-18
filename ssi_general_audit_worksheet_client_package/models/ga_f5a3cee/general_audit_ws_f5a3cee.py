# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSf5a3cee(models.Model):
    _name = "general_audit_ws_f5a3cee"
    _description = "Data Collection (f5a3cee)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_client_package." "worksheet_type_f5a3cee"
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_f5a3cee.detail",
        inverse_name="worksheet_id",
        help=(
            "Detail lines automatically populated from the client's " "account mapping."
        ),
    )

    def _create_details_data(self, mapping):
        self.ensure_one()
        data = {
            "worksheet_id": self.id,
            "account_client_type_id": mapping.id,
        }
        return data

    def _update_details_data(self, mapping):
        self.ensure_one()
        data = {
            "account_client_type_id": mapping.id,
        }
        return data

    def action_populate_details(self):
        for record in self:
            record._create_details()

    def _create_details(self):
        self.ensure_one()
        Detail = self.env["general_audit_ws_f5a3cee.detail"]
        AccMapping = self.env["client_account_mapping"]

        criteria = [("partner_id", "=", self.partner_id.id)]

        acc_mapping_type_ids = AccMapping.search(criteria).mapped("detail_ids").type_id
        mapping = {chk.account_client_type_id.id: chk for chk in self.detail_ids}

        if acc_mapping_type_ids:
            for acc_type in acc_mapping_type_ids:
                if acc_type.id not in mapping:
                    Detail.create(self._create_details_data(acc_type))
                else:
                    mapping[acc_type.id].write(self._update_details_data(acc_type))

            for chk in self.detail_ids:
                if chk.account_client_type_id.id not in acc_mapping_type_ids.ids:
                    chk.unlink()
