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


class GeneralAuditWsA916660(models.Model):
    """
    Sample Determination worksheet: computes Monetary Unit Sampling (MUS)
    parameters from a General Ledger or Subledger population, and selects
    the key items (100% examination) and MUS sample items to test.
    """

    _name = "general_audit_ws_a916660"
    _description = "Sample Determination (a916660)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_sample_determination." "worksheet_type_a916660"
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
        help="The general ledger data used as population for this sample determination.",
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
        help="The subledger data used as population for this sample determination.",
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
        """Restrict the General Ledger picker to the current audit.

        :return: sets ``allowed_general_ledger_ids`` to the
            ``general_audit_ws_d209914`` records sharing this record's
            ``general_audit_id``, or an empty recordset when unset.
        """
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
        """Restrict the Subledger picker to the current audit.

        :return: sets ``allowed_subledger_ids`` to the
            ``general_audit_ws_b5e3d9f`` records sharing this record's
            ``general_audit_id``, or an empty recordset when unset.
        """
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
        """Mirror the raw CSV data from the selected GL or Subledger source.

        :return: sets ``raw_data`` to the source record's ``raw_data``
            according to ``data_mode``, or ``False`` when no source is
            selected.
        """
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
        """Count the data rows (excluding header) in the source raw data.

        :return: sets ``population_count`` to the row count, or ``0`` when
            the source has no data or fails to parse as CSV.
        """
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
        """Sum the monetary column across every data row of the population.

        :return: sets ``population_amount`` to the sum, or ``0.0`` when the
            source has no data, ``monetary_col_number`` is unset, or the
            data fails to parse.
        """
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
        """Sum the ``key_item_count`` largest monetary amounts in the data.

        :return: sets ``key_item_amount`` to the sum of the top
            ``key_item_count`` row amounts (100% examination items), or
            ``0.0`` when the data is missing or ``key_item_count`` is 0.
        """
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
        """Derive the sample pool size (population minus key items).

        :return: sets ``sample_count`` to ``population_count -
            key_item_count``.
        """
        for record in self:
            record.sample_count = record.population_count - (record.key_item_count or 0)

    @api.depends("population_amount", "key_item_amount")
    def _compute_sample_amount(self):
        """Derive the sample pool amount (population minus key items).

        :return: sets ``sample_amount`` to ``population_amount -
            key_item_amount``.
        """
        for record in self:
            record.sample_amount = record.population_amount - record.key_item_amount

    @api.depends("confidence_level")
    def _compute_reliability_factor(self):
        """Look up the MUS reliability factor for the chosen confidence level.

        :return: sets ``reliability_factor`` from
            ``RELIABILITY_FACTOR_TABLE``, or ``0.0`` when
            ``confidence_level`` is unset.
        """
        for record in self:
            record.reliability_factor = RELIABILITY_FACTOR_TABLE.get(
                record.confidence_level, 0.0
            )

    @api.depends("tolerable_misstatement", "reliability_factor")
    def _compute_sampling_interval(self):
        """Derive the MUS sampling interval.

        :return: sets ``sampling_interval`` to ``tolerable_misstatement /
            reliability_factor``, or ``0.0`` when ``reliability_factor`` is
            not positive.
        """
        for record in self:
            if record.reliability_factor > 0:
                record.sampling_interval = (
                    record.tolerable_misstatement / record.reliability_factor
                )
            else:
                record.sampling_interval = 0.0

    @api.depends("sample_amount", "sampling_interval")
    def _compute_computed_sample_size(self):
        """Derive the number of MUS sample items to select from the pool.

        :return: sets ``computed_sample_size`` to ``ceil(sample_amount /
            sampling_interval)``, or ``0`` when ``sampling_interval`` is not
            positive.
        """
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
        """Resolve the raw CSV data of the currently selected source.

        :return: the ``raw_data`` of ``general_ledger_id`` or
            ``subledger_id`` according to ``data_mode``, or ``False`` when
            no source is selected.
        """
        self.ensure_one()
        if self.data_mode == "gl" and self.general_ledger_id:
            return self.general_ledger_id.raw_data
        elif self.data_mode == "subledger" and self.subledger_id:
            return self.subledger_id.raw_data
        return False

    def _get_separators(self):
        """Resolve the thousand/decimal separators of the source data.

        :return: a ``(thousand_separator, decimal_separator)`` tuple from
            the selected GL/Subledger source, defaulting to ``(",", ".")``
            when no source is selected.
        """
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
        """Parse a raw CSV cell into a float monetary amount.

        Handles parenthesized negatives (``(100)`` -> ``-100``) and
        locale-specific thousand/decimal separators.

        :param cell_value: raw cell text from the CSV.
        :param thousand_sep: thousand separator used in ``cell_value``.
        :param decimal_sep: decimal separator used in ``cell_value``.
        :return: the parsed amount, or ``0.0`` when ``cell_value`` is empty
            or not a valid number.
        """
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
        """Run Monetary Unit Sampling and store the result in ``sampling_data``.

        :return: ``None``. Delegates to ``_generate_sampling`` for each
            record, run with sudo rights.
        """
        for record in self.sudo():
            record._generate_sampling()

    def _build_unique_columns(self, identifier_col, monetary_col, info_col):
        """Build the deduplicated, ordered list of columns to export.

        :param identifier_col: 1-based identifier column number, or falsy.
        :param monetary_col: 1-based monetary column number, or falsy.
        :param info_col: 1-based additional-info column number, or falsy.
        :return: list of distinct positive column numbers, in the order
            identifier/monetary/info, skipping unset or duplicate columns.
        """
        columns = [c for c in [identifier_col, monetary_col, info_col] if c and c > 0]
        unique_columns = []
        for c in columns:
            if c not in unique_columns:
                unique_columns.append(c)
        return unique_columns

    def _build_items_from_csv(self, all_rows, unique_columns, monetary_col):
        """Extract the selected columns and monetary amount from each row.

        :param all_rows: parsed CSV rows, header included at index 0.
        :param unique_columns: 1-based column numbers to keep, from
            ``_build_unique_columns``.
        :param monetary_col: 1-based monetary column number used to derive
            each item's amount.
        :return: a ``(output_header, items)`` tuple, where ``output_header``
            is ``["Index", ...selected column labels..., "Type"]`` and
            ``items`` is a list of ``{"index", "cells", "amount"}`` dicts,
            one per data row.
        """
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
        """Select key items and MUS sample items from the population items.

        Sorts items by amount descending, treats the top ``key_count`` as
        key items (100% examination) removed from the sampling pool, then
        walks the remaining pool with a random-start systematic selection
        at ``sample_interval`` to pick the MUS sample.

        :param items: list of ``{"index", "cells", "amount"}`` dicts, as
            produced by ``_build_items_from_csv``.
        :param key_count: number of largest-amount items to treat as key
            items.
        :param sample_interval: MUS sampling interval; must be positive for
            any sample item to be selected.
        :return: a ``(sorted_by_amount, mus_selected_indices)`` tuple:
            all items sorted by amount descending, and the set of item
            ``index`` values selected as MUS samples (excluding key items).
        """
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
        """Build ``sampling_data`` (key items + MUS sample) as a CSV string.

        Reads the source raw data, extracts the configured columns, then
        delegates the key item / MUS selection to ``_perform_mus_sampling``
        and writes the result (key items first, tagged ``Key Item``, then
        MUS-selected items tagged ``Sample``) to ``sampling_data``.

        :return: ``None``. Sets ``sampling_data`` to ``False`` when the
            source, column configuration, or sampling interval is
            incomplete, or when parsing the source data fails.
        """
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
