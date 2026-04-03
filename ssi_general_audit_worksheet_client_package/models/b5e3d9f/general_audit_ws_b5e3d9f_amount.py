# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io

from odoo import api, fields, models


class GeneralAuditWSb5e3d9fAmount(models.Model):
    _name = "general_audit_ws_b5e3d9f.amount"
    _description = "Subledger (b5e3d9f) - Amount"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_b5e3d9f",
        string="# Worksheet",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    label = fields.Char(
        string="Label",
        required=True,
    )
    col_number = fields.Integer(
        string="Column Number",
        help="Column number for this amount value (starting from 1)",
        required=True,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="worksheet_id.currency_id",
        compute_sudo=True,
    )
    amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "col_number",
        "worksheet_id.raw_data",
        "worksheet_id.thousand_separator",
        "worksheet_id.decimal_separator",
    )
    def _compute_amount(self):
        for record in self:
            amount_total = 0.0
            raw_data = record.worksheet_id.raw_data
            col_number = record.col_number
            thousand_sep = record.worksheet_id.thousand_separator or ","
            decimal_sep = record.worksheet_id.decimal_separator or "."
            if raw_data and col_number:
                try:
                    reader = csv.reader(io.StringIO(raw_data))
                    next(reader, None)  # Skip header row if present
                    for row in reader:
                        if len(row) >= col_number:
                            value_str = row[col_number - 1].strip()
                            if value_str:
                                value_str = value_str.replace(thousand_sep, "")
                                value_str = value_str.replace(decimal_sep, ".")
                                value = float(value_str)
                            else:
                                value = 0.0
                            amount_total += value
                except Exception:
                    amount_total = 0.0
            record.amount = amount_total
