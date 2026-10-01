# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class ClientAdjustingCoa(models.Model):
    """Adjusting Chart of Accounts of a running General Audit.

    Transactional document used when the auditor needs an account that
    does not exist in the client's chart of accounts, typically while
    preparing an Adjusting Journal Entry (AJE). Each line describes one
    new account (code, name, type). When the document reaches ``done``
    the accounts are created in ``client_account`` and added to the
    audit incrementally with ``general_audit._add_account``, so only
    worksheets from sequence 520 (Worksheet) onwards are affected.

    State flow: draft -> confirm -> done.
    """

    _name = "client_adjusting_coa"
    _description = "Accountant Client Adjusting CoA"
    _inherit = [
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.single_operating_unit",
    ]

    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True

    # The document reaches done through approval, never by a button
    _automatically_insert_done_button = False
    _automatically_insert_restart_approval_button = False

    _statusbar_visible_label = "draft,confirm,done"

    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    _create_sequence_state = "done"

    @api.model
    def _get_policy_field(self):
        res = super(ClientAdjustingCoa, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.depends(
        "account_type_set_id",
    )
    def _compute_policy(self):
        """Recompute the policy fields of the document.

        Depends on the account type set so that the policy is evaluated
        again when the audit, and so its type set, changes.
        """
        _super = super(ClientAdjustingCoa, self)
        _super._compute_policy()

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        ondelete="restrict",
        help="General Audit that receives the new accounts.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="general_audit_id.partner_id",
        compute_sudo=True,
        store=True,
        readonly=True,
        help="Client company that owns the new accounts.",
    )
    date_start = fields.Date(
        string="Start Date",
        related="general_audit_id.date_start",
        compute_sudo=True,
        store=True,
        readonly=True,
        help="Audit period start date.",
    )
    date_end = fields.Date(
        string="End Date",
        related="general_audit_id.date_end",
        compute_sudo=True,
        store=True,
        readonly=True,
        help="Audit period end date.",
    )
    interim_date_start = fields.Date(
        string="Interim Start Date",
        related="general_audit_id.interim_date_start",
        compute_sudo=True,
        store=True,
        readonly=True,
        help="Interim period start date.",
    )
    interim_date_end = fields.Date(
        string="Interim End Date",
        related="general_audit_id.interim_date_end",
        compute_sudo=True,
        store=True,
        readonly=True,
        help="Interim period end date.",
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        related="general_audit_id.previous_date_start",
        compute_sudo=True,
        store=True,
        readonly=True,
        help="Previous period start date.",
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        related="general_audit_id.previous_date_end",
        compute_sudo=True,
        store=True,
        readonly=True,
        help="Previous period end date.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        compute_sudo=True,
        store=True,
        readonly=True,
        help="Currency used for this audit.",
    )
    account_type_set_id = fields.Many2one(
        string="Account Type Set",
        related="general_audit_id.account_type_set_id",
        compute_sudo=True,
        store=True,
        readonly=True,
        help="Account type set of the audit; line types must belong to it.",
    )
    allowed_type_ids = fields.Many2many(
        string="Allowed Account Types",
        comodel_name="client_account_type",
        related="account_type_set_id.detail_ids",
        readonly=True,
        help="Account types that can be used on the lines of this document.",
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="client_adjusting_coa.detail",
        inverse_name="coa_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        copy=False,
        help="New accounts to be added to the audit.",
    )

    @ssi_decorator.pre_confirm_check()
    def _10_check_detail(self):
        """Validate the lines before the document is confirmed.

        Rejects an empty document, a code repeated on two lines, a code
        that already exists in the client's chart of accounts, and a
        type outside the account type set of the audit.

        :raises UserError: when one of the rules above is violated
        """
        self.ensure_one()
        if not self.detail_ids:
            raise UserError(self._get_error_message(_("No line is defined")))
        codes = self.detail_ids.mapped("code")
        if len(codes) != len(set(codes)):
            raise UserError(self._get_error_message(_("A code is used twice")))
        existing = self.env["client_account"].search(
            [
                ("partner_id", "=", self.partner_id.id),
                ("code", "in", codes),
            ]
        )
        if existing:
            raise UserError(
                self._get_error_message(
                    _("Account code %s already exists for this client")
                    % (", ".join(existing.mapped("code")))
                )
            )
        invalid = self.detail_ids.filtered(
            lambda line: line.type_id not in self.allowed_type_ids
        )
        if invalid:
            raise UserError(
                self._get_error_message(
                    _("Account type of code %s is not in the account type set")
                    % (", ".join(invalid.mapped("code")))
                )
            )

    def _get_error_message(self, problem):
        """Build the structured ``UserError`` text of this model.

        :param problem: short description of what is wrong
        :return: the message, with Context, Database ID, Problem and
            Solution labels
        """
        self.ensure_one()
        return _(
            """
Context: Confirm Adjusting CoA
Database ID: %s
Problem: %s
Solution: Fix the lines of the document, or ask the administrator to add
    the account type to the master data first
"""
            % (self.id, problem)
        )

    @ssi_decorator.post_done_action()
    def _10_create_account_and_add_to_audit(self):
        """Create the accounts and add them to the audit.

        Runs when the document reaches ``done``. Creates one
        ``client_account`` per line, stores it on the line, then calls
        ``general_audit._add_account``. The result cannot be undone.
        """
        self.ensure_one()
        Account = self.env["client_account"].sudo()
        accounts = Account
        for line in self.detail_ids:
            account = Account.create(line._prepare_account_data())
            line.account_id = account
            accounts |= account
        self.general_audit_id._add_account(accounts)
        self.message_post(
            body=_("Accounts added to the audit: %s")
            % (", ".join(accounts.mapped("display_name")))
        )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
