# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import html_escape

from ..where_clause import describe_columns, filter_csv


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
    * The data mode (General Ledger or Subledger) together with the data
      source (Population or Sample) used to derive the reference figures
      that appear in the confirmation request.
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
    data_source = fields.Selection(
        string="Data Source",
        selection=[
            ("population", "Population"),
            ("sample", "Sample"),
        ],
        required=True,
        default="population",
        help="Determines whether the reference data comes directly from "
        "the selected General Ledger/Subledger (Population), or from a "
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
        help="Sample Determination worksheet used as data source for this "
        "confirmation.",
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
    raw_data = fields.Text(
        string="Raw Data",
        compute="_compute_raw_data",
        store=False,
        compute_sudo=True,
    )
    raw_data_title = fields.Char(
        string="Raw Data Title",
        compute="_compute_raw_data_title",
        store=True,
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
    )
    def _compute_allowed_sample_determination_ids(self):
        """Restrict selectable Sample Determination worksheets.

        Only Sample Determination worksheets whose own
        ``general_ledger_id``/``subledger_id`` matches this confirmation's
        selected General Ledger/Subledger (per ``data_mode``) are allowed.
        Pattern mirrored from
        ``general_audit_ws_b4f7d9c._compute_allowed_sample_determination_ids``
        (``ssi_general_audit_worksheet_audit_procedure_vouching``).

        :return: none, assigns ``allowed_sample_determination_ids``
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
        "data_source",
        "general_ledger_id",
        "subledger_id",
        "sample_determination_id",
        "filter_where_clause",
    )
    def _compute_raw_data(self):
        """Derive the reference CSV data from the selected data source.

        :return: none, assigns ``raw_data`` from ``_get_source_data``,
            narrowed by ``filter_where_clause`` (if any).
        """
        for record in self:
            source_data = record._get_source_data()
            if source_data and record.filter_where_clause:
                thousand_sep, decimal_sep = record._get_separators()
                source_data = record._apply_where_clause(
                    source_data,
                    record.filter_where_clause,
                    thousand_sep,
                    decimal_sep,
                )
            record.raw_data = source_data

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

    def _get_separators(self):
        """Resolve the thousand/decimal separators of the data source.

        :return: a ``(thousand_separator, decimal_separator)`` tuple from
            the selected Sample Determination, General Ledger or
            Subledger, defaulting to ``(",", ".")`` without a source.
        """
        self.ensure_one()
        if self.data_source == "sample" and self.sample_determination_id:
            return self.sample_determination_id._get_separators()
        source = False
        if self.data_mode == "gl":
            source = self.general_ledger_id
        elif self.data_mode == "subledger":
            source = self.subledger_id
        if source:
            return (
                source.thousand_separator or ",",
                source.decimal_separator or ".",
            )
        return (",", ".")

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

        The filter is tried on the unfiltered source data; without
        source data it cannot be checked and is accepted.

        :return: ``None``.
        :raises ValidationError: when the filter holds a forbidden
            keyword or SQLite cannot run it, naming the usable columns.
        """
        for record in self:
            where_clause = (record.filter_where_clause or "").strip()
            source_data = record._get_source_data()
            if not where_clause or not source_data:
                continue
            thousand_sep, decimal_sep = record._get_separators()
            try:
                filter_csv(source_data, where_clause, thousand_sep, decimal_sep)
            except Exception as exc:
                error_message = (
                    _(
                        """
Context: Validate confirmation filter
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
            "<p>Filter (WHERE clause) of confirmation <b>%(name)s</b> "
            "changed.</p><ul><li>Old: <code>%(old)s</code></li>"
            "<li>New: <code>%(new)s</code></li></ul>"
        ) % {
            "name": html_escape(self.party_name or ""),
            "old": html_escape(old_value or ""),
            "new": html_escape(self.filter_where_clause or ""),
        }
        self.worksheet_id.message_post(body=body, subtype_xmlid="mail.mt_note")

    @api.model_create_multi
    def create(self, vals_list):
        """Create confirmations and log any initial filter.

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

    @api.depends(
        "data_mode",
        "data_source",
        "general_ledger_id",
        "subledger_id",
        "sample_determination_id",
    )
    def _compute_raw_data_title(self):
        """Derive the display title of the selected data source.

        Mirrors ``_compute_raw_data``: the title comes from the same
        General Ledger/Subledger worksheet when ``data_source`` is
        ``population``, or from the Sample Determination worksheet when
        ``data_source`` is ``sample``.

        :return: none, assigns ``raw_data_title``
        """
        for record in self:
            if (
                record.data_mode == "gl"
                and record.data_source == "population"
                and record.general_ledger_id
            ):
                record.raw_data_title = record.general_ledger_id.title
            elif (
                record.data_mode == "subledger"
                and record.data_source == "population"
                and record.subledger_id
            ):
                record.raw_data_title = record.subledger_id.title
            elif record.data_source == "sample" and record.sample_determination_id:
                record.raw_data_title = record.sample_determination_id.title
            else:
                record.raw_data_title = False

    @api.onchange("data_mode")
    def onchange_general_ledger_id(self):
        self.general_ledger_id = False

    @api.onchange("data_mode")
    def onchange_subledger_id(self):
        self.subledger_id = False

    @api.onchange("data_mode", "general_ledger_id", "subledger_id", "data_source")
    def onchange_sample_determination_id(self):
        self.sample_determination_id = False

    @api.depends(
        "date_sent",
        "date_received",
        "detail_ids.confirmation_data",
    )
    def _compute_result_status(self):
        for record in self:
            if not record.date_sent:
                record.result_status = "kfk"
            elif record.date_sent and not record.date_received:
                record.result_status = "kft"
            elif record.date_received:
                details = record.detail_ids
                if details and all(d._check_agreed() for d in details):
                    record.result_status = "kfo"
                elif details:
                    record.result_status = "kfb"
                else:
                    record.result_status = "kfo"
            else:
                record.result_status = False

    @api.depends("detail_ids.confirmation_data")
    def _compute_internal_confirmation_result(self):
        for record in self:
            details = record.detail_ids
            if not details:
                record.internal_confirmation_result = False
                continue
            agreed_list = [d._check_agreed() for d in details]
            if all(agreed_list):
                record.internal_confirmation_result = "ok"
            elif not any(agreed_list):
                record.internal_confirmation_result = "not_ok"
            else:
                record.internal_confirmation_result = "partial"

    def action_open_confirmation_details(self):
        self.ensure_one()
        action = self.env.ref(
            "ssi_general_audit_worksheet_audit_procedure_confirmation"
            ".general_audit_ws_d45dd19_confirmation_detail_action"
        ).read()[0]
        action["domain"] = [("confirmation_id", "=", self.id)]
        action["context"] = {"default_confirmation_id": self.id}
        return action
