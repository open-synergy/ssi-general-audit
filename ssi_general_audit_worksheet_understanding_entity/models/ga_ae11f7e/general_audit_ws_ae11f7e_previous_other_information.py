# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSAE11F7EPreviousOtherInformation(models.Model):
    _name = "general_audit_ws_ae11f7e.previous_other_information"
    _description = "Worksheet ae11f7e - Previous Significant Other Information"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae11f7e",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This entry will be removed if the worksheet is deleted."
        ),
    )
    name = fields.Text(
        string="Summary",
        required=True,
        help="Summary of significant other information from prior periods.",
    )
    documentation = fields.Text(
        string="Documentation",
        help="Narrative explanation, sources, or references for the information.",
    )
    attachment_ids = fields.Many2many(
        string="Attachments",
        comodel_name="ir.attachment",
        relation="rel_ga_ae11f7e_previous_other_2_attachment",
        column1="ae11f7e_previous_other_id",
        column2="attachment_id",
        domain="[('res_model', '=', 'general_audit_ws_ae11f7e'), "
        "('res_id', '=', worksheet_id)]",
        help=(
            "Files attached to this worksheet record. Only attachments whose res_model is "
            "'general_audit_ws_ae11f7e' and res_id equals this worksheet can be selected."
        ),
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_ae11f7e_prev_other_2_account_type",
        column1="prev_other_id",
        column2="type_id",
        required=True,
        help=(
            "Standard account types related to this item. Used to link the entry to "
            "relevant accounts."
        ),
    )
    standard_detail_ids = fields.Many2many(
        string="Standard Details",
        comodel_name="general_audit.standard_detail",
        relation="rel_general_audit_ws_ae11f7e_prev_other_2_standard_detail",
        column1="prev_other_id",
        column2="standard_detail_id",
        compute="_compute_standard_detail_ids",
        store=True,
        compute_sudo=True,
        help=(
            "Standard details automatically linked based on the selected account types "
            "and the worksheet's General Audit."
        ),
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
