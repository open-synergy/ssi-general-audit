# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import html_escape

from ..where_clause import describe_columns, filter_csv


class GeneralAuditWSaa899bafVariable(models.Model):
    """Variable for Plausible Relationship Audit Procedure (WS-AA899BAF).

    Each record defines one variable used in the plausible relationship
    comparison.  The variable's numeric value is derived by summing a
    specific column from a GL or Subledger raw data source (optionally
    filtered with a SQL WHERE clause).
    """

    _name = "general_audit_ws_aa899baf.variable"
    _description = "Plausible Relationship Audit Procedure - Variable"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_aa899baf",
        string="Worksheet",
        required=True,
        ondelete="cascade",
        index=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    name = fields.Char(
        string="Variable Name",
        required=True,
        help="Name of the variable used in the plausible relationship comparison.",
    )
    data_mode = fields.Selection(
        string="Data Mode",
        selection=[
            ("gl", "General Ledger"),
            ("subledger", "Subledger"),
        ],
        required=True,
        help="Determines whether to use General Ledger or Subledger data as population.",
    )
    allowed_general_ledger_ids = fields.Many2many(
        comodel_name="general_audit_ws_d209914",
        string="Allowed General Ledgers",
        compute="_compute_allowed_general_ledger_ids",
        store=False,
        compute_sudo=True,
    )
    general_ledger_id = fields.Many2one(
        comodel_name="general_audit_ws_d209914",
        string="General Ledger",
        required=False,
        help="General Ledger worksheet used as data source for this variable.",
    )
    allowed_subledger_ids = fields.Many2many(
        comodel_name="general_audit_ws_b5e3d9f",
        string="Allowed Subledgers",
        compute="_compute_allowed_subledger_ids",
        store=False,
        compute_sudo=True,
    )
    subledger_id = fields.Many2one(
        comodel_name="general_audit_ws_b5e3d9f",
        string="Subledger",
        required=False,
        help="Subledger worksheet used as data source for this variable.",
    )
    data_source = fields.Selection(
        string="Data Source",
        selection=[
            ("population", "Population"),
            ("sample", "Sample"),
        ],
        required=True,
        default="population",
        help="Determines whether the raw data comes directly from the "
        "selected General Ledger/Subledger (Population), or from a "
        "Sample Determination worksheet matching it (Sample).",
    )
    allowed_sample_determination_ids = fields.Many2many(
        comodel_name="general_audit_ws_a916660",
        string="Allowed Sample Determinations",
        compute="_compute_allowed_sample_determination_ids",
        store=False,
        compute_sudo=True,
    )
    sample_determination_id = fields.Many2one(
        comodel_name="general_audit_ws_a916660",
        string="Sample Determination",
        required=False,
        help="Sample Determination worksheet used as data source for " "this variable.",
    )
    data_title = fields.Char(
        string="Data Title",
        compute="_compute_data_title",
        store=False,
        compute_sudo=True,
    )
    filter_where_clause = fields.Text(
        string="Filter (WHERE clause)",
        help="Optional SQL WHERE clause to filter the raw data.\n"
        "Use column names from the CSV header row.\n"
        "Spaces and special characters in column names are replaced "
        "by underscores. Numeric columns are compared by value, using "
        "the thousand and decimal separators set on this variable. Every "
        "change is logged in the worksheet chatter.\n"
        "Example: Entry_Label = 'posted' AND Debit > 1000",
    )
    raw_data = fields.Text(
        string="Raw Data",
        compute="_compute_raw_data",
        store=False,
        compute_sudo=True,
    )
    value_col_number = fields.Integer(
        string="Value Column Number",
        required=True,
        help="1-based column index from the raw data CSV to sum as the "
        "variable's value.",
    )
    thousand_separator = fields.Char(
        string="Thousand Separator",
        required=True,
        help="Character used as thousand separator in the CSV data. "
        "Leave empty if the data uses no thousand separator.",
        default=",",
    )
    decimal_separator = fields.Char(
        string="Decimal Separator",
        required=True,
        help="Character used as decimal separator in the CSV data. "
        "Leave empty to use the default '.' separator.",
        default=".",
    )
    value = fields.Float(
        string="Value",
        digits=(16, 2),
        compute="_compute_value",
        store=True,
        compute_sudo=True,
        help="Sum of the selected column from the filtered raw data.",
    )

    @api.depends(
        "data_mode",
        "general_ledger_id",
        "subledger_id",
        "data_source",
        "sample_determination_id",
    )
    def _compute_data_title(self):
        """Derive the display title of the currently selected data source.

        :return: sets ``data_title`` to the ``title`` of the General
            Ledger/Subledger when ``data_source`` is ``population``, or
            of ``sample_determination_id`` when it is ``sample``; empty
            when no matching source is selected.
        """
        for record in self:
            if (
                record.data_mode == "gl"
                and record.data_source == "population"
                and record.general_ledger_id
            ):
                record.data_title = record.general_ledger_id.title
            elif (
                record.data_mode == "subledger"
                and record.data_source == "population"
                and record.subledger_id
            ):
                record.data_title = record.subledger_id.title
            elif record.data_source == "sample" and record.sample_determination_id:
                record.data_title = record.sample_determination_id.title
            else:
                record.data_title = False

    @api.depends(
        "worksheet_id",
        "worksheet_id.general_audit_id",
    )
    def _compute_allowed_general_ledger_ids(self):
        GL = self.env["general_audit_ws_d209914"]
        for record in self:
            record.allowed_general_ledger_ids = False
            if record.worksheet_id and record.worksheet_id.general_audit_id:
                criteria = [
                    (
                        "general_audit_id",
                        "=",
                        record.worksheet_id.general_audit_id.id,
                    ),
                ]
                record.allowed_general_ledger_ids = GL.search(criteria)

    @api.depends(
        "worksheet_id",
        "worksheet_id.general_audit_id",
    )
    def _compute_allowed_subledger_ids(self):
        SL = self.env["general_audit_ws_b5e3d9f"]
        for record in self:
            record.allowed_subledger_ids = False
            if record.worksheet_id and record.worksheet_id.general_audit_id:
                criteria = [
                    (
                        "general_audit_id",
                        "=",
                        record.worksheet_id.general_audit_id.id,
                    ),
                ]
                record.allowed_subledger_ids = SL.search(criteria)

    @api.depends(
        "data_mode",
        "general_ledger_id",
        "subledger_id",
    )
    def _compute_allowed_sample_determination_ids(self):
        """Restrict the Sample Determination picker to the matching source.

        :return: sets ``allowed_sample_determination_ids`` to the
            ``general_audit_ws_a916660`` records sharing this record's
            selected General Ledger or Subledger, or an empty recordset
            when no source is selected.
        """
        SD = self.env["general_audit_ws_a916660"]
        for record in self:
            record.allowed_sample_determination_ids = False
            if record.data_mode == "gl" and record.general_ledger_id:
                record.allowed_sample_determination_ids = SD.search(
                    [("general_ledger_id", "=", record.general_ledger_id.id)]
                )
            elif record.data_mode == "subledger" and record.subledger_id:
                record.allowed_sample_determination_ids = SD.search(
                    [("subledger_id", "=", record.subledger_id.id)]
                )

    @api.depends(
        "data_mode",
        "general_ledger_id",
        "subledger_id",
        "data_source",
        "sample_determination_id",
        "filter_where_clause",
        "thousand_separator",
        "decimal_separator",
    )
    def _compute_raw_data(self):
        """Resolve the raw CSV data for the currently selected source.

        :return: sets ``raw_data`` to the population source (General
            Ledger/Subledger) when ``data_source`` is ``population``, or
            to ``sample_determination_id.raw_data`` when ``sample``,
            optionally filtered by ``filter_where_clause``.
        """
        for record in self:
            source_data = record._get_source_data()

            if source_data and record.filter_where_clause:
                source_data = record._apply_where_clause(
                    source_data,
                    record.filter_where_clause,
                    record.thousand_separator or ",",
                    record.decimal_separator or ".",
                )
            record.raw_data = source_data

    @api.depends(
        "data_mode",
        "general_ledger_id",
        "subledger_id",
        "data_source",
        "sample_determination_id",
        "filter_where_clause",
        "value_col_number",
        "thousand_separator",
        "decimal_separator",
    )
    def _compute_value(self):
        """Sum the value column of the currently selected data source.

        :return: sets ``value`` to the sum of ``value_col_number`` over
            the raw data resolved the same way as ``_compute_raw_data``
            (population source, or Sample Determination when
            ``data_source`` is ``sample``), after applying
            ``filter_where_clause``.
        """
        for record in self:
            # Recompute raw data inline to avoid dependency on non-stored field
            source_data = record._get_source_data()

            if source_data and record.filter_where_clause:
                source_data = record._apply_where_clause(
                    source_data,
                    record.filter_where_clause,
                    record.thousand_separator or ",",
                    record.decimal_separator or ".",
                )

            total = 0.0
            if source_data and record.value_col_number:
                reader = csv.reader(io.StringIO(source_data))
                headers = next(reader, None)
                if headers and 1 <= record.value_col_number <= len(headers):
                    col_idx = record.value_col_number - 1
                    for row in reader:
                        if col_idx < len(row):
                            total += record._parse_numeric_value(row[col_idx])
            record.value = total

    def _parse_numeric_value(self, value_str):
        if not value_str or not value_str.strip():
            return 0.0
        value_str = value_str.strip()
        if self.thousand_separator:
            value_str = value_str.replace(self.thousand_separator, "")
        if self.decimal_separator and self.decimal_separator != ".":
            value_str = value_str.replace(self.decimal_separator, ".")
        try:
            return float(value_str)
        except ValueError:
            return 0.0

    def _get_source_data(self):
        """Return the unfiltered CSV of the selected data source.

        Pulls ``raw_data`` from the General Ledger or Subledger worksheet
        selected via ``data_mode`` when ``data_source`` is ``population``,
        or from the Sample Determination worksheet selected via
        ``sample_determination_id`` when ``data_source`` is ``sample``.

        :return: the CSV text, or ``False`` when no source is selected.
        """
        self.ensure_one()
        if (
            self.data_mode == "gl"
            and self.data_source == "population"
            and self.general_ledger_id
        ):
            return self.general_ledger_id.raw_data
        if (
            self.data_mode == "subledger"
            and self.data_source == "population"
            and self.subledger_id
        ):
            return self.subledger_id.raw_data
        if self.data_source == "sample" and self.sample_determination_id:
            return self.sample_determination_id.raw_data
        return False

    @api.model
    def _apply_where_clause(
        self, raw_csv, where_clause, thousand_sep=",", decimal_sep="."
    ):
        """Filter CSV data using a read-only SQL WHERE clause.

        Failure-tolerant wrapper around ``filter_csv``: an unusable
        clause never breaks the form. ``_check_filter_where_clause``
        tells the user a clause is invalid, when it is saved.

        :param raw_csv: CSV text with a header row.
        :param where_clause: a SQL WHERE clause (without the ``WHERE``
            keyword) referencing the header's sanitised column names.
        :param thousand_sep: thousand separator used in the data.
        :param decimal_sep: decimal separator used in the data.
        :return: the filtered CSV text, or the original ``raw_csv``
            unchanged when it is empty, ``where_clause`` is blank or
            contains a forbidden keyword, or filtering fails.
        """
        try:
            return filter_csv(raw_csv, where_clause, thousand_sep, decimal_sep)
        except Exception:
            return raw_csv

    @api.constrains("filter_where_clause")
    def _check_filter_where_clause(self):
        """Reject a filter that cannot run against the data source.

        The filter is tried on the unfiltered source data with the
        variable's own separators; without source data it cannot be
        checked and is accepted.

        :return: ``None``.
        :raises ValidationError: when the filter holds a forbidden
            keyword or SQLite cannot run it, naming the usable columns.
        """
        for record in self:
            where_clause = (record.filter_where_clause or "").strip()
            source_data = record._get_source_data()
            if not where_clause or not source_data:
                continue
            try:
                filter_csv(
                    source_data,
                    where_clause,
                    record.thousand_separator or ",",
                    record.decimal_separator or ".",
                )
            except Exception as exc:
                error_message = (
                    _(
                        """
Context: Validate variable filter
Database ID: %s
Problem: The filter cannot be applied (%s)
Solution: Fix the WHERE clause. Usable columns: %s
"""
                    )
                    % (record.id, exc, describe_columns(source_data))
                )
                raise ValidationError(error_message) from exc

    def _post_filter_change_note(self, old_value):
        """Log a filter change as an internal note on the worksheet.

        :param old_value: the previous ``filter_where_clause`` text.
        :return: ``None``.
        """
        self.ensure_one()
        body = _(
            "<p>Filter (WHERE clause) of variable <b>%(name)s</b> "
            "changed.</p><ul><li>Old: <code>%(old)s</code></li>"
            "<li>New: <code>%(new)s</code></li></ul>"
        ) % {
            "name": html_escape(self.name or ""),
            "old": html_escape(old_value or ""),
            "new": html_escape(self.filter_where_clause or ""),
        }
        self.worksheet_id.message_post(body=body, subtype_xmlid="mail.mt_note")

    @api.model_create_multi
    def create(self, vals_list):
        """Create variables and log any initial filter.

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

    @api.onchange("data_mode")
    def onchange_general_ledger_id(self):
        self.general_ledger_id = False

    @api.onchange("data_mode")
    def onchange_subledger_id(self):
        self.subledger_id = False

    @api.onchange("data_mode", "general_ledger_id", "subledger_id", "data_source")
    def onchange_sample_determination_id(self):
        self.sample_determination_id = False
