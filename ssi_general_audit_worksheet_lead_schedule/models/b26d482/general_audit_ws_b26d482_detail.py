# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSb26d482Detail(models.Model):
    """
    Detail line for the All Accounts Lead Schedule (b26d482).

    One record is created per GL account included in the General Audit.
    The line mirrors the parent ``general_audit.detail`` record and exposes:

    * ``current_balance`` — computed from End Period or Interim balance
      depending on the parent worksheet's ``balance_type``.
    * ``adjustment_dr`` / ``adjustment_cr`` — total debit/credit adjustments
      from the audit detail.
    * ``adjusted_balance`` — net balance after applying adjustments, honouring
      the account's normal balance convention.
    * ``current_profit`` / ``oci`` / ``balance_sheet`` — the adjusted
      balance placed in the column of the account group's report category
      (Profit & Loss, Other Comprehensive Income, or asset, liability and
      equity), left at zero in the other columns.
    * ``ws_f9f3299_id`` — optional cross-reference to the per-account-type
      lead schedule (``general_audit_ws_f9f3299``).
    """

    _name = "general_audit_ws_b26d482.detail"
    _description = "Worksheet (b26d482) - Detail"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_b26d482",
        string="Worksheet",
        required=True,
        ondelete="cascade",
    )
    detail_id = fields.Many2one(
        comodel_name="general_audit.detail",
        string="Detail",
        ondelete="restrict",
        required=True,
    )
    account_id = fields.Many2one(
        comodel_name="client_account",
        string="Account",
        related="detail_id.account_id",
        store=True,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="worksheet_id.general_audit_id.currency_id",
        store=True,
        readonly=True,
    )
    current_balance = fields.Monetary(
        string="Current Balance",
        currency_field="currency_id",
        compute="_compute_current_balance",
        compute_sudo=True,
        store=False,
    )
    ws_f9f3299_id = fields.Many2one(
        comodel_name="general_audit_ws_f9f3299",
        ondelete="restrict",
        string="Lead Schedule - Account (f9f3299)",
    )
    adjustment_dr = fields.Monetary(
        string="Total Debit Adjustments",
        related="detail_id.adjustment_dr",
        store=True,
        help="Total debit adjustments for this account.",
    )
    adjustment_cr = fields.Monetary(
        string="Total Credit Adjustments",
        related="detail_id.adjustment_cr",
        store=True,
        help="Total credit adjustments for this account.",
    )
    adjusted_balance = fields.Monetary(
        string="Adjusted Balance",
        compute="_compute_adjusted_balance",
        compute_sudo=True,
        store=True,
    )
    current_profit = fields.Monetary(
        string="Current Profit",
        compute="_compute_statement_columns",
        compute_sudo=True,
        store=True,
        help="Adjusted balance of an account whose group has the "
        "Profit & Loss report category.",
    )
    oci = fields.Monetary(
        string="OCI",
        compute="_compute_statement_columns",
        compute_sudo=True,
        store=True,
        help="Adjusted balance of an account whose group has the "
        "Other Comprehensive Income report category.",
    )
    balance_sheet = fields.Monetary(
        string="Balance Sheet",
        compute="_compute_statement_columns",
        compute_sudo=True,
        store=True,
        help="Adjusted balance of an account whose group has the Asset, "
        "Liability or Equity report category.",
    )

    @api.depends(
        "worksheet_id.balance_type",
        "detail_id",
        "detail_id.home_statement_balance",
        "detail_id.interim_balance",
    )
    def _compute_current_balance(self):
        for record in self:
            record.current_balance = 0.0
            if record.worksheet_id.balance_type == "end_period":
                record.current_balance = record.detail_id.home_statement_balance
            else:
                record.current_balance = record.detail_id.interim_balance

    @api.depends(
        "current_balance",
        "adjustment_dr",
        "adjustment_cr",
        "account_id",
    )
    def _compute_adjusted_balance(self):
        for record in self:
            record.adjusted_balance = 0.0
            if record.account_id:
                if record.account_id.normal_balance == "dr":
                    record.adjusted_balance = (
                        record.current_balance
                        + record.adjustment_dr
                        - record.adjustment_cr
                    )
                else:
                    record.adjusted_balance = (
                        record.current_balance
                        - record.adjustment_dr
                        + record.adjustment_cr
                    )

    @api.depends(
        "adjusted_balance",
        "account_id.type_id.group_id.report_category",
    )
    def _compute_statement_columns(self):
        """Place the adjusted balance in its financial statement column.

        The category comes from the report category of the account
        group. Profit & Loss feeds ``current_profit``, Other
        Comprehensive Income feeds ``oci`` and asset, liability and
        equity feed ``balance_sheet``. The adjusted balance is copied as
        is, on the normal balance side of the account; a group without a
        report category leaves all three columns at zero.

        :return: ``None``, the columns are assigned in-place per record
        """
        for record in self:
            record.current_profit = 0.0
            record.oci = 0.0
            record.balance_sheet = 0.0
            category = record.account_id.type_id.group_id.report_category
            if category == "profit_loss":
                record.current_profit = record.adjusted_balance
            elif category == "oci":
                record.oci = record.adjusted_balance
            elif category in ("asset", "liability", "equity"):
                record.balance_sheet = record.adjusted_balance
