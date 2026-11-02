# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models

from .general_audit_ws_b26d482_detail import BALANCE_SHEET_CATEGORIES


class GeneralAuditWSb26d482(models.Model):
    """
    WS: All Accounts Lead Schedule (b26d482) — ISA 230 / SA 230.

    Aggregates *every* GL account included in the General Audit engagement into
    a single lead schedule (top schedule / trial balance schedule).  For each
    account the worksheet shows:

    * **Current balance** — either End Period or Interim depending on
      ``balance_type``.
    * **Debit / Credit adjustments** — proposed adjustment journal entries
      sourced from the audit detail record.
    * **Adjusted balance** — current balance ± adjustments, respecting the
      account's normal balance side.
    * **Current profit / OCI / Balance sheet** — the adjusted balance
      placed in the column of the account group's report category.
    * Cross-reference to the per-account-type lead schedule
      (``general_audit_ws_f9f3299``).

    ``total_current_balance``, ``total_debit_adjustments``,
    ``total_credit_adjustments`` and ``total_adjusted_balance`` mirror
    each Monetary column of ``detail_ids`` as a grand total, shown next
    to the detail tree. ``total_current_profit``, ``total_oci`` and
    ``total_balance_sheet`` weigh each line by the normal balance of its
    account, like the aggregate of the uncorrected AJE analysis: credit
    accounts add and debit accounts subtract for profit and OCI, the
    other way round for the balance sheet. The ``total_<column>_debit``
    and ``total_<column>_credit`` fields split the five statement columns
    by the normal balance of the account, like the control rows of the
    manual lead schedule. ``total_closing_unallocated`` shows the closing
    that has no account to receive it.

    Use ``action_load_detail`` to synchronise the detail lines with the
    accounts registered on the parent General Audit.
    """

    _name = "general_audit_ws_b26d482"
    _description = "Worksheet (b26d482)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_lead_schedule." "worksheet_type_b26d482"

    balance_type = fields.Selection(
        selection=[
            ("end_period", "End Period Balance"),
            ("interim", "Interim Balance"),
        ],
        string="Balance Type",
        required=False,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Type of balance to consider for the accounts.",
    )

    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_b26d482.detail",
        inverse_name="worksheet_id",
        string="Details",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
    )
    total_current_balance = fields.Monetary(
        string="Total Current Balance",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the current balance of all detail lines.",
    )
    total_debit_adjustments = fields.Monetary(
        string="Total Debit Adjustments",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the debit adjustments of all detail lines.",
    )
    total_credit_adjustments = fields.Monetary(
        string="Total Credit Adjustments",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the credit adjustments of all detail lines.",
    )
    total_adjusted_balance = fields.Monetary(
        string="Total Adjusted Balance",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the adjusted balance of all detail lines.",
    )
    total_current_profit = fields.Monetary(
        string="Total Current Profit",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Revenue minus expense: credit accounts add and debit "
        "accounts subtract their current profit column.",
    )
    total_oci = fields.Monetary(
        string="Total OCI",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Credit accounts add and debit accounts subtract their OCI " "column.",
    )
    total_balance_sheet = fields.Monetary(
        string="Total Balance Sheet",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Assets minus liabilities and equity: debit accounts add and "
        "credit accounts subtract their balance sheet column. On a "
        "balanced trial balance with every group categorised it equals "
        "Total Current Profit plus Total OCI.",
    )
    total_current_balance_debit = fields.Monetary(
        string="Total Current Balance Debit",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the current balance column of the debit-normal accounts.",
    )
    total_current_balance_credit = fields.Monetary(
        string="Total Current Balance Credit",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the current balance column of the credit-normal accounts.",
    )
    total_adjusted_balance_debit = fields.Monetary(
        string="Total Adjusted Balance Debit",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the adjusted balance column of the debit-normal accounts.",
    )
    total_adjusted_balance_credit = fields.Monetary(
        string="Total Adjusted Balance Credit",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the adjusted balance column of the credit-normal accounts.",
    )
    total_current_profit_debit = fields.Monetary(
        string="Total Current Profit Debit",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the current profit column of the debit-normal accounts.",
    )
    total_current_profit_credit = fields.Monetary(
        string="Total Current Profit Credit",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the current profit column of the credit-normal accounts.",
    )
    total_oci_debit = fields.Monetary(
        string="Total OCI Debit",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the OCI column of the debit-normal accounts.",
    )
    total_oci_credit = fields.Monetary(
        string="Total OCI Credit",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the OCI column of the credit-normal accounts.",
    )
    total_balance_sheet_debit = fields.Monetary(
        string="Total Balance Sheet Debit",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the balance sheet column of the debit-normal accounts.",
    )
    total_balance_sheet_credit = fields.Monetary(
        string="Total Balance Sheet Credit",
        currency_field="currency_id",
        compute="_compute_total_detail",
        compute_sudo=True,
        store=True,
        help="Sum of the balance sheet column of the credit-normal accounts.",
    )
    total_closing_unallocated = fields.Monetary(
        string="Closing Not Allocated",
        currency_field="currency_id",
        compute="_compute_total_closing_unallocated",
        compute_sudo=True,
        store=True,
        help="Debit minus credit of the closing lines whose destination "
        "type has no account in this worksheet to receive it. It is not "
        "part of Total Balance Sheet; on a balanced trial balance Total "
        "Balance Sheet plus this amount equals zero.",
    )

    closing_line_ids = fields.One2many(
        string="Closing Line(s)",
        comodel_name="general_audit.closing_line",
        related="general_audit_id.closing_line_ids",
        readonly=True,
        help="Closing journal lines of the General Audit.",
    )

    @api.depends(
        "detail_ids",
        "detail_ids.current_balance",
        "detail_ids.adjustment_dr",
        "detail_ids.adjustment_cr",
        "detail_ids.adjusted_balance",
        "detail_ids.current_profit",
        "detail_ids.oci",
        "detail_ids.balance_sheet",
        "detail_ids.account_id.normal_balance",
    )
    def _compute_total_detail(self):
        """Sum every Monetary column of ``detail_ids`` onto the parent.

        The first four totals are plain sums. The current profit and OCI
        totals add credit-normal lines and subtract debit-normal lines;
        the balance sheet total does the opposite. The ``_debit`` and
        ``_credit`` totals of the five statement columns sum the lines
        of the debit-normal and credit-normal accounts separately.

        :return: None, fields are assigned in-place per record.
        """
        columns = (
            "current_balance",
            "adjusted_balance",
            "current_profit",
            "oci",
            "balance_sheet",
        )
        for record in self:
            current_balance = (
                debit_adjustments
            ) = credit_adjustments = adjusted_balance = 0.0
            current_profit = oci = balance_sheet = 0.0
            sides = {(column, side): 0.0 for column in columns for side in ("dr", "cr")}
            for detail in record.detail_ids:
                current_balance += detail.current_balance
                debit_adjustments += detail.adjustment_dr
                credit_adjustments += detail.adjustment_cr
                adjusted_balance += detail.adjusted_balance
                side = "cr" if detail.account_id.normal_balance == "cr" else "dr"
                for column in columns:
                    sides[(column, side)] += detail[column]
                if side == "cr":
                    current_profit += detail.current_profit
                    oci += detail.oci
                    balance_sheet -= detail.balance_sheet
                else:
                    current_profit -= detail.current_profit
                    oci -= detail.oci
                    balance_sheet += detail.balance_sheet
            record.total_current_balance = current_balance
            record.total_debit_adjustments = debit_adjustments
            record.total_credit_adjustments = credit_adjustments
            record.total_adjusted_balance = adjusted_balance
            record.total_current_profit = current_profit
            record.total_oci = oci
            record.total_balance_sheet = balance_sheet
            record.total_current_balance_debit = sides[("current_balance", "dr")]
            record.total_current_balance_credit = sides[("current_balance", "cr")]
            record.total_adjusted_balance_debit = sides[("adjusted_balance", "dr")]
            record.total_adjusted_balance_credit = sides[("adjusted_balance", "cr")]
            record.total_current_profit_debit = sides[("current_profit", "dr")]
            record.total_current_profit_credit = sides[("current_profit", "cr")]
            record.total_oci_debit = sides[("oci", "dr")]
            record.total_oci_credit = sides[("oci", "cr")]
            record.total_balance_sheet_debit = sides[("balance_sheet", "dr")]
            record.total_balance_sheet_credit = sides[("balance_sheet", "cr")]

    def _get_closing_allocation(self):
        """Find who receives the closing of each destination type.

        The destination lines of the closing are the lines without an
        account. For a destination type the receiver is the account of
        this worksheet with that type, in a balance sheet group, that is
        ticked ``receive_closing``; without a ticked account, the first
        one by code. A type without such an account has no receiver.

        The amount of a type is positive on its normal balance side:
        credit minus debit for a credit-normal type, debit minus credit
        for a debit-normal type.

        :return: tuple ``(receivers, amounts)``, two dictionaries keyed
            by the id of the destination type: the receiving
            ``client_account`` record and the closing amount
        """
        self.ensure_one()
        receivers = {}
        amounts = {}
        lines = self.general_audit_id.closing_line_ids.filtered(
            lambda line: not line.account_id and line.account_type_id
        )
        accounts = self.detail_ids.mapped("account_id")
        for account_type in lines.mapped("account_type_id"):
            candidates = accounts.filtered(
                lambda account: account.type_id == account_type
                and account.group_id.report_category in BALANCE_SHEET_CATEGORIES
            )
            if candidates:
                ticked = candidates.filtered("receive_closing")
                receivers[account_type.id] = (ticked or candidates.sorted("code"))[:1]
            type_lines = lines.filtered(
                lambda line: line.account_type_id == account_type
            )
            debit = sum(type_lines.mapped("debit"))
            credit = sum(type_lines.mapped("credit"))
            if account_type.normal_balance == "cr":
                amounts[account_type.id] = credit - debit
            else:
                amounts[account_type.id] = debit - credit
        return receivers, amounts

    @api.depends(
        "detail_ids.account_id",
        "detail_ids.account_id.receive_closing",
        "general_audit_id.closing_line_ids.account_id",
        "general_audit_id.closing_line_ids.account_type_id",
        "general_audit_id.closing_line_ids.debit",
        "general_audit_id.closing_line_ids.credit",
    )
    def _compute_total_closing_unallocated(self):
        """Add up the closing lines whose type has no receiving account.

        :return: None, the field is assigned in-place per record.
        """
        for record in self:
            receivers = record._get_closing_allocation()[0]
            lines = record.general_audit_id.closing_line_ids.filtered(
                lambda line: not line.account_id
                and line.account_type_id
                and line.account_type_id.id not in receivers
            )
            record.total_closing_unallocated = sum(lines.mapped("debit")) - sum(
                lines.mapped("credit")
            )

    def action_generate_closing(self):
        """Generate the closing lines of the parent General Audit.

        Runs with ``sudo()`` like ``action_load_detail`` and delegates
        to ``general_audit._generate_closing_lines``.

        :return: nothing; the closing lines of the audit are replaced
        """
        for record in self.sudo():
            record.general_audit_id._generate_closing_lines()

    def action_load_detail(self):
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        self.ensure_one()
        detail_model = self.env["general_audit_ws_b26d482.detail"]

        all_accounts = self.general_audit_id.mapped("detail_ids.account_id")
        existing_accounts = self.detail_ids.mapped("account_id")

        accounts_to_add = all_accounts - existing_accounts
        accounts_to_remove = existing_accounts - all_accounts

        # Add detail
        for account in accounts_to_add:
            detail_record = self.general_audit_id.detail_ids.filtered(
                lambda d: d.account_id == account
            )
            detail_model.create(
                {
                    "worksheet_id": self.id,
                    "detail_id": detail_record.id,
                }
            )

        # Remove detail
        details_to_remove = self.detail_ids.filtered(
            lambda d: d.account_id in accounts_to_remove
        )
        if details_to_remove:
            details_to_remove.unlink()

    def _add_accounts_to_worksheet(self, accounts):
        """Load accounts added to the audit after it started.

        Called by ``general_audit._add_account``. Delegates to
        ``_load_detail``, which only adds the missing lines and removes
        the ones whose account left the audit, so existing lines are
        kept.

        :param accounts: ``client_account`` recordset just added to the
            audit
        :return: nothing
        """
        self.ensure_one()
        self._load_detail()
