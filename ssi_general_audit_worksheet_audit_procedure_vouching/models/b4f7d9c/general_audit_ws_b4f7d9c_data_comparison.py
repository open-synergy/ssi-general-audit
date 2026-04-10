# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSb4f7d9cDataComparison(models.Model):
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
    raw_data = fields.Text(
        string="Raw Data",
        compute="_compute_raw_data",
        store=False,
        compute_sudo=True,
        help="Raw CSV data from the selected General Ledger or Subledger.",
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

    # ── Onchange methods ─────────────────────────────────────────────────────

    @api.onchange("data_mode")
    def onchange_general_ledger_id(self):
        self.general_ledger_id = False

    @api.onchange("data_mode")
    def onchange_subledger_id(self):
        self.subledger_id = False
