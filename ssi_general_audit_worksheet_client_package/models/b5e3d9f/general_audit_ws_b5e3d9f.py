# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io

from odoo import api, fields, models


class GeneralAuditWSb5e3d9f(models.Model):
    _name = "general_audit_ws_b5e3d9f"
    _description = "Subledger (b5e3d9f)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_client_package." "worksheet_type_b5e3d9f"
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
        help="Account related to this subledger entry.",
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
    amount_col_number = fields.Integer(
        string="Amount Column Number",
        help="Column number for Amount values (starting from 1)",
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
    amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
    )

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
        "raw_data", "amount_col_number", "thousand_separator", "decimal_separator"
    )
    def _compute_amount(self):
        for record in self:
            amount_total = 0.0
            if record.raw_data and record.amount_col_number:
                try:
                    reader = csv.reader(io.StringIO(record.raw_data))
                    next(reader, None)  # Skip header row if present
                    for row in reader:
                        if len(row) >= record.amount_col_number:
                            value_str = row[record.amount_col_number - 1].strip()
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
                            amount_total += value
                except Exception:
                    amount_total = 0.0
            record.amount = amount_total
