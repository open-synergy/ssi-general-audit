# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io
import random

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class GeneralAuditWSe3f4a5b(models.Model):
    """
    Test of Control Worksheet (e3f4a5b).

    Main worksheet for Test of Control (ToC) procedures during the Fieldwork
    phase of an audit engagement. Manages the full attribute sampling workflow
    in accordance with AICPA standards, from population preparation through
    master sample generation cascaded to all control attributes.

    **Population Data Source**
    Population is sourced from either a General Ledger (``general_audit_ws_d209914``)
    or a Subledger (``general_audit_ws_b5e3d9f``) linked to the same audit
    engagement, controlled via ``data_mode``. ``raw_data`` is computed
    automatically from the selected source; ``population_count`` is derived
    from the number of non-empty data rows in ``raw_data``.

    **Sample Column Configuration**
    - ``ref_col_number``: column number in ``raw_data`` used to populate the
      Ref column of the master sample CSV (1-based).
    - ``note_col_number``: column number in ``raw_data`` used to pre-fill the
      Note column of the master sample CSV (1-based).

    **Generate Sample**
    ``action_generate_sample`` randomly selects (``random.sample``) up to
    ``sample_actual`` rows from ``raw_data`` — taken as the maximum
    ``sample_final`` across all attributes — writes the master CSV to
    ``sample_data``, then cascades to all attributes (``attribute_ids``)
    via ``attr.action_generate_sample()``.

    Control attributes being tested are represented by
    ``general_audit_ws_e3f4a5b.attribute``.

    Reference standard: ISA 330 / SA 330 — Auditor Responses to Assessed Risks.
    """

    _name = "general_audit_ws_e3f4a5b"
    _description = "Test of Control (e3f4a5b)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_test_of_control.worksheet_type_e3f4a5b"

    cycle_id = fields.Many2one(
        comodel_name="client_business_process",
        string="Cycle (Siklus)",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The business cycle or account cycle being tested (e.g. Penjualan, Pembelian).",
    )
    allowed_account_type_ids = fields.Many2many(
        comodel_name="client_account_type",
        related="general_audit_id.account_type_ids",
        string="Allowed Account Types",
        store=False,
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
        help="Standard account type related to this Test of Control.",
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
        help="The account related to this Test of Control.",
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
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The general ledger data used as population for this Test of Control.",
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
        help="The subledger data used as population for this Test of Control.",
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
    attribute_ids = fields.One2many(
        string="Attribute Sampling",
        comodel_name="general_audit_ws_e3f4a5b.attribute",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Attribute sampling plan and results per control attribute.",
    )
    population_count = fields.Integer(
        string="Population Count",
        compute="_compute_population_count",
        store=False,
        compute_sudo=True,
        help="Total number of items in the population (data rows from GL/Subledger).",
    )
    ref_col_number = fields.Integer(
        string="Ref Column Number",
        help="Column number from raw data for document reference (starting from 1).",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    note_col_number = fields.Integer(
        string="Note Column Number",
        help="Column number from raw data to pre-fill the Note column"
        " in sample data (starting from 1).",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    sample_actual = fields.Integer(
        string="Sample Actual",
        compute="_compute_sample_actual",
        store=True,
        compute_sudo=True,
        help="Maximum sample_final across all attributes.",
    )
    sample_data = fields.Text(
        string="Sample Data",
        help="CSV data of sampled items at worksheet level. "
        "Generated by 'Generate Sample' button.",
    )
    worksheet_result = fields.Text(
        string="Worksheet Result",
        help="Rich-text result or conclusion of this test of control procedure.",
    )

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
    def _compute_raw_data_title(self):
        for record in self:
            if record.data_mode == "gl" and record.general_ledger_id:
                record.raw_data_title = record.general_ledger_id.title
            elif record.data_mode == "subledger" and record.subledger_id:
                record.raw_data_title = record.subledger_id.title
            else:
                record.raw_data_title = False

    @api.depends("attribute_ids.sample_final")
    def _compute_sample_actual(self):
        for record in self:
            finals = record.attribute_ids.mapped("sample_final")
            record.sample_actual = max(finals) if finals else 0

    @api.depends("raw_data")
    def _compute_population_count(self):
        for record in self:
            count = 0
            if record.raw_data:
                reader = csv.reader(io.StringIO(record.raw_data))
                next(reader, None)  # skip header row
                for row in reader:
                    if row and any(cell.strip() for cell in row):
                        count += 1
            record.population_count = count

    @api.onchange("general_audit_id")
    def onchange_account_type_id(self):
        self.account_type_id = False

    @api.onchange("account_type_id")
    def onchange_account_id(self):
        self.account_id = False

    @api.onchange("data_mode", "account_type_id", "account_id")
    def onchange_general_ledger_id(self):
        self.general_ledger_id = False

    @api.onchange("data_mode", "account_type_id", "account_id")
    def onchange_subledger_id(self):
        self.subledger_id = False

    def action_generate_sample(self):
        self.ensure_one()
        if not self.raw_data:
            raise UserError(
                _("No raw data available. Please select a data source first.")
            )
        if self.sample_actual <= 0:
            raise UserError(
                _("Sample size is zero. Please configure attributes first.")
            )

        reader = csv.reader(io.StringIO(self.raw_data))
        header = next(reader, None)
        if not header:
            raise UserError(_("Raw data has no header row."))

        data_rows = []
        for idx, row in enumerate(reader, start=1):
            if row and any(cell.strip() for cell in row):
                data_rows.append((idx, row))

        if not data_rows:
            raise UserError(_("Raw data has no data rows."))

        n = min(self.sample_actual, len(data_rows))
        selected = sorted(random.sample(data_rows, n), key=lambda x: x[0])

        ref_col_header = "Document Ref"
        if self.ref_col_number and self.ref_col_number <= len(header):
            ref_col_header = header[self.ref_col_number - 1].strip() or ref_col_header

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Seq", "Item No", ref_col_header, "Note"])

        for seq, (item_no, row) in enumerate(selected, start=1):
            ref = ""
            if self.ref_col_number and self.ref_col_number <= len(row):
                ref = row[self.ref_col_number - 1].strip()

            note = ""
            if self.note_col_number and self.note_col_number <= len(row):
                note = row[self.note_col_number - 1].strip()

            writer.writerow([seq, item_no, ref, note])

        self.sample_data = output.getvalue()
        for attr in self.attribute_ids:
            attr.action_generate_sample()

    def action_open_attributes(self):
        self.ensure_one()
        action = self.env.ref(
            "ssi_general_audit_worksheet_test_of_control"
            ".general_audit_ws_e3f4a5b_attribute_action"
        ).read()[0]
        action["domain"] = [("worksheet_id", "=", self.id)]
        action["context"] = {"default_worksheet_id": self.id}
        return action
