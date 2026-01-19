# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io

from odoo import api, fields, models


class GeneralAuditWSd209914(models.Model):
    _name = "general_audit_ws_d209914"
    _description = "General Ledger (d209914)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_client_package." "worksheet_type_d209914"
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

    @api.depends("general_audit_id", "account_id")
    def _coompute_detail_id(self):
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
