# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io

from odoo import api, fields, models


class GeneralAuditWSe3f4a5b(models.Model):
    """
    Test of Control Worksheet (e3f4a5b).

    Worksheet pelaksanaan pengujian pengendalian (Test of Control / ToC)
    pada fase Fieldwork audit. Digunakan oleh auditor untuk mengevaluasi
    efektivitas operasional pengendalian internal klien melalui pendekatan
    attribute sampling statistis berbasis tabel AICPA.

    Setiap worksheet dikaitkan dengan satu siklus bisnis (business cycle)
    dan sumber data populasi (General Ledger atau Subledger). Atribut
    pengendalian yang diuji didefinisikan pada model
    ``general_audit_ws_e3f4a5b.attribute``.

    Referensi standar: ISA 330 / SA 330 — Auditor Responses to Assessed Risks.
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
    amount_col_number = fields.Integer(
        string="Amount Column Number",
        help="Column number from raw data for amount (starting from 1).",
        readonly=True,
        states={"open": [("readonly", False)]},
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

    def action_open_attributes(self):
        self.ensure_one()
        action = self.env.ref(
            "ssi_general_audit_worksheet_test_of_control"
            ".general_audit_ws_e3f4a5b_attribute_action"
        ).read()[0]
        action["domain"] = [("worksheet_id", "=", self.id)]
        action["context"] = {"default_worksheet_id": self.id}
        return action
