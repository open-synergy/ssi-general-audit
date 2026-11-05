# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import html_escape

from ..where_clause import describe_columns, filter_csv


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
        "by underscores. Numeric columns are compared by value, using "
        "the thousand and decimal separators of the data source. Every "
        "change is logged in the worksheet chatter.\n"
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

    @api.constrains("filter_where_clause")
    def _check_filter_where_clause(self):
        """Reject a filter that cannot run against the confirmation data.

        The filter is tried on ``confirmation_id.raw_data``; without
        data it cannot be checked and is accepted.

        :return: ``None``.
        :raises ValidationError: when the filter holds a forbidden
            keyword or SQLite cannot run it, naming the usable columns.
        """
        for record in self:
            where_clause = (record.filter_where_clause or "").strip()
            raw_data = record.confirmation_id.raw_data
            if not where_clause or not raw_data:
                continue
            thousand_sep, decimal_sep = record.confirmation_id._get_separators()
            try:
                filter_csv(raw_data, where_clause, thousand_sep, decimal_sep)
            except Exception as exc:
                error_message = (
                    _(
                        """
Context: Validate confirmation detail filter
Database ID: %s
Problem: The filter cannot be applied (%s)
Solution: Fix the WHERE clause. Usable columns: %s
"""
                    )
                    % (record.id, exc, describe_columns(raw_data))
                )
                raise ValidationError(error_message) from exc

    def _post_filter_change_note(self, old_value):
        """Log a filter change as an internal note on the worksheet.

        :param old_value: the previous ``filter_where_clause`` text.
        :return: ``None``.
        """
        self.ensure_one()
        body = _(
            "<p>Filter (WHERE clause) of confirmation detail "
            "<b>%(name)s</b> changed.</p><ul><li>Old: "
            "<code>%(old)s</code></li><li>New: <code>%(new)s</code></li></ul>"
        ) % {
            "name": html_escape(
                self.confirmation_type or self.confirmation_id.party_name or ""
            ),
            "old": html_escape(old_value or ""),
            "new": html_escape(self.filter_where_clause or ""),
        }
        self.confirmation_id.worksheet_id.message_post(
            body=body, subtype_xmlid="mail.mt_note"
        )

    @api.model_create_multi
    def create(self, vals_list):
        """Create details and log any initial filter.

        :param vals_list: the values of the records to create.
        :return: the created records.
        """
        records = super().create(vals_list)
        for record in records:
            if record.filter_where_clause:
                record._post_filter_change_note(False)
        return records

    def write(self, vals):
        """Write values and log a change of ``filter_where_clause``.

        :param vals: the values to write.
        :return: the result of the parent ``write``.
        """
        if "filter_where_clause" not in vals:
            return super().write(vals)
        old_values = {record.id: record.filter_where_clause for record in self}
        result = super().write(vals)
        for record in self:
            old_value = old_values[record.id]
            if (old_value or "") != (record.filter_where_clause or ""):
                record._post_filter_change_note(old_value)
        return result

    def action_generate_data(self):
        for record in self:
            raw_data = record.confirmation_id.raw_data
            if not raw_data:
                record.confirmation_data = False
                continue

            if record.filter_where_clause:
                thousand_sep, decimal_sep = record.confirmation_id._get_separators()
                raw_data = record.confirmation_id._apply_where_clause(
                    raw_data,
                    record.filter_where_clause,
                    thousand_sep,
                    decimal_sep,
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
