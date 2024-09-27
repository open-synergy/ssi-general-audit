# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSBA9B2F0(models.Model):
    _name = "general_audit_ws_ba9b2f0"
    _description = "Significant Account Internal Control (ba9b2f0)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_control_risk." "worksheet_type_ba9b2f0"

    account_type_id = fields.Many2one(
        string="Standard Account",
        comodel_name="client_account_type",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    significant_risk_account_type_ids = fields.Many2many(
        string="Significant Account Types",
        related="general_audit_id.significant_risk_account_type_ids",
        store=False,
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="general_audit.standard_detail",
        compute="_compute_standard_detail_id",
        store=True,
        compute_sudo=True,
    )

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_ba9b2f0.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "account_type_id",
    )
    def _compute_standard_detail_id(self):
        StandardDetail = self.env["general_audit.standard_detail"]
        for record in self:
            result = []
            general_audit = record.general_audit_id
            criteria = [
                ("general_audit_id", "=", general_audit.id),
                ("type_id", "=", record.account_type_id.id),
            ]
            standard_details = StandardDetail.search(criteria)
            if len(standard_details) > 0:
                result = standard_details[0]
            record.standard_detail_id = result
