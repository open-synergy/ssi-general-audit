# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io
import re
import sqlite3

from odoo import api, fields, models


class GeneralAuditWSd45dd19Confirmation(models.Model):
    """
    Confirmation record for the External Confirmation Audit Procedure
    Worksheet (WS-D45DD19).

    Represents a single external confirmation request dispatched to a third
    party (e.g. a bank, debtor, or legal counsel) as part of the confirmation
    procedure under ISA 505 / SA 505.  Each record captures:

    * The external party from whom confirmation is requested (name and address).
    * The type of confirmation (positive or negative).
    * The dispatch and receipt dates of the confirmation letter.
    * The data source (General Ledger or Subledger) used to derive the
      reference figures that appear in the confirmation request.
    * The book balance and confirmation amount, together with the resulting
      difference and the auditor's internal assessment.

    Field layout is adapted from the "Confirm" sheet of the working-paper
    template (RR.SS.X.03):

        No. | Nama Bank | Alamat Bank | Ref | Tanggal Pengiriman |
        Saldo Per Book (VALAS / IDR / Total IDR) |
        Jawaban Konfirmasi (VALAS / IDR / Total IDR) |
        Selisih | Penjelasan | Hasil Konfirmasi Internal

    **ISA / SA references:** ISA 505 / SA 505 — External Confirmations.
    """

    _name = "general_audit_ws_d45dd19.confirmation"
    _description = "Confirmation Audit Procedure WS - Confirmation"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_d45dd19",
        string="Worksheet",
        required=True,
        ondelete="cascade",
        index=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    party_name = fields.Char(
        string="Confirmation Party",
    )
    party_address = fields.Char(
        string="Party Address",
    )
    confirmation_type = fields.Selection(
        string="Confirmation Type",
        selection=[
            ("positive", "Positive"),
            ("negative", "Negative"),
        ],
        help="Type of external confirmation: Positive (reply expected) or "
        "Negative (reply only if the third party disagrees).",
    )
    date_sent = fields.Date(
        string="Date Sent",
        help="Date on which the confirmation request was dispatched to the "
        "external party.",
    )
    date_received = fields.Date(
        string="Date Received",
        help="Date on which the confirmation response was received from the "
        "external party.",
    )
    data_mode = fields.Selection(
        string="Data Mode",
        selection=[
            ("gl", "General Ledger"),
            ("subledger", "Subledger"),
        ],
        help="Data source used to derive the reference balances included in "
        "this confirmation request.",
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
        help="General Ledger worksheet used as data source for this " "confirmation.",
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
        help="Subledger worksheet used as data source for this confirmation.",
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
    result_status = fields.Selection(
        string="Result Status",
        selection=[
            ("kfo", "Kfo – Confirmation returned, agreed"),
            ("kfb", "Kfb – Confirmation returned, different"),
            ("kft", "Kft – Confirmation not returned"),
            ("kfk", "Kfk – Confirmation undeliverable"),
        ],
        compute="_compute_result_status",
        store=True,
        help="Derived automatically: Kfk if date_sent is not filled, Kft if "
        "sent but not yet received, Kfo if received and all details agree, "
        "Kfb if received with any difference.",
    )
    internal_confirmation_result = fields.Selection(
        string="Internal Confirmation Result",
        selection=[
            ("ok", "Ok"),
            ("not_ok", "Not Ok"),
            ("partial", "Partial"),
        ],
        compute="_compute_internal_confirmation_result",
        store=True,
        help="Derived from detail lines: Ok if all agreed, Not Ok if all "
        "different, Partial if mixed.",
    )
    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_d45dd19.confirmation.detail",
        inverse_name="confirmation_id",
        string="Confirmation Details",
    )
    explanation = fields.Text(
        string="Explanation",
        help="Auditor's notes or explanation for any difference found in this "
        "confirmation.",
    )

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
        "filter_where_clause",
    )
    def _compute_raw_data(self):
        for record in self:
            if record.data_mode == "gl" and record.general_ledger_id:
                source_data = record.general_ledger_id.raw_data
            elif record.data_mode == "subledger" and record.subledger_id:
                source_data = record.subledger_id.raw_data
            else:
                source_data = False

            if source_data and record.filter_where_clause:
                source_data = record._apply_where_clause(
                    source_data, record.filter_where_clause
                )
            record.raw_data = source_data

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

    @api.depends(
        "date_sent",
        "date_received",
        "detail_ids.status",
    )
    def _compute_result_status(self):
        for record in self:
            if not record.date_sent:
                record.result_status = "kfk"
            elif record.date_sent and not record.date_received:
                record.result_status = "kft"
            elif record.date_received:
                details = record.detail_ids
                if details and all(d.status == "agreed" for d in details):
                    record.result_status = "kfo"
                elif details:
                    record.result_status = "kfb"
                else:
                    record.result_status = "kfo"
            else:
                record.result_status = False

    @api.depends("detail_ids.status")
    def _compute_internal_confirmation_result(self):
        for record in self:
            statuses = record.detail_ids.mapped("status")
            if not statuses:
                record.internal_confirmation_result = False
            elif all(s == "agreed" for s in statuses):
                record.internal_confirmation_result = "ok"
            elif all(s == "different" for s in statuses):
                record.internal_confirmation_result = "not_ok"
            else:
                record.internal_confirmation_result = "partial"
