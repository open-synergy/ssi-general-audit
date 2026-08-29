# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io
import re
import sqlite3

from odoo import api, fields, models


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
            ("sample_determination", "Sample Determination"),
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
        "by underscores.\n"
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
        "sample_determination_id",
    )
    def _compute_data_title(self):
        for record in self:
            if record.data_mode == "gl" and record.general_ledger_id:
                record.data_title = record.general_ledger_id.title
            elif record.data_mode == "subledger" and record.subledger_id:
                record.data_title = record.subledger_id.title
            elif (
                record.data_mode == "sample_determination"
                and record.sample_determination_id
            ):
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
        "worksheet_id",
        "worksheet_id.general_audit_id",
    )
    def _compute_allowed_sample_determination_ids(self):
        """Restrict the Sample Determination picker to the current audit.

        :return: sets ``allowed_sample_determination_ids`` to the
            ``general_audit_ws_a916660`` records sharing this variable's
            worksheet's ``general_audit_id``, or an empty recordset when
            unset.
        """
        SD = self.env["general_audit_ws_a916660"]
        for record in self:
            record.allowed_sample_determination_ids = False
            if record.worksheet_id and record.worksheet_id.general_audit_id:
                criteria = [
                    (
                        "general_audit_id",
                        "=",
                        record.worksheet_id.general_audit_id.id,
                    ),
                ]
                record.allowed_sample_determination_ids = SD.search(criteria)

    @api.depends(
        "data_mode",
        "general_ledger_id",
        "subledger_id",
        "sample_determination_id",
        "filter_where_clause",
    )
    def _compute_raw_data(self):
        for record in self:
            if record.data_mode == "gl" and record.general_ledger_id:
                source_data = record.general_ledger_id.raw_data
            elif record.data_mode == "subledger" and record.subledger_id:
                source_data = record.subledger_id.raw_data
            elif (
                record.data_mode == "sample_determination"
                and record.sample_determination_id
            ):
                source_data = record.sample_determination_id.raw_data
            else:
                source_data = False

            if source_data and record.filter_where_clause:
                source_data = record._apply_where_clause(
                    source_data, record.filter_where_clause
                )
            record.raw_data = source_data

    @api.depends(
        "data_mode",
        "general_ledger_id",
        "subledger_id",
        "sample_determination_id",
        "filter_where_clause",
        "value_col_number",
        "thousand_separator",
        "decimal_separator",
    )
    def _compute_value(self):
        for record in self:
            # Recompute raw data inline to avoid dependency on non-stored field
            if record.data_mode == "gl" and record.general_ledger_id:
                source_data = record.general_ledger_id.raw_data
            elif record.data_mode == "subledger" and record.subledger_id:
                source_data = record.subledger_id.raw_data
            elif (
                record.data_mode == "sample_determination"
                and record.sample_determination_id
            ):
                source_data = record.sample_determination_id.raw_data
            else:
                source_data = False

            if source_data and record.filter_where_clause:
                source_data = record._apply_where_clause(
                    source_data, record.filter_where_clause
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

    @api.model
    def _apply_where_clause(self, raw_csv, where_clause):
        """Filter CSV data using a SQL WHERE clause via in-memory SQLite."""
        where_clause = (where_clause or "").strip()
        if not where_clause:
            return raw_csv

        # Reject dangerous SQL keywords
        _FORBIDDEN = re.compile(
            r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|DETACH"
            r"|REPLACE|PRAGMA|REINDEX|VACUUM|SAVEPOINT|RELEASE"
            r"|BEGIN|COMMIT|ROLLBACK)\b",
            re.IGNORECASE,
        )
        if _FORBIDDEN.search(where_clause):
            return raw_csv

        reader = csv.reader(io.StringIO(raw_csv))
        headers = next(reader, None)
        if not headers:
            return raw_csv

        rows = list(reader)
        if not rows:
            return raw_csv

        # Sanitise header names: replace non-alphanumeric chars with _
        safe_cols = []
        for h in headers:
            col = re.sub(r"[^\w]", "_", h.strip())
            if not col or col[0].isdigit():
                col = "c_" + col
            safe_cols.append(col)

        col_defs = ", ".join('"{}" TEXT'.format(c) for c in safe_cols)
        placeholders = ", ".join(["?"] * len(safe_cols))

        try:
            conn = sqlite3.connect(":memory:")
            cur = conn.cursor()
            cur.execute("CREATE TABLE data ({})".format(col_defs))
            for row in rows:
                # Pad or trim row to match header count
                padded = list(row) + [""] * (len(safe_cols) - len(row))
                cur.execute(
                    "INSERT INTO data VALUES ({})".format(placeholders),
                    padded[: len(safe_cols)],
                )
            cur.execute("SELECT * FROM data WHERE {}".format(where_clause))
            filtered = cur.fetchall()
            conn.close()
        except Exception:
            return raw_csv

        # Rebuild CSV output
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(headers)
        writer.writerows(filtered)
        return out.getvalue()

    @api.onchange("data_mode")
    def onchange_general_ledger_id(self):
        self.general_ledger_id = False

    @api.onchange("data_mode")
    def onchange_subledger_id(self):
        self.subledger_id = False

    @api.onchange("data_mode")
    def onchange_sample_determination_id(self):
        self.sample_determination_id = False
