# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io

from odoo import api, fields, models


class GeneralAuditWSC7D5F2B(models.Model):
    """Worksheet for Physical Check Audit Procedure.

    This worksheet implements the **physical check** (physical
    inspection) audit procedure in accordance with ISA 501 (Audit
    Evidence -- Specific Considerations for Selected Items). Physical
    check is a substantive audit procedure where the auditor directly
    inspects tangible assets (e.g. fixed assets, inventory) to verify
    their existence, condition, and completeness against recorded
    amounts -- in contrast to vouching, which traces recorded
    transactions to supporting *documents* rather than to the physical
    item itself.

    Typical use cases include:

    - Observing physical inventory counts and comparing the counted
      quantity/value to the recorded inventory ledger
    - Physically inspecting fixed assets (e.g. property, plant and
      equipment) to confirm existence and condition against the fixed
      asset register
    - Comparing a physically-verified count/measurement to a
      previously-sampled population of items

    Workflow context:

    - References a Key Audit Procedures worksheet (WS-E51BB1C / Lead
      Schedule) to link the physical check work to a specific planned
      audit procedure
    - The ``account_type_id`` field ties the physical check test to the
      relevant financial statement account being audited
    - Assertion types (e.g. Existence, Completeness) indicate which
      financial statement assertions the physical check procedure
      addresses

    ISA/SA references: ISA 501 -- Audit Evidence, Specific
    Considerations for Selected Items
    """

    _name = "general_audit_ws_c7d5f2b"
    _description = "Physical Check (c7d5f2b)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_physical_check.worksheet_type_c7d5f2b"

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
        help="Key audit procedures that can be selected based on the "
        "referenced worksheet.",
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
        help="Account types allowed for selection in this physical check " "procedure.",
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
        help="The standard account type related to this physical check " "procedure.",
    )
    allowed_assertion_type_ids = fields.Many2many(
        comodel_name="general_audit_assersion_type",
        string="Allowed Assertion Types",
        help="Assertion types that can be selected based on the key audit "
        "procedure.",
        related="detail_ws_e51bb1c_id.assertion_type_ids",
        store=False,
        compute_sudo=True,
    )
    assertion_type_ids = fields.Many2many(
        comodel_name="general_audit_assersion_type",
        relation="general_audit_ws_c7d5f2b_assertion_type_rel",
        column1="worksheet_id",
        column2="assertion_type_id",
        string="Assertion Types",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Assertion types relevant to this physical check procedure.",
    )
    # ── Data Mode ────────────────────────────────────────────────────────────
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
        help="Determines whether to use General Ledger or Subledger data as "
        "population for this physical check procedure.",
    )
    allowed_general_ledger_ids = fields.Many2many(
        comodel_name="general_audit_ws_d209914",
        string="Allowed General Ledgers",
        compute="_compute_allowed_general_ledger_ids",
        store=False,
        compute_sudo=True,
        help="General Ledger worksheets available for the current audit engagement.",
    )
    general_ledger_id = fields.Many2one(
        comodel_name="general_audit_ws_d209914",
        string="General Ledger",
        required=False,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The general ledger data used as population for this physical "
        "check procedure.",
    )
    allowed_subledger_ids = fields.Many2many(
        comodel_name="general_audit_ws_b5e3d9f",
        string="Allowed Subledgers",
        compute="_compute_allowed_subledger_ids",
        store=False,
        compute_sudo=True,
        help="Subledger worksheets available for the current audit engagement.",
    )
    subledger_id = fields.Many2one(
        comodel_name="general_audit_ws_b5e3d9f",
        string="Subledger",
        required=False,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The subledger data used as population for this physical check "
        "procedure.",
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
    raw_data = fields.Text(
        string="Raw Data",
        compute="_compute_raw_data",
        store=False,
        compute_sudo=True,
        help="Raw CSV data from the selected General Ledger or Subledger.",
    )
    # ── Sample Determination ─────────────────────────────────────────────────
    allowed_sample_determination_ids = fields.Many2many(
        comodel_name="general_audit_ws_a916660",
        string="Allowed Sample Determination",
        compute="_compute_allowed_sample_determination_ids",
        store=False,
        compute_sudo=True,
        help="Sample Determination worksheets whose data source matches the current "
        "data mode and selected ledger/subledger.",
    )
    sample_determination_id = fields.Many2one(
        comodel_name="general_audit_ws_a916660",
        string="# Sample Determination",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Reference to the Sample Determination worksheet whose sampling "
        "result will be used as the list of items subject to physical check.",
    )
    sampling_data = fields.Text(
        string="Sampling Data",
        related="sample_determination_id.sampling_data",
        store=True,
        compute_sudo=True,
        help="Sampling data inherited from the referenced Sample Determination "
        "worksheet, used as the list of items subject to physical check.",
    )
    reference_col_number = fields.Integer(
        string="Reference Column Number",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The column number (1-based) in the sampling data that contains "
        "the reference identifier used to match against comparison data.",
    )
    check_data = fields.Text(
        string="Check Data",
        compute="_compute_check_data",
        store=False,
        compute_sudo=True,
        help="Subset of raw data whose reference column matches the "
        "sampling data, used as the population subject to physical check "
        "comparison.",
    )
    # ── Child O2M ────────────────────────────────────────────────────────────
    data_comparison_ids = fields.One2many(
        comodel_name="general_audit_ws_c7d5f2b.data_comparison",
        inverse_name="worksheet_id",
        string="Data Comparisons",
        help="Comparison data sources to be matched against the sampling data "
        "using the reference column.",
    )
    check_line_ids = fields.One2many(
        comodel_name="general_audit_ws_c7d5f2b.check_line",
        inverse_name="worksheet_id",
        string="Check Lines",
        help="Physical check comparison lines that compare the header raw "
        "data against the selected data comparison source.",
    )
    population_description = fields.Text(
        string="Population Description",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Description of the population or set of items subject to this "
        "physical check procedure, including the location covered and any "
        "stratification applied.",
    )
    sampling_description = fields.Text(
        string="Sampling Description",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Description of the sampling approach used to select items for "
        "physical check (e.g. random, systematic, judgmental) and the basis "
        "for the sample size determination.",
    )
    findings = fields.Text(
        string="Findings",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Summary of exceptions, differences, or notable observations "
        "identified during the physical check procedure.",
    )
    worksheet_result = fields.Text(
        string="Worksheet Result",
        help="Overall result or conclusion of this physical check audit " "procedure.",
    )

    @api.depends(
        "data_source",
        "raw_data",
        "sampling_data",
        "reference_col_number",
    )
    def _compute_check_data(self):
        """Compute the data actually used for the physical check procedure.

        :return: nothing; assigns ``check_data``. When ``data_source``
            is ``"population"``, the whole ``raw_data`` is used as-is
            (no cross-reference against a sample). When ``data_source``
            is ``"sample"``, ``raw_data`` is filtered to the rows whose
            ``reference_col_number`` column value appears in the
            referenced ``sampling_data`` (excluding rows marked
            ``"Candidate"``).
        """
        for record in self:
            result = False
            raw = record.raw_data
            sampling = record.sampling_data
            ref_col = record.reference_col_number
            if record.data_source == "population":
                if raw:
                    result = raw
            elif raw and sampling and ref_col:
                try:
                    sampling_reader = csv.reader(io.StringIO(sampling))
                    sampling_rows = list(sampling_reader)
                    ref_values = set()
                    for idx, row in enumerate(sampling_rows):
                        if idx == 0:
                            continue
                        if len(row) >= 2 and row[-1].strip() != "Candidate":
                            ref_values.add(row[1].strip())
                    raw_reader = csv.reader(io.StringIO(raw))
                    raw_rows = list(raw_reader)
                    if raw_rows:
                        result_rows = [raw_rows[0]]
                        for idx, row in enumerate(raw_rows):
                            if idx == 0:
                                continue
                            if len(row) >= ref_col:
                                if row[ref_col - 1].strip() in ref_values:
                                    result_rows.append(row)
                        if len(result_rows) > 1:
                            output = io.StringIO()
                            writer = csv.writer(output)
                            writer.writerows(result_rows)
                            result = output.getvalue()
                except Exception:
                    result = False
            record.check_data = result

    @api.depends("general_audit_id")
    def _compute_allowed_general_ledger_ids(self):
        """Restrict the General Ledger picker to the current engagement.

        :return: nothing; assigns ``allowed_general_ledger_ids`` to the
            ``general_audit_ws_d209914`` records of the same
            ``general_audit_id``, or an empty recordset when the
            engagement is not set.
        """
        GL = self.env["general_audit_ws_d209914"]
        for record in self:
            record.allowed_general_ledger_ids = False
            if record.general_audit_id:
                record.allowed_general_ledger_ids = GL.search(
                    [("general_audit_id", "=", record.general_audit_id.id)]
                )

    @api.depends("general_audit_id")
    def _compute_allowed_subledger_ids(self):
        """Restrict the Subledger picker to the current engagement.

        :return: nothing; assigns ``allowed_subledger_ids`` to the
            ``general_audit_ws_b5e3d9f`` records of the same
            ``general_audit_id``, or an empty recordset when the
            engagement is not set.
        """
        SL = self.env["general_audit_ws_b5e3d9f"]
        for record in self:
            record.allowed_subledger_ids = False
            if record.general_audit_id:
                record.allowed_subledger_ids = SL.search(
                    [("general_audit_id", "=", record.general_audit_id.id)]
                )

    @api.depends(
        "data_mode",
        "data_source",
        "general_ledger_id",
        "subledger_id",
        "sample_determination_id",
    )
    def _compute_raw_data(self):
        """Compute raw CSV data from the selected data source.

        :return: nothing; assigns ``raw_data`` from the General Ledger
            or Subledger when ``data_source`` is ``"population"``, from
            the referenced Sample Determination worksheet when it is
            ``"sample"``, or ``False`` when no matching source is
            selected.
        """
        for record in self:
            result = False
            if record.data_source == "population":
                if record.data_mode == "gl" and record.general_ledger_id:
                    result = record.general_ledger_id.raw_data
                elif record.data_mode == "subledger" and record.subledger_id:
                    result = record.subledger_id.raw_data
            elif record.data_source == "sample" and record.sample_determination_id:
                result = record.sample_determination_id.raw_data
            record.raw_data = result

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

    @api.depends("ws_e51bb1c_id")
    def _compute_allowed_key_audit_procedure_ids(self):
        """Restrict the Key Audit Procedure picker to performed details.

        :return: nothing; assigns ``allowed_key_audit_procedure_ids`` to
            the audit procedure categories of the performed detail lines
            on the referenced ``ws_e51bb1c_id``, or an empty recordset
            when the reference is not set.
        """
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
        """Resolve the matching detail line on the referenced worksheet.

        :return: nothing; assigns ``detail_ws_e51bb1c_id`` to the detail
            line whose ``audit_procedure_category_id`` matches
            ``key_audit_procedure_id``, or ``False`` when either
            reference is unset or no match is found.
        """
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

    @api.onchange("general_audit_id")
    def onchange_account_type_id(self):
        """Reset ``account_type_id`` when the audit engagement changes."""
        self.account_type_id = False

    @api.onchange("general_audit_id")
    def onchange_ws_e51bb1c_id(self):
        """Reset ``ws_e51bb1c_id`` when the audit engagement changes."""
        self.ws_e51bb1c_id = False

    @api.onchange("ws_e51bb1c_id")
    def onchange_key_audit_procedure_id(self):
        """Reset ``key_audit_procedure_id`` when its source changes."""
        self.key_audit_procedure_id = False

    @api.onchange("key_audit_procedure_id")
    def onchange_assertion_type_ids(self):
        """Reset ``assertion_type_ids`` when its source changes."""
        self.assertion_type_ids = False

    @api.onchange("data_mode")
    def onchange_general_ledger_id(self):
        """Reset ``general_ledger_id`` when ``data_mode`` changes."""
        self.general_ledger_id = False

    @api.onchange("data_mode")
    def onchange_subledger_id(self):
        """Reset ``subledger_id`` when ``data_mode`` changes."""
        self.subledger_id = False

    @api.onchange("data_mode", "general_ledger_id", "subledger_id")
    def onchange_sample_determination_id(self):
        """Reset ``sample_determination_id`` when its scoping changes."""
        self.sample_determination_id = False

    # ── Action methods ───────────────────────────────────────────────────────

    def action_open_data_comparisons(self):
        """Open the Data Comparisons list of this worksheet.

        :return: an ``ir.actions.act_window`` dict opening
            ``general_audit_ws_c7d5f2b.data_comparison`` records whose
            ``worksheet_id`` is this record.
        """
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Data Comparisons",
            "res_model": "general_audit_ws_c7d5f2b.data_comparison",
            "view_mode": "tree,form",
            "domain": [("worksheet_id", "=", self.id)],
            "context": {
                "default_worksheet_id": self.id,
            },
        }

    def action_open_check_lines(self):
        """Open the Check Lines list of this worksheet.

        :return: an ``ir.actions.act_window`` dict opening
            ``general_audit_ws_c7d5f2b.check_line`` records whose
            ``worksheet_id`` is this record.
        """
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Check Lines",
            "res_model": "general_audit_ws_c7d5f2b.check_line",
            "view_mode": "tree,form",
            "domain": [("worksheet_id", "=", self.id)],
            "context": {
                "default_worksheet_id": self.id,
            },
        }
