# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSf5a3ceeDetail(models.Model):
    _name = "general_audit_ws_f5a3cee.detail"
    _description = "Data Collection (f5a3cee) - Details"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_f5a3cee",
        required=True,
        ondelete="cascade",
    )
    account_client_type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        required=True,
    )
    date = fields.Date(
        string="Date",
        required=False,
    )
    attachment_ids = fields.Many2many(
        string="Attachments",
        comodel_name="ir.attachment",
        relation="rel_ga_f5a3cee_detail_2_attachment",
        column1="f5a3cee_detail_id",
        column2="attachment_id",
        domain="[('res_model', '=', 'general_audit_ws_f5a3cee'), "
        "('res_id', '=', worksheet_id)]",
    )
    complete_ok = fields.Boolean(
        string="Completed",
        default=False,
    )
    state = fields.Selection(
        related="worksheet_id.state",
    )
