# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io
import math
import random

from odoo import api, fields, models

RELIABILITY_FACTOR_TABLE = {
    "80": 1.61,
    "90": 2.31,
    "95": 3.00,
}


class GeneralAuditWSa916660(models.Model):
    _name = "general_audit_ws_a916660"
    _description = "Test of Detail (a916660)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_test_of_detail." "worksheet_type_a916660"
    )

    # --- Data Mode fields ---
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
        help="The general ledger data used as population for this test of detail.",
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
        help="The subledger data used as population for this test of detail.",
    )
    raw_data = fields.Text(
        string="Raw Data",
        compute="_compute_raw_data",
        store=False,
        compute_sudo=True,
    )

    # --- Column configuration ---
    identifier_col_number = fields.Integer(
        string="Identifier Column",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The identifier column number (1-based) in the raw data.",
    )
    monetary_col_number = fields.Integer(
        string="Monetary Column Number",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The monetary column number (1-based) in the raw data.",
    )
    additional_info_col_number = fields.Integer(
        string="Additional Info Column Number",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The additional information column number (1-based) in the raw data.",
    )

    # --- Population statistics ---
    population_count = fields.Integer(
        string="Population Count",
        compute="_compute_population_count",
        store=True,
        compute_sudo=True,
        help="The total number of items in the population.",
    )
    population_amount = fields.Monetary(
        string="Population Amount",
        currency_field="currency_id",
        compute="_compute_population_amount",
        store=True,
        compute_sudo=True,
        help="The total monetary amount of the population.",
    )

    # --- Key item (100% examination) ---
    key_item_count = fields.Integer(
        string="Key Item Count",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The number of key items selected for 100%% examination.",
    )
    key_item_amount = fields.Monetary(
        string="Key Item Amount",
        currency_field="currency_id",
        compute="_compute_key_item_amount",
        store=True,
        compute_sudo=True,
        help="The total monetary amount of key items selected for 100%% examination.",
    )

    # --- Sample statistics ---
    sample_count = fields.Integer(
        string="Sample Count",
        compute="_compute_sample_count",
        store=True,
        compute_sudo=True,
        help="The number of items in the sample pool (excluding key items).",
    )
    sample_amount = fields.Monetary(
        string="Sample Amount",
        currency_field="currency_id",
        compute="_compute_sample_amount",
        store=True,
        compute_sudo=True,
        help="The total monetary amount of the sample pool (excluding key items).",
    )

    # --- Sampling output ---
    sampling_data = fields.Text(
        string="Sampling Data",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The result of Monetary Unit Sampling. "
        "Contains key items (100%% examination) and MUS-selected sample items.",
    )

    # --- MUS Parameters ---
    confidence_level = fields.Selection(
        string="Confidence Level",
        selection=[
            ("80", "80%"),
            ("90", "90%"),
            ("95", "95%"),
        ],
        default="95",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Confidence level for Monetary Unit Sampling.",
    )
    tolerable_misstatement = fields.Monetary(
        string="Tolerable Misstatement",
        currency_field="currency_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Maximum monetary misstatement acceptable for this account.",
    )
    reliability_factor = fields.Float(
        string="Reliability Factor",
        compute="_compute_reliability_factor",
        store=True,
        compute_sudo=True,
        digits=(12, 4),
        help="Statistical reliability factor based on confidence level. "
        "R = -ln(1 - confidence_level).",
    )
    sampling_interval = fields.Monetary(
        string="Sampling Interval",
        currency_field="currency_id",
        compute="_compute_sampling_interval",
        store=True,
        compute_sudo=True,
        help="Sampling interval = Tolerable Misstatement / Reliability Factor.",
    )
    computed_sample_size = fields.Integer(
        string="MUS Sample Size",
        compute="_compute_computed_sample_size",
        store=True,
        compute_sudo=True,
        help="Number of sample items to select from the sample pool using MUS.",
    )

    # --- Compute methods ---

    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_general_ledger_ids(self):
        GL = self.env["general_audit_ws_d209914"]
        for record in self:
            record.allowed_general_ledger_ids = False
            if record.general_audit_id:
                record.allowed_general_ledger_ids = GL.search(
                    [
                        ("general_audit_id", "=", record.general_audit_id.id),
                    ]
                )

    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_subledger_ids(self):
        SL = self.env["general_audit_ws_b5e3d9f"]
        for record in self:
            record.allowed_subledger_ids = False
            if record.general_audit_id:
                record.allowed_subledger_ids = SL.search(
                    [
                        ("general_audit_id", "=", record.general_audit_id.id),
                    ]
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
        "general_ledger_id.raw_data",
        "subledger_id.raw_data",
    )
    def _compute_population_count(self):
        for record in self:
            raw_data = record._get_source_raw_data()
            if raw_data:
                try:
                    reader = csv.reader(io.StringIO(raw_data))
                    count = sum(1 for _ in reader) - 1
                    record.population_count = max(0, count)
                except Exception:
                    record.population_count = 0
            else:
                record.population_count = 0

    @api.depends(
        "data_mode",
        "general_ledger_id.raw_data",
        "general_ledger_id.thousand_separator",
        "general_ledger_id.decimal_separator",
        "subledger_id.raw_data",
        "subledger_id.thousand_separator",
        "subledger_id.decimal_separator",
        "monetary_col_number",
    )
    def _compute_population_amount(self):
        for record in self:
            total_amount = 0.0
            raw_data = record._get_source_raw_data()
            col_number = record.monetary_col_number

            if raw_data and col_number:
                thousand_sep, decimal_sep = record._get_separators()
                try:
                    reader = csv.reader(io.StringIO(raw_data))
                    for index, row in enumerate(reader):
                        if index == 0:
                            continue
                        if len(row) < col_number:
                            continue
                        total_amount += record._parse_monetary_value(
                            row[col_number - 1], thousand_sep, decimal_sep
                        )
                except Exception:
                    total_amount = 0.0

            record.population_amount = total_amount

    @api.depends(
        "data_mode",
        "general_ledger_id.raw_data",
        "general_ledger_id.thousand_separator",
        "general_ledger_id.decimal_separator",
        "subledger_id.raw_data",
        "subledger_id.thousand_separator",
        "subledger_id.decimal_separator",
        "monetary_col_number",
        "key_item_count",
    )
    def _compute_key_item_amount(self):
        for record in self:
            raw_data = record._get_source_raw_data()
            col_number = record.monetary_col_number
            key_count = record.key_item_count or 0
            amounts = []

            if raw_data and col_number and key_count > 0:
                thousand_sep, decimal_sep = record._get_separators()
                try:
                    reader = csv.reader(io.StringIO(raw_data))
                    for index, row in enumerate(reader):
                        if index == 0:
                            continue
                        if len(row) < col_number:
                            continue
                        amounts.append(
                            record._parse_monetary_value(
                                row[col_number - 1], thousand_sep, decimal_sep
                            )
                        )
                except Exception:
                    amounts = []

            amounts.sort(reverse=True)
            record.key_item_amount = sum(amounts[:key_count]) if amounts else 0.0

    @api.depends("population_count", "key_item_count")
    def _compute_sample_count(self):
        for record in self:
            record.sample_count = record.population_count - (record.key_item_count or 0)

    @api.depends("population_amount", "key_item_amount")
    def _compute_sample_amount(self):
        for record in self:
            record.sample_amount = record.population_amount - record.key_item_amount

    @api.depends("confidence_level")
    def _compute_reliability_factor(self):
        for record in self:
            record.reliability_factor = RELIABILITY_FACTOR_TABLE.get(
                record.confidence_level, 0.0
            )

    @api.depends("tolerable_misstatement", "reliability_factor")
    def _compute_sampling_interval(self):
        for record in self:
            if record.reliability_factor > 0:
                record.sampling_interval = (
                    record.tolerable_misstatement / record.reliability_factor
                )
            else:
                record.sampling_interval = 0.0

    @api.depends("sample_amount", "sampling_interval")
    def _compute_computed_sample_size(self):
        for record in self:
            if record.sampling_interval > 0:
                record.computed_sample_size = math.ceil(
                    record.sample_amount / record.sampling_interval
                )
            else:
                record.computed_sample_size = 0

    # --- Onchange methods ---

    @api.onchange("data_mode")
    def onchange_general_ledger_id(self):
        self.general_ledger_id = False

    @api.onchange("data_mode")
    def onchange_subledger_id(self):
        self.subledger_id = False

    # --- Helper methods ---

    def _get_source_raw_data(self):
        self.ensure_one()
        if self.data_mode == "gl" and self.general_ledger_id:
            return self.general_ledger_id.raw_data
        elif self.data_mode == "subledger" and self.subledger_id:
            return self.subledger_id.raw_data
        return False

    def _get_separators(self):
        self.ensure_one()
        source = False
        if self.data_mode == "gl" and self.general_ledger_id:
            source = self.general_ledger_id
        elif self.data_mode == "subledger" and self.subledger_id:
            source = self.subledger_id
        if source:
            return (
                source.thousand_separator or ",",
                source.decimal_separator or ".",
            )
        return (",", ".")

    @staticmethod
    def _parse_monetary_value(cell_value, thousand_sep=",", decimal_sep="."):
        raw_val = cell_value.strip()
        if raw_val.startswith("(") and raw_val.endswith(")"):
            raw_val = "-" + raw_val[1:-1]
        raw_val = raw_val.replace(thousand_sep, "")
        if decimal_sep != ".":
            raw_val = raw_val.replace(decimal_sep, ".")
        try:
            return float(raw_val) if raw_val else 0.0
        except ValueError:
            return 0.0

    # --- Action methods ---

    def action_generate_sampling(self):
        for record in self.sudo():
            record._generate_sampling()

    def _build_unique_columns(self, identifier_col, monetary_col, info_col):
        columns = [c for c in [identifier_col, monetary_col, info_col] if c and c > 0]
        unique_columns = []
        for c in columns:
            if c not in unique_columns:
                unique_columns.append(c)
        return unique_columns

    def _build_items_from_csv(self, all_rows, unique_columns, monetary_col):
        source_header = all_rows[0]
        source_data = all_rows[1:]
        thousand_sep, decimal_sep = self._get_separators()
        output_header_parts = [
            source_header[col - 1] if len(source_header) >= col else ""
            for col in unique_columns
        ]
        output_header = ["Index"] + output_header_parts + ["Type"]
        items = []
        for idx, row in enumerate(source_data):
            selected = [
                row[col - 1] if len(row) >= col else "" for col in unique_columns
            ]
            amount = self._parse_monetary_value(
                row[monetary_col - 1] if len(row) >= monetary_col else "",
                thousand_sep,
                decimal_sep,
            )
            items.append({"index": idx, "cells": selected, "amount": amount})
        return output_header, items

    def _perform_mus_sampling(self, items, key_count, sample_interval):
        sorted_by_amount = sorted(items, key=lambda x: x["amount"], reverse=True)
        key_item_indices = {item["index"] for item in sorted_by_amount[:key_count]}
        sample_pool = [item for item in items if item["index"] not in key_item_indices]
        total_sample_amount = sum(item["amount"] for item in sample_pool)
        sample_size = (
            math.ceil(total_sample_amount / sample_interval)
            if total_sample_amount > 0
            else 0
        )
        mus_selected_indices = set()
        if sample_interval > 0 and sample_size > 0 and total_sample_amount > 0:
            random_start = random.uniform(0, sample_interval)
            thresholds = [
                random_start + i * sample_interval for i in range(sample_size)
            ]
            cumulative = 0.0
            threshold_idx = 0
            for item in sample_pool:
                cumulative += item["amount"]
                while (
                    threshold_idx < len(thresholds)
                    and thresholds[threshold_idx] < cumulative
                ):
                    mus_selected_indices.add(item["index"])
                    threshold_idx += 1
                if threshold_idx >= len(thresholds):
                    break
        return sorted_by_amount, mus_selected_indices

    def _generate_sampling(self):
        self.ensure_one()
        raw_data = self._get_source_raw_data()
        if not raw_data:
            self.sampling_data = False
            return
        monetary_col = self.monetary_col_number
        identifier_col = self.identifier_col_number
        info_col = self.additional_info_col_number
        if not monetary_col:
            self.sampling_data = False
            return
        unique_columns = self._build_unique_columns(
            identifier_col, monetary_col, info_col
        )
        if not unique_columns:
            self.sampling_data = False
            return
        sample_interval = self.sampling_interval
        if sample_interval <= 0:
            self.sampling_data = False
            return
        try:
            reader = csv.reader(io.StringIO(raw_data))
            all_rows = list(reader)
            if len(all_rows) < 2:
                self.sampling_data = False
                return
            output_header, items = self._build_items_from_csv(
                all_rows, unique_columns, monetary_col
            )
            key_count = self.key_item_count or 0
            sorted_by_amount, mus_selected_indices = self._perform_mus_sampling(
                items, key_count, sample_interval
            )
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(output_header)
            for item in sorted_by_amount[:key_count]:
                writer.writerow([str(item["index"])] + item["cells"] + ["Key Item"])
            for item in items:
                if item["index"] in mus_selected_indices:
                    writer.writerow([str(item["index"])] + item["cells"] + ["Sample"])
            self.sampling_data = output.getvalue()
        except Exception:
            self.sampling_data = False
