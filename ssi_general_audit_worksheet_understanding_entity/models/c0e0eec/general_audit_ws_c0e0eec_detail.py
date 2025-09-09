# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSC0E0EECDetail(models.Model):
    _name = "general_audit_ws_c0e0eec.detail"
    _description = "Worksheet c0e0eec - Detail"
    _order = "worksheet_id, category_id, factor_id, indicator_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_c0e0eec",
        required=True,
        ondelete="cascade",
    )
    indicator_id = fields.Many2one(
        string="Indicator",
        comodel_name="general_audit_fraud_factor_indicator",
        required=True,
    )
    factor_id = fields.Many2one(
        related="indicator_id.factor_id",
        store=True,
    )
    category_id = fields.Many2one(
        related="indicator_id.factor_id.category_id",
        store=True,
    )
    tcgw = fields.Text(
        string="TCGW",
    )
    management = fields.Text(
        string="Management",
    )
    other = fields.Text(
        string="Other",
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_c0e0eec_detail_2_account_type",
        column1="detail_id",
        column2="type_id",
        required=True,
    )
    standard_detail_ids = fields.Many2many(
        string="Standard Details",
        comodel_name="general_audit.standard_detail",
        relation="rel_general_audit_ws_c0e0eec_detail_2_standard_detail",
        column1="detail_id",
        column2="standard_detail_id",
        compute="_compute_standard_detail_ids",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "related_account_type_ids",
    )
    def _compute_standard_detail_ids(self):
        StandardDetail = self.env["general_audit.standard_detail"]
        for record in self:
            result = []
            general_audit = record.worksheet_id.general_audit_id
            criteria = [
                ("general_audit_id", "=", general_audit.id),
                ("type_id", "in", record.related_account_type_ids.ids),
            ]
            standard_details = StandardDetail.search(criteria)
            if len(standard_details) > 0:
                result = standard_details.ids
            record.standard_detail_ids = result
