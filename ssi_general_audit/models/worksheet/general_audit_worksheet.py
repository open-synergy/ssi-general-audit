# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GeneralAuditWorksheet(models.Model):
    _name = "general_audit_worksheet"
    _description = "General Audit Worksheet"
    _inherit = [
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.transaction_done",
    ]
    _order = "general_audit_id, parent_type_id, id"

    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"
    _create_sequence_state = "open"

    @api.model
    def _get_policy_field(self):
        res = super(GeneralAuditWorksheet, self)._get_policy_field()
        policy_field = [
            "open_ok",
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def _compute_policy(self):
        _super = super(GeneralAuditWorksheet, self)
        _super._compute_policy()

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        readonly=True,
        required=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="General Audit to which this worksheet belongs.",
    )
    # Fields related from general audit
    date_start = fields.Date(
        string="Start Date",
        related="general_audit_id.date_start",
        readonly=True,
        store=True,
        help="Audit period start date.",
    )
    date_end = fields.Date(
        string="End Date",
        related="general_audit_id.date_end",
        readonly=True,
        store=True,
        help="Audit period end date.",
    )
    interim_date_start = fields.Date(
        string="Interim Start Date",
        related="general_audit_id.interim_date_start",
        readonly=True,
        store=True,
        help="Start date for the interim period.",
    )
    interim_date_end = fields.Date(
        string="Interim End Date",
        related="general_audit_id.interim_date_end",
        readonly=True,
        store=True,
        help="End date for the interim period.",
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        related="general_audit_id.previous_date_start",
        readonly=True,
        store=True,
        help="Start date of the previous period.",
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        related="general_audit_id.previous_date_end",
        readonly=True,
        store=True,
        help="End date of the previous period.",
    )
    preparation_date = fields.Date(
        string="Preparation Date",
        help="Date when the worksheet was prepared.",
    )
    preparation_time = fields.Integer(
        string="Preparation Time",
        help="Effort spent preparing the worksheet (in hours or minutes).",
    )
    review_date = fields.Date(
        string="Review Date",
        help="Date when the worksheet was reviewed.",
    )
    review_time = fields.Integer(
        string="Review Time",
        help="Effort spent reviewing the worksheet (in hours or minutes).",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        readonly=True,
        store=True,
        help="Currency used for amounts in this worksheet.",
    )
    account_type_set_id = fields.Many2one(
        string="Accoount Type Set",
        comodel_name="client_account_type_set",
        related="general_audit_id.account_type_set_id",
        readonly=True,
        store=True,
        help="Account type set used by the linked General Audit.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        related="general_audit_id.partner_id",
        store=True,
        help="Audited client company.",
    )
    accountant_id = fields.Many2one(
        string="Accountant",
        related="general_audit_id.accountant_id",
        store=True,
        help="Accountant responsible for the audit.",
    )
    title = fields.Char(
        string="Title",
        related="general_audit_id.title",
        store=True,
        help="Title of the General Audit engagement.",
    )
    parent_type_id = fields.Many2one(
        string="Parent Type",
        comodel_name="general_audit_worksheet_type",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Worksheet type category/group for this specific worksheet.",
    )
    conclusion_id = fields.Many2one(
        string="Conclusion",
        comodel_name="general_audit_worksheet_conclusion",
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Selected conclusion summarizing the worksheet's assessment.",
    )
    conclusion = fields.Text(
        string="Conclusion Additional Explanation",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Narrative explanation to support the selected conclusion.",
    )

    @api.constrains(
        "state",
    )
    def _constrains_state_change_confirm(self):
        for record in self.sudo():
            if record.state == "confirm":
                if not record._check_conclusion():
                    error_message = _(
                        """
                    Context: Confirm worksheet
                    Database ID: %s
                    Problem: Conclusion is not set
                    Solution: Choose conclusion
                    """
                        % (self.id)
                    )
                    raise ValidationError(error_message)

                if not record._check_conclusion_explanation():
                    error_message = _(
                        """
                    Context: Confirm worksheet
                    Database ID: %s
                    Problem: Conclusion explanation is not set
                    Solution: Fill conclusion explanation
                    """
                        % (self.id)
                    )
                    raise ValidationError(error_message)

    def _check_conclusion(self):
        self.ensure_one()
        result = True
        if not self.conclusion_id:
            result = False

        return result

    def _check_conclusion_explanation(self):
        self.ensure_one()
        result = True
        if not self.conclusion:
            result = False

        return result
