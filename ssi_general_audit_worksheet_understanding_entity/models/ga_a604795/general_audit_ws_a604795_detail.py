# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSA604795Detail(models.Model):
    """Transaction class detail line within the Business Cycle Summaries worksheet.

    Represents a single class of transaction within the business cycle being
    documented. Per ISA 315 (Revised), auditors must understand classes of
    transactions, account balances, and disclosures, including the related
    business functions and documents that flow through the cycle.

    Each detail line captures:
    - The class of transaction (e.g., sales, purchases, payroll)
    - Business functions driving the transaction class
    - Related standard account types affected
    """

    _name = "general_audit_ws_a604795.detail"
    _description = "Worksheet a604795 - Detail"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_a604795",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This detail will be removed if the worksheet is deleted."
        ),
    )
    class_transaction_id = fields.Many2one(
        string="Class of Transaction",
        comodel_name="general_audit_class_transaction",
        required=True,
        ondelete="restrict",
        help=(
            "Class of transaction in scope for this detail. "
            "Related records cannot be deleted due to 'restrict' policy."
        ),
    )
    business_function_ids = fields.One2many(
        string="Business Functions",
        comodel_name="general_audit_ws_a604795.business_function",
        inverse_name="detail_id",
        help="Business functions associated with this class of transaction.",
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_a604795_detail_2_account_type",
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
        relation="rel_general_audit_ws_a604795_detail_2_standard_detail",
        column1="detail_id",
        column2="standard_detail_id",
        compute="_compute_standard_detail_ids",
        store=True,
        compute_sudo=True,
        help=(
            "Standard details automatically linked based on the selected account types "
            "and the worksheet's General Audit."
        ),
    )
    review = fields.Text(
        string="Review",
        help="Reviewer notes or comments regarding this class of transaction.",
    )
    need_unannounced_audit = fields.Boolean(
        string="Need Unannounced Audit",
        default=False,
        help="Indicates if an unannounced audit is required for this class of transaction.",
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
