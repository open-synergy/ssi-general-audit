# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbdcdfc5ODetail(models.Model):
    _name = "general_audit_ws_bdcdfc5.detail"
    _description = "Worksheet bdcdfc5 - Detail"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_bdcdfc5",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    understanding_result = fields.Text(
        string="Understanding Result",
        required=True,
    )
    impact_to_financial_report = fields.Text(
        string="Impact To Financial Report",
        required=True,
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_bdcdfc5_detail_2_account_type",
        column1="detail_id",
        column2="type_id",
        required=True,
    )
