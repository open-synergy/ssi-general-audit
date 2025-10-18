# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSbdcdfc5ODetail(models.Model):
    _name = "general_audit_ws_bdcdfc5.detail"
    _description = "Worksheet bdcdfc5 - Detail"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_bdcdfc5",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This detail will be removed if the worksheet is deleted."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help="Ordering of this line within the worksheet.",
    )
    understanding_result = fields.Text(
        string="Understanding Result",
        required=True,
        help=(
            "Summary of the entity understanding obtained for this area, including key "
            "processes, risks, and controls identified."
        ),
    )
    impact_to_financial_report = fields.Text(
        string="Impact To Financial Report",
        required=True,
        help=(
            "Describe potential impacts on the financial statements, "
            "assertions affected, and audit implications."
        ),
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_bdcdfc5_detail_2_account_type",
        column1="detail_id",
        column2="type_id",
        required=True,
        help=(
            "Standard account types related to this detail. Used to link the understanding "
            "to relevant accounts."
        ),
    )
    standard_detail_ids = fields.Many2many(
        string="Standard Details",
        comodel_name="general_audit.standard_detail",
        relation="rel_general_audit_ws_bdcdfc5_detail_2_standard_detail",
        column1="detail_id",
        column2="standard_detail_id",
        compute="_compute_standard_detail_ids",
        store=True,
        compute_sudo=True,
        help=(
            "Standard details automatically linked based on the selected account types "
            "and the worksheet's general audit."
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
