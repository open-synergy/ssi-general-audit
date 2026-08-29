# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSb4f7d9cDataComparison(models.Model):
    """Comparison line for a Vouching Audit Procedure worksheet.

    Each row provides an alternate raw data source -- General Ledger,
    Subledger, or a matching Sample Determination worksheet -- that is
    later matched against the parent worksheet's sampling data via
    ``reference_col_number``.
    """

    _name = "general_audit_ws_b4f7d9c.data_comparison"
    _description = "Vouching Data Comparison"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_b4f7d9c",
        string="# Worksheet",
        required=True,
        ondelete="cascade",
        index=True,
        help="Parent vouching worksheet.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Determines the display order of data comparison lines.",
    )
    general_audit_id = fields.Many2one(
        related="worksheet_id.general_audit_id",
        store=True,
        help="General audit engagement from the parent worksheet.",
    )
    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store=True,
        compute_sudo=True,
        help="Title from the selected General Ledger or Subledger.",
    )
    # ── Data Mode ────────────────────────────────────────────────────────────
    data_mode = fields.Selection(
        string="Data Mode",
        selection=[
            ("gl", "General Ledger"),
            ("subledger", "Subledger"),
        ],
        help="Determines whether to use General Ledger or Subledger data "
        "as the comparison source.",
    )
    allowed_general_ledger_ids = fields.Many2many(
        comodel_name="general_audit_ws_d209914",
        string="Allowed General Ledgers",
        compute="_compute_allowed_general_ledger_ids",
        store=False,
        compute_sudo=True,
        help="General Ledger worksheets available for the current audit " "engagement.",
    )
    general_ledger_id = fields.Many2one(
        comodel_name="general_audit_ws_d209914",
        string="General Ledger",
        required=False,
        help="The general ledger data used as comparison source.",
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
        help="The subledger data used as comparison source.",
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
        help="Sample Determination worksheets whose data source matches "
        "this row's own data mode and selected ledger/subledger.",
    )
    sample_determination_id = fields.Many2one(
        comodel_name="general_audit_ws_a916660",
        string="# Sample Determination",
        required=False,
        help="Reference to the Sample Determination worksheet used as "
        "the raw data source for this comparison row when data_source "
        'is "sample".',
    )
    reference_col_number = fields.Integer(
        string="Reference Column Number",
        help="The column number (1-based) in the comparison raw data that "
        "contains the reference identifier to match against the parent "
        "worksheet's reference column.",
    )

    # ── Compute methods ──────────────────────────────────────────────────────

    @api.depends(
        "data_mode",
        "general_ledger_id",
        "general_ledger_id.title",
        "subledger_id",
        "subledger_id.title",
    )
    def _compute_name(self):
        for record in self:
            if record.data_mode == "gl" and record.general_ledger_id:
                record.name = record.general_ledger_id.title
            elif record.data_mode == "subledger" and record.subledger_id:
                record.name = record.subledger_id.title
            else:
                record.name = False

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
        """Restrict the Sample Determination picker to this row's source.

        :return: nothing; assigns ``allowed_sample_determination_ids``
            to the ``general_audit_ws_a916660`` records sharing this
            row's own selected General Ledger or Subledger, or an empty
            recordset when neither is selected.
        """
        SD = self.env["general_audit_ws_a916660"]
        for record in self:
            result = []
            if record.data_mode == "gl" and record.general_ledger_id:
                result = SD.search(
                    [("general_ledger_id", "=", record.general_ledger_id.id)]
                )
            elif record.data_mode == "subledger" and record.subledger_id:
                result = SD.search([("subledger_id", "=", record.subledger_id.id)])
            record.allowed_sample_determination_ids = result

    # ── Onchange methods ─────────────────────────────────────────────────────

    @api.onchange("data_mode")
    def onchange_general_ledger_id(self):
        self.general_ledger_id = False

    @api.onchange("data_mode")
    def onchange_subledger_id(self):
        self.subledger_id = False

    @api.onchange("data_mode", "general_ledger_id", "subledger_id", "data_source")
    def onchange_sample_determination_id(self):
        """Reset ``sample_determination_id`` when its scoping changes.

        :return: nothing; clears ``sample_determination_id`` in-memory.
        """
        self.sample_determination_id = False
