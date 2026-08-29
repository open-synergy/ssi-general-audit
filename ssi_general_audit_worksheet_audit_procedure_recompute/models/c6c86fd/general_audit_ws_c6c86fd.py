# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class GeneralAuditWSc6c86fd(models.Model):
    """
    Recalculation (Recompute) Audit Procedure Worksheet (WS-C6C86FD).

    Implements the **Recalculation** audit procedure as defined in ISA 500 /
    SA 500 (Audit Evidence). Recalculation consists of checking the mathematical
    accuracy of documents or records — for example, independently verifying
    depreciation schedules, interest accrual computations, payroll calculations,
    tax provisions, or totals and subtotals in financial schedules.

    Recalculation may be performed manually, using spreadsheet software, or by
    re-running the client's own calculation model. Because the auditor executes
    it entirely without reliance on client representations, recalculation
    provides high-quality, reliable evidence for the **Accuracy** and
    **Valuation** financial statement assertions.

    **Audit purpose:**

    - Documents the auditor's independent re-execution of mathematical
      calculations that underlie figures in the financial statements.
    - Links the procedure to a specific Key Audit Procedure (WS-E51BB1C) and
      the relevant financial statement assertions (e.g., Accuracy, Valuation
      and Allocation).
    - Associates the recalculation with the relevant standard account type
      and/or specific client account for traceability in the overall audit file.
    - Supports completeness of substantive testing evidence under ISA 330.
    - Imports raw data from either a General Ledger (WS-D209914) or a
      Subledger (WS-B5E3D9F) worksheet, selected via the ``data_mode`` field.
    - Allows the auditor to define a recompute formula using ``col_N``
      variables that reference raw-data columns, then automatically generates
      a comparison CSV (``recompute_data``) with Ref, Original Amount,
      Recompute Amount, Diff, and Result columns.

    **ISA / SA references:** ISA 500 / SA 500 — Audit Evidence;
    ISA 330 / SA 330 — The Auditor's Responses to Assessed Risks;
    ISA 520 / SA 520 — Analytical Procedures.
    """

    _name = "general_audit_ws_c6c86fd"
    _description = "Recompute Audit Procedure (c6c86fd)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_audit_procedure_recompute."
        "worksheet_type_c6c86fd"
    )
    ws_e51bb1c_id = fields.Many2one(
        comodel_name="general_audit_ws_e51bb1c",
        string="# WS-E51BB1C",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Reference to the Key Audit Procedures worksheet.",
    )
    detail_ws_e51bb1c_id = fields.Many2one(
        comodel_name="general_audit_ws_e51bb1c.detail",
        string="Detail WS-E51BB1C",
        compute="_compute_detail_ws_e51bb1c_id",
        store=True,
        help="Details from the referenced Key Audit Procedures worksheet.",
        compute_sudo=True,
    )
    allowed_key_audit_procedure_ids = fields.Many2many(
        comodel_name="general_audit_audit_procedure_category",
        string="Allowed Key Audit Procedures",
        help="Key audit procedures that can be selected based on the referenced worksheet.",
        compute="_compute_allowed_key_audit_procedure_ids",
        store=False,
        compute_sudo=True,
    )
    key_audit_procedure_id = fields.Many2one(
        comodel_name="general_audit_audit_procedure_category",
        string="Key Audit Procedure",
        help="The key audit procedure associated with the referenced worksheet.",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
    )
    allowed_account_type_ids = fields.Many2many(
        comodel_name="client_account_type",
        related="general_audit_id.account_type_ids",
        string="Allowed Account Types",
        store=False,
        help="Account types allowed for selection in this observation procedure.",
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
        help="The standard account type related to this observation procedure.",
    )
    allowed_account_ids = fields.Many2many(
        comodel_name="client_account",
        string="Allowed Accounts",
        related="general_audit_id.account_ids",
        compute_sudo=True,
    )
    account_id = fields.Many2one(
        comodel_name="client_account",
        string="Account",
        required=False,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The account related to this recompute procedure.",
    )
    data_mode = fields.Selection(
        string="Data Mode",
        selection=[
            ("gl", "General Ledger"),
            ("subledger", "Subledger"),
        ],
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Determines whether to use General Ledger or Subledger data for recompute.",
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
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The general ledger data to recompute.",
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
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The subledger data to recompute.",
    )
    data_source = fields.Selection(
        string="Data Source",
        selection=[
            ("population", "Population"),
            ("sample", "Sample"),
        ],
        required=True,
        default="population",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
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
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The sample determination data to recompute.",
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
    recompute_data = fields.Text(
        string="Recompute Data",
        readonly=True,
    )
    worksheet_result = fields.Text(
        string="Worksheet Result",
    )
    ref_col_number = fields.Integer(
        string="Ref Column Number",
        help="Column number for Ref values (starting from 1)",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    original_amount_col_number = fields.Integer(
        string="Original Amount Column Number",
        help="Column number for Original Amount values (starting from 1)",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    recompute_formula = fields.Text(
        string="Recompute Formula",
        help="Python expression to compute the recompute amount. "
        "Use col_N to reference column N from the raw data. "
        "Example: col_3 + col_4 - col_5",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    thousand_separator = fields.Char(
        string="Thousand Separator",
        help="Character used as thousand separator in the CSV data",
        default=",",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    decimal_separator = fields.Char(
        string="Decimal Separator",
        help="Character used as decimal separator in the CSV data",
        default=".",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    tolerable_amount = fields.Float(
        string="Tolerable Amount",
        digits=(16, 2),
        default=0.0,
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Absolute tolerance for comparing Original Amount vs Recompute Amount. "
        "Differences within this threshold are considered Ok.",
    )
    allowed_assertion_type_ids = fields.Many2many(
        comodel_name="general_audit_assersion_type",
        string="Allowed Assertion Types",
        help="Assertion types that can be selected based on the key audit procedure.",
        related="detail_ws_e51bb1c_id.assertion_type_ids",
        store=False,
        compute_sudo=True,
    )
    assertion_type_ids = fields.Many2many(
        comodel_name="general_audit_assersion_type",
        relation="general_audit_ws_c6c86fd_assertion_type_rel",
        column1="worksheet_id",
        column2="assertion_type_id",
        string="Assertion Types",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Assertion types relevant to this observation procedure.",
    )

    @api.depends(
        "ws_e51bb1c_id",
    )
    def _compute_allowed_key_audit_procedure_ids(self):
        Detail = self.env["general_audit_ws_e51bb1c.detail"]
        for record in self:
            record.allowed_key_audit_procedure_ids = False
            if record.ws_e51bb1c_id:
                criteria = [
                    ("worksheet_id", "=", record.ws_e51bb1c_id.id),
                    ("status", "=", "performed"),
                ]
                details = Detail.search(criteria)
                if details:
                    procedures = details.mapped("audit_procedure_category_id")
                    record.allowed_key_audit_procedure_ids = procedures

    @api.depends(
        "ws_e51bb1c_id",
        "key_audit_procedure_id",
    )
    def _compute_detail_ws_e51bb1c_id(self):
        Detail = self.env["general_audit_ws_e51bb1c.detail"]
        for record in self:
            record.detail_ws_e51bb1c_id = False
            if record.ws_e51bb1c_id and record.key_audit_procedure_id:
                criteria = [
                    ("worksheet_id", "=", record.ws_e51bb1c_id.id),
                    (
                        "audit_procedure_category_id",
                        "=",
                        record.key_audit_procedure_id.id,
                    ),
                ]
                detail = Detail.search(criteria, limit=1)
                if detail:
                    record.detail_ws_e51bb1c_id = detail

    @api.depends(
        "general_audit_id",
        "account_type_id",
        "account_id",
    )
    def _compute_allowed_general_ledger_ids(self):
        GL = self.env["general_audit_ws_d209914"]
        for record in self:
            record.allowed_general_ledger_ids = False
            if record.general_audit_id:
                criteria = [
                    ("general_audit_id", "=", record.general_audit_id.id),
                ]
                if record.account_id:
                    criteria += [
                        ("account_mode", "=", "account"),
                        ("account_id", "=", record.account_id.id),
                    ]
                else:
                    criteria += [
                        ("account_mode", "=", "standard_account"),
                    ]
                    if record.account_type_id:
                        criteria += [
                            ("account_type_id", "=", record.account_type_id.id),
                        ]
                record.allowed_general_ledger_ids = GL.search(criteria)

    @api.depends(
        "general_audit_id",
        "account_type_id",
        "account_id",
    )
    def _compute_allowed_subledger_ids(self):
        SL = self.env["general_audit_ws_b5e3d9f"]
        for record in self:
            record.allowed_subledger_ids = False
            if record.general_audit_id:
                criteria = [
                    ("general_audit_id", "=", record.general_audit_id.id),
                ]
                if record.account_id:
                    criteria += [
                        ("account_mode", "=", "account"),
                        ("account_id", "=", record.account_id.id),
                    ]
                else:
                    criteria += [
                        ("account_mode", "=", "standard_account"),
                    ]
                    if record.account_type_id:
                        criteria += [
                            ("account_type_id", "=", record.account_type_id.id),
                        ]
                record.allowed_subledger_ids = SL.search(criteria)

    @api.depends(
        "data_mode",
        "general_ledger_id",
        "subledger_id",
    )
    def _compute_allowed_sample_determination_ids(self):
        """Restrict the Sample Determination picker to the matching source.

        Unlike ``allowed_general_ledger_ids``/``allowed_subledger_ids``,
        the criteria is scoped only by ``general_ledger_id``/
        ``subledger_id`` -- ``general_audit_ws_a916660`` has no
        account-scoping fields (``account_id``/``account_type_id``) to
        filter on. Pattern mirrored from
        ``general_audit_ws_b4f7d9c._compute_allowed_sample_determination_ids``
        (``ssi_general_audit_worksheet_audit_procedure_vouching``).

        :return: sets ``allowed_sample_determination_ids`` to the
            ``general_audit_ws_a916660`` records sharing this record's
            selected General Ledger or Subledger, or an empty recordset
            when no source is selected.
        """
        SampleDetermination = self.env["general_audit_ws_a916660"]
        for record in self:
            record.allowed_sample_determination_ids = False
            if record.data_mode == "gl" and record.general_ledger_id:
                record.allowed_sample_determination_ids = SampleDetermination.search(
                    [("general_ledger_id", "=", record.general_ledger_id.id)]
                )
            elif record.data_mode == "subledger" and record.subledger_id:
                record.allowed_sample_determination_ids = SampleDetermination.search(
                    [("subledger_id", "=", record.subledger_id.id)]
                )

    @api.depends(
        "data_mode",
        "data_source",
        "general_ledger_id",
        "subledger_id",
        "sample_determination_id",
    )
    def _compute_raw_data(self):
        """Copy the recompute source data from the selected data source.

        Pulls ``raw_data`` from the General Ledger or Subledger worksheet
        selected via ``data_mode`` when ``data_source`` is ``population``,
        or from the Sample Determination worksheet selected via
        ``sample_determination_id`` when ``data_source`` is ``sample``.

        :return: sets ``raw_data`` to the ``raw_data`` of
            ``general_ledger_id``, ``subledger_id``, or
            ``sample_determination_id`` -- whichever matches the current
            ``data_mode``/``data_source`` -- or ``False`` when none
            applies.
        """
        for record in self:
            if (
                record.data_mode == "gl"
                and record.data_source == "population"
                and record.general_ledger_id
            ):
                record.raw_data = record.general_ledger_id.raw_data
            elif (
                record.data_mode == "subledger"
                and record.data_source == "population"
                and record.subledger_id
            ):
                record.raw_data = record.subledger_id.raw_data
            elif record.data_source == "sample" and record.sample_determination_id:
                record.raw_data = record.sample_determination_id.raw_data
            else:
                record.raw_data = False

    @api.depends(
        "data_mode",
        "data_source",
        "general_ledger_id",
        "subledger_id",
        "sample_determination_id",
    )
    def _compute_raw_data_title(self):
        """Copy the recompute source title from the selected data source.

        Mirrors ``_compute_raw_data``: the title comes from the same
        General Ledger/Subledger worksheet when ``data_source`` is
        ``population``, or from the Sample Determination worksheet when
        ``data_source`` is ``sample``.

        :return: sets ``raw_data_title`` to the ``title`` of
            ``general_ledger_id``, ``subledger_id``, or
            ``sample_determination_id`` -- whichever matches the current
            ``data_mode``/``data_source`` -- or ``False`` when none
            applies.
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

    @api.onchange(
        "general_audit_id",
    )
    def onchange_account_type_id(self):
        self.account_type_id = False

    @api.onchange(
        "account_type_id",
    )
    def onchange_account_id(self):
        self.account_id = False

    @api.onchange(
        "data_mode",
        "account_type_id",
        "account_id",
    )
    def onchange_general_ledger_id(self):
        self.general_ledger_id = False

    @api.onchange(
        "data_mode",
        "account_type_id",
        "account_id",
    )
    def onchange_subledger_id(self):
        self.subledger_id = False

    @api.onchange(
        "general_audit_id",
    )
    def onchange_ws_e51bb1c_id(self):
        self.ws_e51bb1c_id = False

    @api.onchange(
        "data_mode",
        "account_type_id",
        "account_id",
        "general_ledger_id",
        "subledger_id",
        "data_source",
    )
    def onchange_sample_determination_id(self):
        self.sample_determination_id = False

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

    def action_recompute(self):
        self.ensure_one()
        if not self.raw_data:
            raise UserError(_("No raw data available. Please select a data source."))
        if not self.ref_col_number:
            raise UserError(_("Please set the Ref Column Number."))
        if not self.original_amount_col_number:
            raise UserError(_("Please set the Original Amount Column Number."))
        if not self.recompute_formula:
            raise UserError(_("Please set the Recompute Formula."))

        reader = csv.reader(io.StringIO(self.raw_data))
        header = next(reader, None)
        if not header:
            raise UserError(_("Raw data has no header row."))

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            ["Ref", "Original Amount", "Recompute Amount", "Diff", "Result"]
        )

        for row in reader:
            if not row or all(not c.strip() for c in row):
                continue

            ref = ""
            if self.ref_col_number <= len(row):
                ref = row[self.ref_col_number - 1].strip()

            original_amount = 0.0
            if self.original_amount_col_number <= len(row):
                original_amount = self._parse_numeric_value(
                    row[self.original_amount_col_number - 1]
                )

            col_vars = {}
            for idx, val in enumerate(row, start=1):
                col_vars["col_{}".format(idx)] = self._parse_numeric_value(val)

            try:
                recompute_amount = float(safe_eval(self.recompute_formula, col_vars))
            except Exception as e:
                raise UserError(
                    _("Error evaluating formula on row '%s': %s") % (ref, str(e))
                )

            diff = original_amount - recompute_amount
            result = "Ok" if abs(diff) <= self.tolerable_amount else "Not Ok"

            writer.writerow([ref, original_amount, recompute_amount, diff, result])

        self.recompute_data = output.getvalue()
