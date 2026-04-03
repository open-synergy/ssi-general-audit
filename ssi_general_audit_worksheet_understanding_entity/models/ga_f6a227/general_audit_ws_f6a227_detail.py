# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSf6a227Detail(models.Model):
    """Detail line for one step of the financial statement preparation process.

    Documents the auditor's understanding of a specific financial statement
    preparation step (e.g., journal entry processing, period-end close,
    consolidation). For each step the auditor captures the understanding
    result, control activities, audit relevancy, and potential misstatements.
    This information directly informs the test of controls and substantive
    procedures designed per ISA 330 / SA 330.
    """

    _name = "general_audit_ws_f6a227.detail"
    _description = "Worksheet f6a227 - Detail"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_f6a227",
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
        help="Ordering of this line; defaults to the selected step's sequence.",
    )
    step_id = fields.Many2one(
        string="Step",
        comodel_name="general_audit_fs_preparation_step",
        ondelete="restrict",
        required=True,
        help="Financial statements preparation step.",
    )
    description = fields.Text(
        string="Understanding Result",
        required=True,
        help=(
            "Understanding result for the selected step, including key processes and "
            "responsibilities."
        ),
    )
    control_activity = fields.Text(
        string="Control Activity",
        required=True,
        help="Control activities identified for the step/process.",
    )
    audit_relevancy = fields.Text(
        string="Audit Relevancy",
        required=True,
        help="How and why this area is relevant to audit assertions and procedures.",
    )
    misstatement_identification = fields.Text(
        string="Misstatement Identification",
        required=True,
        help="Potential misstatements or risks identified.",
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_f6a227_detail_2_account_type",
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
        relation="rel_general_audit_ws_f6a227_detail_2_standard_detail",
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

    def onchange_sequence(self):
        self.sequence = 10
        if self.step_id:
            self.sequence = self.step_id.sequence
