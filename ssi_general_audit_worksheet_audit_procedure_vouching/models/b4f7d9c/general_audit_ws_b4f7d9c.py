# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io

from odoo import api, fields, models


class GeneralAuditWSb4f7d9c(models.Model):
    """Worksheet for Vouching Audit Procedure.

    This worksheet implements the **vouching** audit procedure in accordance
    with ISA 500 / SA 500 (Audit Evidence).  Vouching is a substantive audit
    procedure where the auditor traces from recorded transactions *back* to
    supporting source documents (e.g. invoices, purchase orders, contracts,
    payment authorizations) to verify the accuracy, completeness, and validity
    of the recorded amounts.

    Typical use cases include:

    - Verifying recorded revenue by tracing sales entries to customer invoices
      and delivery notes
    - Confirming recorded expenses by tracing journal entries to vendor
      invoices and payment authorizations
    - Validating fixed-asset additions by tracing to purchase orders and
      supplier invoices
    - Substantiating payroll charges by tracing to employment contracts and
      authorization records

    Workflow context:

    - References a Key Audit Procedures worksheet (WS-E51BB1C / Lead Schedule)
      to link the vouching work to a specific planned audit procedure
    - The ``account_type_id`` field ties the vouching test to the relevant
      financial statement account being audited
    - Assertion types (e.g. Existence, Completeness, Accuracy) indicate which
      financial statement assertions the vouching procedure addresses

    ISA/SA references: ISA 500, SA 500 — Audit Evidence
    """

    _name = "general_audit_ws_b4f7d9c"
    _description = "Vouching Audit Procedure (b4f7d9c)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_audit_procedure_vouching." "worksheet_type_b4f7d9c"
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
        help="Account types allowed for selection in this vouching procedure.",
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
        help="The standard account type related to this vouching procedure.",
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
        relation="general_audit_ws_b4f7d9c_assertion_type_rel",
        column1="worksheet_id",
        column2="assertion_type_id",
        string="Assertion Types",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Assertion types relevant to this vouching procedure.",
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
        "population for this vouching procedure.",
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
        help="The general ledger data used as population for this vouching "
        "procedure.",
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
        help="The subledger data used as population for this vouching procedure.",
    )
    raw_data = fields.Text(
        string="Raw Data",
        compute="_compute_raw_data",
        store=False,
        compute_sudo=True,
        help="Raw CSV data from the selected General Ledger or Subledger.",
    )
    # ── Test of Detail ───────────────────────────────────────────────────────
    allowed_test_of_detail_ids = fields.Many2many(
        comodel_name="general_audit_ws_a916660",
        string="Allowed Test of Detail",
        compute="_compute_allowed_test_of_detail_ids",
        store=False,
        compute_sudo=True,
        help="Test of Detail worksheets whose data source matches the current "
        "data mode and selected ledger/subledger.",
    )
    test_of_detail_id = fields.Many2one(
        comodel_name="general_audit_ws_a916660",
        string="# Test of Detail",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Reference to the Test of Detail worksheet whose sampling result "
        "will be used as the list of items to vouch.",
    )
    sampling_data = fields.Text(
        string="Sampling Data",
        related="test_of_detail_id.sampling_data",
        store=True,
        compute_sudo=True,
        help="Sampling data inherited from the referenced Test of Detail "
        "worksheet, used as the list of items subject to vouching.",
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
    vouching_data = fields.Text(
        string="Vouching Data",
        compute="_compute_vouching_data",
        store=False,
        compute_sudo=True,
        help="Subset of raw data filtered to rows whose reference column "
        "value appears in column 2 of the sampling data.",
    )
    # ── Child O2M ────────────────────────────────────────────────────────────
    data_comparison_ids = fields.One2many(
        comodel_name="general_audit_ws_b4f7d9c.data_comparison",
        inverse_name="worksheet_id",
        string="Data Comparisons",
        help="Comparison data sources to be matched against the sampling data "
        "using the reference column.",
    )
    vouching_ids = fields.One2many(
        comodel_name="general_audit_ws_b4f7d9c.vouching",
        inverse_name="worksheet_id",
        string="Vouching Lines",
        help="Vouching comparison lines that compare the header raw data "
        "against the selected data comparison source.",
    )
    population_description = fields.Text(
        string="Population Description",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Description of the population or set of transactions subject to "
        "this vouching procedure, including the period covered and any "
        "stratification applied.",
    )
    sampling_description = fields.Text(
        string="Sampling Description",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Description of the sampling approach used to select items for "
        "vouching (e.g. random, systematic, judgmental) and the basis for the "
        "sample size determination.",
    )
    findings = fields.Text(
        string="Findings",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Summary of exceptions, differences, or notable observations "
        "identified during the vouching procedure.",
    )
    worksheet_result = fields.Text(
        string="Worksheet Result",
        help="Overall result or conclusion of this vouching audit procedure.",
    )

    @api.depends(
        "raw_data",
        "sampling_data",
        "reference_col_number",
    )
    def _compute_vouching_data(self):
        for record in self:
            record.vouching_data = False
            raw = record.raw_data
            sampling = record.sampling_data
            ref_col = record.reference_col_number
            if not raw or not sampling or not ref_col:
                continue
            try:
                sampling_reader = csv.reader(io.StringIO(sampling))
                sampling_rows = list(sampling_reader)
                ref_values = set()
                for idx, row in enumerate(sampling_rows):
                    if idx == 0:
                        continue
                    if len(row) >= 2:
                        ref_values.add(row[1].strip())
                raw_reader = csv.reader(io.StringIO(raw))
                raw_rows = list(raw_reader)
                if not raw_rows:
                    continue
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
                    record.vouching_data = output.getvalue()
            except Exception:
                record.vouching_data = False

    @api.depends("general_audit_id")
    def _compute_allowed_general_ledger_ids(self):
        GL = self.env["general_audit_ws_d209914"]
        for record in self:
            record.allowed_general_ledger_ids = False
            if record.general_audit_id:
                record.allowed_general_ledger_ids = GL.search(
                    [("general_audit_id", "=", record.general_audit_id.id)]
                )

    @api.depends("general_audit_id")
    def _compute_allowed_subledger_ids(self):
        SL = self.env["general_audit_ws_b5e3d9f"]
        for record in self:
            record.allowed_subledger_ids = False
            if record.general_audit_id:
                record.allowed_subledger_ids = SL.search(
                    [("general_audit_id", "=", record.general_audit_id.id)]
                )

    @api.depends(
        "data_mode",
        "general_ledger_id",
        "subledger_id",
    )
    def _compute_raw_data(self):
        for record in self:
            if record.data_mode == "gl" and record.general_ledger_id:
                record.raw_data = record.general_ledger_id.raw_data
            elif record.data_mode == "subledger" and record.subledger_id:
                record.raw_data = record.subledger_id.raw_data
            else:
                record.raw_data = False

    @api.depends(
        "data_mode",
        "general_ledger_id",
        "subledger_id",
    )
    def _compute_allowed_test_of_detail_ids(self):
        TOD = self.env["general_audit_ws_a916660"]
        for record in self:
            record.allowed_test_of_detail_ids = False
            if record.data_mode == "gl" and record.general_ledger_id:
                record.allowed_test_of_detail_ids = TOD.search(
                    [("general_ledger_id", "=", record.general_ledger_id.id)]
                )
            elif record.data_mode == "subledger" and record.subledger_id:
                record.allowed_test_of_detail_ids = TOD.search(
                    [("subledger_id", "=", record.subledger_id.id)]
                )

    @api.depends("ws_e51bb1c_id")
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

    @api.onchange("general_audit_id")
    def onchange_account_type_id(self):
        self.account_type_id = False

    @api.onchange("general_audit_id")
    def onchange_ws_e51bb1c_id(self):
        self.ws_e51bb1c_id = False

    @api.onchange("ws_e51bb1c_id")
    def onchange_key_audit_procedure_id(self):
        self.key_audit_procedure_id = False

    @api.onchange("key_audit_procedure_id")
    def onchange_assertion_type_ids(self):
        self.assertion_type_ids = False

    @api.onchange("data_mode")
    def onchange_general_ledger_id(self):
        self.general_ledger_id = False

    @api.onchange("data_mode")
    def onchange_subledger_id(self):
        self.subledger_id = False

    @api.onchange("data_mode", "general_ledger_id", "subledger_id")
    def onchange_test_of_detail_id(self):
        self.test_of_detail_id = False

    # ── Action methods ───────────────────────────────────────────────────────

    def action_open_data_comparisons(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Data Comparisons",
            "res_model": "general_audit_ws_b4f7d9c.data_comparison",
            "view_mode": "tree,form",
            "domain": [("worksheet_id", "=", self.id)],
            "context": {
                "default_worksheet_id": self.id,
            },
        }

    def action_open_vouching_lines(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Vouching Lines",
            "res_model": "general_audit_ws_b4f7d9c.vouching",
            "view_mode": "tree,form",
            "domain": [("worksheet_id", "=", self.id)],
            "context": {
                "default_worksheet_id": self.id,
            },
        }
