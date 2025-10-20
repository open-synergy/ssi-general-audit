# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSa8f4d88(models.Model):
    _name = "general_audit_ws_a8f4d88"
    _description = "Accounting Estimation (a8f4d88)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_specific_procedure." "worksheet_type_a8f4d88"
    )

    allowed_account_type_ids = fields.Many2many(
        comodel_name="client_account_type",
        string="Allowed Account Types",
        help="Account types that can be selected",
        compute="_compute_allowed_account_type_ids",
        store=False,
    )
    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_a8f4d88.detail",
        inverse_name="worksheet_id",
        string="Details",
        readonly=True,
        states={"draft": [("readonly", False)], "open": [("readonly", False)]},
    )

    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_account_type_ids(self):
        for record in self:
            record.allowed_account_type_ids = self.env["client_account_type"]
            if record.general_audit_id:
                record.allowed_account_type_ids = record.general_audit_id.mapped(
                    "standard_detail_ids.type_id"
                )
