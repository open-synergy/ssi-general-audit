# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io

from odoo import api, fields, models


class GeneralAuditWSd209914(models.Model):
    """Worksheet — General Ledger data import (d209914).

    Accepts client general-ledger transaction data in CSV format for a selected
    client account and parses debit/credit columns to compute the net movement
    and ending balance.  Configurable column numbers (``debit_col_number``,
    ``credit_col_number``) and separators allow flexible handling of
    client-specific export formats.

    The worksheet is linked to the lead-schedule detail (``detail_id``) so that
    the computed ledger totals can be reconciled to the trial balance figure.
    This supports the lead-schedule tie-out procedure and substantive testing
    of account balances.

    ISA/SA references: ISA 500/SA 500 (Audit Evidence);
    ISA 520/SA 520 (Analytical Procedures).
    """

    _name = "general_audit_ws_d209914"
    _description = "General Ledger (d209914)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_client_package." "worksheet_type_d209914"
    )

    account_mode = fields.Selection(
        string="Account Mode",
        selection=[
            ("account", "Account"),
            ("standard_account", "Standard Account"),
        ],
        default="account",
        required=True,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Determines whether to select by Account or Standard Account.",
    )
    account_id = fields.Many2one(
        comodel_name="client_account",
        string="Account",
        required=False,
        ondelete="restrict",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Account related to this general ledger entry.",
    )
    allowed_account_ids = fields.Many2many(
        comodel_name="client_account",
        string="Allowed Accounts",
        related="general_audit_id.account_ids",
        compute_sudo=True,
    )
    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Standard Account",
        required=False,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Standard account type related to this general ledger entry.",
    )
    allowed_account_type_ids = fields.Many2many(
        comodel_name="client_account_type",
        related="general_audit_id.account_type_ids",
        string="Allowed Account Types",
        store=False,
        help="Account types allowed for selection in this general ledger.",
        compute_sudo=True,
    )
    detail_id = fields.Many2one(
        comodel_name="general_audit.detail",
        string="Detail",
        compute="_compute_detail_id",
        store=True,
        readonly=True,
        compute_sudo=True,
    )
    raw_data = fields.Text(
        string="Raw Data",
        help="Raw data in CSV format",
        required=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    debit_col_number = fields.Integer(
        string="Debit Column Number",
        help="Column number for Debit values (starting from 1)",
        required=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    credit_col_number = fields.Integer(
        string="Credit Column Number",
        help="Column number for Credit values (starting from 1)",
        required=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    identifier_col_number = fields.Integer(
        string="Identifier Column Number",
        help="Column number (starting from 1) for the row identifier/reference "
        "value in Raw Data — used by consuming worksheets when examining the "
        "population directly (e.g. Test of Detail).",
        required=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    thousand_separator = fields.Char(
        string="Thousand Separator",
        help="Character used as thousand separator in the CSV data",
        required=False,
        default=",",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    decimal_separator = fields.Char(
        string="Decimal Separator",
        help="Character used as decimal separator in the CSV data",
        required=False,
        default=".",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    title = fields.Char(
        string="Title",
        required=False,
        default="-",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    debit = fields.Monetary(
        string="Debit",
        currency_field="currency_id",
        compute="_compute_debit",
        store=True,
        compute_sudo=True,
    )
    credit = fields.Monetary(
        string="Credit",
        currency_field="currency_id",
        compute="_compute_credit",
        store=True,
        compute_sudo=True,
    )
    balance = fields.Monetary(
        string="Balance",
        currency_field="currency_id",
        compute="_compute_balance",
        store=True,
        compute_sudo=True,
    )
    initial_balance = fields.Monetary(
        string="Initial Balance",
        currency_field="currency_id",
        required=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    ending_balance = fields.Monetary(
        string="Ending Balance",
        currency_field="currency_id",
        compute="_compute_ending_balance",
        store=True,
        compute_sudo=True,
    )

    @api.onchange("account_mode")
    def onchange_account_mode(self):
        if self.account_mode == "account":
            self.account_type_id = False
        elif self.account_mode == "standard_account":
            self.account_id = False

    @api.depends("general_audit_id", "account_id")
    def _compute_detail_id(self):
        for record in self:
            result = False
            if record.general_audit_id and record.account_id:
                result = self.env["general_audit.detail"].search(
                    [
                        ("general_audit_id", "=", record.general_audit_id.id),
                        ("account_id", "=", record.account_id.id),
                    ],
                    limit=1,
                )
            record.detail_id = result

    @api.depends(
        "raw_data", "debit_col_number", "thousand_separator", "decimal_separator"
    )
    def _compute_debit(self):
        for record in self:
            debit_total = 0.0
            if record.raw_data and record.debit_col_number:
                try:
                    reader = csv.reader(io.StringIO(record.raw_data))
                    next(reader, None)  # Skip header row if present
                    for row in reader:
                        if len(row) >= record.debit_col_number:
                            value_str = row[record.debit_col_number - 1].strip()
                            if value_str:
                                # Remove thousand separator
                                value_str = value_str.replace(
                                    record.thousand_separator, ""
                                )
                                # Replace decimal separator with '.'
                                value_str = value_str.replace(
                                    record.decimal_separator, "."
                                )
                                value = float(value_str)
                            else:
                                value = 0.0
                            debit_total += value
                except Exception:
                    debit_total = 0.0
            record.debit = debit_total

    @api.depends(
        "raw_data", "credit_col_number", "thousand_separator", "decimal_separator"
    )
    def _compute_credit(self):
        for record in self:
            credit_total = 0.0
            if record.raw_data and record.credit_col_number:
                try:
                    reader = csv.reader(io.StringIO(record.raw_data))
                    next(reader, None)  # Skip header row if present
                    for row in reader:
                        if len(row) >= record.credit_col_number:
                            value_str = row[record.credit_col_number - 1].strip()
                            if value_str:
                                # Remove thousand separator
                                value_str = value_str.replace(
                                    record.thousand_separator, ""
                                )
                                # Replace decimal separator with '.'
                                value_str = value_str.replace(
                                    record.decimal_separator, "."
                                )
                                value = float(value_str)
                            else:
                                value = 0.0
                            credit_total += value
                except Exception:
                    credit_total = 0.0
            record.credit = credit_total

    @api.depends("debit", "credit", "account_id")
    def _compute_balance(self):
        for record in self:
            if record.account_id:
                if record.account_id.normal_balance == "dr":
                    record.balance = record.debit - record.credit
                else:
                    record.balance = record.credit - record.debit

    @api.depends("initial_balance", "balance")
    def _compute_ending_balance(self):
        for record in self:
            record.ending_balance = record.initial_balance + record.balance
