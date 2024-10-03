# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSAE11F7EDetail(models.Model):
    _name = "general_audit_ws_ae11f7e.expert"
    _description = "Worksheet ae11f7e - Expert"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae11f7e",
        required=True,
        ondelete="cascade",
    )
    general_audit_id = fields.Many2one(
        related="worksheet_id.general_audit_id",
        store=True,
    )
    name = fields.Char(
        string="Expert Name",
        required=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="general_audit_expert_type",
        required=True,
    )
    documentation = fields.Text(
        string="Documentation",
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_ae11f7e_expert_2_account_type",
        column1="detail_id",
        column2="type_id",
        required=True,
    )
    standard_detail_ids = fields.Many2many(
        string="Standard Details",
        comodel_name="general_audit.standard_detail",
        relation="rel_general_audit_ws_ae11f7e_expert_2_standard_detail",
        column1="expert_id",
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
