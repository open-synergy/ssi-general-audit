# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io

from odoo import fields, models


class GeneralAuditWSd45dd19ConfirmationDetail(models.Model):
    _name = "general_audit_ws_d45dd19.confirmation.detail"
    _description = "Confirmation Audit Procedure WS - Confirmation Detail"
    _order = "confirmation_id, sequence, id"

    confirmation_id = fields.Many2one(
        comodel_name="general_audit_ws_d45dd19.confirmation",
        string="Confirmation",
        required=True,
        ondelete="cascade",
        index=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    confirmation_type = fields.Char(
        string="Confirmation Type",
    )
    filter_where_clause = fields.Text(
        string="Filter (WHERE clause)",
        help="Optional SQL WHERE clause to filter the raw data.\n"
        "Use column names from the CSV header row.\n"
        "Spaces and special characters in column names are replaced "
        "by underscores.\n"
        "Example: Entry_Label = 'posted' AND Debit > 1000",
    )
    confirmation_data = fields.Text(
        string="Confirmation Data",
    )
    reference_col_number = fields.Integer(
        string="Reference Column Number",
        help="Column number (1-based) in the raw data that contains "
        "the reference identifier.",
    )
    amount_original_col_number = fields.Integer(
        string="Amount Original Column Number",
        help="Column number (1-based) in the raw data that contains "
        "the original amount.",
    )

    def action_generate_data(self):
        for record in self:
            raw_data = record.confirmation_id.raw_data
            if not raw_data:
                record.confirmation_data = False
                continue

            if record.filter_where_clause:
                raw_data = record.confirmation_id._apply_where_clause(
                    raw_data, record.filter_where_clause
                )

            if not raw_data:
                record.confirmation_data = False
                continue

            reader = csv.reader(io.StringIO(raw_data))
            headers = next(reader, None)
            if not headers:
                record.confirmation_data = False
                continue

            rows = list(reader)
            if not rows:
                record.confirmation_data = False
                continue

            ref_idx = (record.reference_col_number or 1) - 1
            amt_idx = (record.amount_original_col_number or 1) - 1

            out = io.StringIO()
            writer = csv.writer(out)
            writer.writerow(["Ref", "Original", "Confirmation Amount"])
            for row in rows:
                ref_val = row[ref_idx] if ref_idx < len(row) else ""
                amt_val = row[amt_idx] if amt_idx < len(row) else ""
                writer.writerow([ref_val, amt_val, amt_val])

            record.confirmation_data = out.getvalue()

    def _get_total_original_amount(self):
        """Sum the 'Original' column from confirmation_data CSV."""
        self.ensure_one()
        if not self.confirmation_data:
            return 0.0
        reader = csv.reader(io.StringIO(self.confirmation_data))
        headers = next(reader, None)
        if not headers:
            return 0.0
        try:
            orig_idx = headers.index("Original")
        except ValueError:
            return 0.0
        total = 0.0
        for row in reader:
            if len(row) <= orig_idx:
                continue
            try:
                total += float(row[orig_idx]) if row[orig_idx] else 0.0
            except (ValueError, TypeError):
                continue
        return total

    def _check_agreed(self):
        """Check if all rows in confirmation_data have
        Original == Confirmation Amount within tolerable_amount."""
        self.ensure_one()
        if not self.confirmation_data:
            return True
        tolerable = (
            self.confirmation_id.worksheet_id.tolerable_amount
            if self.confirmation_id and self.confirmation_id.worksheet_id
            else 0.0
        )
        reader = csv.reader(io.StringIO(self.confirmation_data))
        headers = next(reader, None)
        if not headers:
            return True
        try:
            orig_idx = headers.index("Original")
            conf_idx = headers.index("Confirmation Amount")
        except ValueError:
            return True
        for row in reader:
            if len(row) <= max(orig_idx, conf_idx):
                continue
            try:
                orig_val = float(row[orig_idx]) if row[orig_idx] else 0.0
                conf_val = float(row[conf_idx]) if row[conf_idx] else 0.0
            except (ValueError, TypeError):
                continue
            if abs(orig_val - conf_val) > tolerable:
                return False
        return True
