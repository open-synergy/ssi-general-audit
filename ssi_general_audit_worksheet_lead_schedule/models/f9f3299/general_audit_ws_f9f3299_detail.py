# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSf9f3299Detail(models.Model):
    """
    Detail line for the per-Account-Type Lead Schedule (f9f3299).

    One record is created per GL account that belongs to the account type
    selected on the parent worksheet.  The line exposes:

    * ``account_id`` — the client GL account.
    * ``current_balance`` — End Period or Interim balance (follows parent
      ``balance_type``).
    * ``supporting_schedule`` — free-text reference to the sub-workpaper.
    * ``adjustment_ids`` / ``adjustment_dr`` / ``adjustment_cr`` — all
      proposed adjustment entries and their debit/credit totals.
    * ``adjusted_balance`` — balance after adjustments, sign-aware.
    * ``previous_balance`` — prior-year comparative.
    * ``diff`` — year-on-year percentage change, useful for preliminary
      analytical procedures.
    """

    _name = "general_audit_ws_f9f3299.detail"
    _description = "Lead Schedule - Account (f9f3299) - Detail"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_f9f3299",
        string="# Worksheet",
        required=True,
        ondelete="cascade",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="worksheet_id.general_audit_id.currency_id",
        store=True,
        help="Currency of amounts; inherited from the parent worksheet.",
    )
    detail_id = fields.Many2one(
        comodel_name="general_audit.detail",
        string="# Detail",
        required=True,
        ondelete="restrict",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="client_account",
        related="detail_id.account_id",
        store=True,
        readonly=True,
        help="Client Account",
    )
    current_balance = fields.Monetary(
        string="Current Balance",
        compute="_compute_current_balance",
        compute_sudo=True,
        store=True,
    )
    supporting_schedule = fields.Char(
        string="Supporting Schedule",
        help="Reference to the supporting schedule for this account.",
    )

    adjustment_ids = fields.Many2many(
        string="Adjustment Entries",
        comodel_name="client_adjustment_entry",
        related="detail_id.adjustment_ids",
        help="Adjustment entries related to this account.",
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
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="detail_id.previous_balance",
        store=True,
        help="Previous period balance for this account.",
    )
    diff = fields.Float(
        string="Difference (%)",
        compute="_compute_diff",
        store=True,
        help="Percentage difference between audited and previous balances.",
    )

    @api.depends(
        "adjusted_balance",
        "previous_balance",
    )
    def _compute_diff(self):
        for record in self:
            record.diff = 0.0
            if record.previous_balance != 0:
                record.diff = (record.adjusted_balance - record.previous_balance) / abs(
                    record.previous_balance
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
