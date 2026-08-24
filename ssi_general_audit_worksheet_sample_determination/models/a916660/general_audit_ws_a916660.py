# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io
import math
import random
import re
import sqlite3

from odoo import _, api, fields, models
from odoo.exceptions import UserError

# Forbidden SQL keywords for `filter_where_clause` (mutating/DDL statements);
# only a read-only WHERE clause against the in-memory candidate table is
# allowed. Mirrors `general_audit_ws_d45dd19.confirmation._apply_where_clause`.
_FORBIDDEN_SQL = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|DETACH"
    r"|REPLACE|PRAGMA|REINDEX|VACUUM|SAVEPOINT|RELEASE"
    r"|BEGIN|COMMIT|ROLLBACK)\b",
    re.IGNORECASE,
)

RELIABILITY_FACTOR_TABLE = {
    "80": 1.61,
    "90": 2.31,
    "95": 3.00,
}

# Confidence-coefficient lookup table, keyed by each risk figure's own
# percentage value. Both dicts encode the same 13-row reliability table
# (Confidence Level / ARIA% / ARIR% / Coefficient); ARIA and ARIR are
# looked up independently because a user may pick different percentages
# for each, landing on different rows.
ARIA_COEFFICIENT_TABLE = {
    "0.5": 2.58,
    "2.5": 1.96,
    "5": 1.64,
    "10": 1.28,
    "12.5": 1.15,
    "15": 1.04,
    "20": 0.84,
    "25": 0.67,
    "30": 0.52,
    "35": 0.39,
    "40": 0.25,
    "45": 0.13,
    "50": 0.0,
}
ARIR_COEFFICIENT_TABLE = {
    "1": 2.58,
    "5": 1.96,
    "10": 1.64,
    "20": 1.28,
    "25": 1.15,
    "30": 1.04,
    "40": 0.84,
    "50": 0.67,
    "60": 0.52,
    "70": 0.39,
    "80": 0.25,
    "90": 0.13,
    "100": 0.0,
}
ARIA_SELECTION = [(k, "{}%".format(k)) for k in ARIA_COEFFICIENT_TABLE]
ARIR_SELECTION = [(k, "{}%".format(k)) for k in ARIR_COEFFICIENT_TABLE]


class GeneralAuditWsA916660(models.Model):
    """
    Sample Determination worksheet: computes the sample size from a General
    Ledger or Subledger population using one of three methods (Monetary
    Unit Sampling, Classical Variable Sampling, or Non-Statistical
    Sampling), and selects the key items (100% examination) and sample
    items to test.
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
        help="The final result of the sample determination: key items "
        "(100%% examination) and the selected/chosen sample items. For "
        "Non-Statistical Sampling, every remaining item starts out listed "
        "as a 'Candidate'; use the 'Sampling Process' tab to choose which "
        "candidates become 'Sample'. Always read-only here -- for NSS, "
        "edit via 'Sampling Process' instead.",
    )
    sampling_process_filter = fields.Text(
        string="Filter (WHERE clause)",
        help="Optional SQL WHERE clause to narrow down the candidates shown "
        "in 'Sampling Process' -- useful when the population is large. "
        "Use column names from the table header; spaces and special "
        "characters are replaced by underscores.\n"
        "Example: Additional_Info LIKE '%%FRONT WALL%%'",
    )
    sampling_process_data = fields.Text(
        string="Sampling Process Data",
        compute="_compute_sampling_process_data",
        inverse="_inverse_sampling_process_data",
        store=False,
        compute_sudo=True,
        help="Non-Statistical Sampling only: the 'Candidate' rows of "
        "``sampling_data`` (optionally narrowed by "
        "``sampling_process_filter``), each with a 'Chose?' checkbox. "
        "Check it to promote a candidate to 'Sample'; uncheck to send a "
        "'Sample' back to 'Candidate'. Key items are not shown here -- "
        "they are always chosen automatically and are not affected by "
        "this tab.",
    )

    # --- Method selection ---
    method_type = fields.Selection(
        string="Sampling Method",
        selection=[
            ("mus", "Monetary Unit Sampling"),
            ("cvs", "Classical Variable Sampling"),
            ("nss", "Non-Statistical Sampling"),
        ],
        required=True,
        default="mus",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Statistical method used to determine the sample size and "
        "select the sample items.",
    )

    # --- MUS parameters (Monetary Unit Sampling) ---
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
        digits=(12, 4),
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Statistical reliability factor based on confidence level. "
        "Auto-filled from Confidence Level when it changes, but can be "
        "overridden.",
    )
    sampling_interval = fields.Monetary(
        string="Sampling Interval",
        currency_field="currency_id",
        compute="_compute_sampling_interval",
        store=True,
        compute_sudo=True,
        help="Sampling interval = Tolerable Misstatement / Reliability Factor.",
    )

    # --- Input Variabel: shared by all three sampling methods ---
    performance_materiality = fields.Monetary(
        string="Performance Materiality",
        currency_field="currency_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Performance materiality for this account. Used to derive "
        "``Tolerable Misstatement`` (= Performance Materiality x Risk "
        "Factor).",
    )
    risk_factor = fields.Float(
        string="Risk Factor",
        digits=(3, 2),
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Combined audit risk factor, used to derive ``Tolerable "
        "Misstatement``.",
    )

    # --- CVS / NSS parameters (Classical Variable / Non-Statistical Sampling) ---
    aria = fields.Selection(
        string="ARIA (%)",
        selection=ARIA_SELECTION,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Acceptable Risk of Incorrect Acceptance, for Classical "
        "Variable / Non-Statistical Sampling.",
    )
    arir = fields.Selection(
        string="ARIR (%)",
        selection=ARIR_SELECTION,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Acceptable Risk of Incorrect Rejection, for Classical "
        "Variable / Non-Statistical Sampling.",
    )
    aria_coefficient = fields.Float(
        string="ARIA Coefficient",
        compute="_compute_aria_coefficient",
        store=True,
        compute_sudo=True,
        digits=(12, 4),
        help="Confidence coefficient looked up from the reliability table "
        "for the chosen ARIA.",
    )
    arir_coefficient = fields.Float(
        string="ARIR Coefficient",
        compute="_compute_arir_coefficient",
        store=True,
        compute_sudo=True,
        digits=(12, 4),
        help="Confidence coefficient looked up from the reliability table "
        "for the chosen ARIR.",
    )
    estimate_misstatement_ratio = fields.Float(
        string="Estimate Misstatement Ratio",
        digits=(3, 2),
        default=0.55,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="``Estimate Misstatement`` = Tolerable Misstatement x this "
        "ratio, for Classical Variable / Non-Statistical Sampling.",
    )
    standard_deviation_ratio = fields.Float(
        string="Standard Deviation Ratio",
        digits=(5, 4),
        default=0.013,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="``Standard Deviation Estimate`` = Estimate Misstatement x "
        "this ratio, for Classical Variable / Non-Statistical Sampling.",
    )
    estimate_misstatement = fields.Monetary(
        string="Estimate Misstatement",
        currency_field="currency_id",
        compute="_compute_estimate_misstatement",
        store=True,
        compute_sudo=True,
        help="Estimate Misstatement = Tolerable Misstatement x Estimate "
        "Misstatement Ratio.",
    )
    standard_deviation_estimate = fields.Monetary(
        string="Standard Deviation Estimate",
        currency_field="currency_id",
        compute="_compute_standard_deviation_estimate",
        store=True,
        compute_sudo=True,
        help="Standard Deviation Estimate = Estimate Misstatement x "
        "Standard Deviation Ratio.",
    )
    nss_final_sample_size = fields.Integer(
        string="Final Sample Size (Judgment)",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Optional manual override of the statistically computed "
        "sample size, based on professional judgment. Non-Statistical "
        "Sampling only; leave empty to use the computed size as-is.",
    )

    # --- Sampling output size ---
    computed_sample_size = fields.Integer(
        string="Computed Sample Size",
        compute="_compute_computed_sample_size",
        store=True,
        compute_sudo=True,
        help="Number of sample items to select from the sample pool, "
        "using the chosen sampling method.",
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

    @api.depends("aria")
    def _compute_aria_coefficient(self):
        """Look up the confidence coefficient for the chosen ARIA.

        :return: sets ``aria_coefficient`` from ``ARIA_COEFFICIENT_TABLE``,
            or ``0.0`` when ``aria`` is unset.
        """
        for record in self:
            record.aria_coefficient = ARIA_COEFFICIENT_TABLE.get(record.aria, 0.0)

    @api.depends("arir")
    def _compute_arir_coefficient(self):
        """Look up the confidence coefficient for the chosen ARIR.

        :return: sets ``arir_coefficient`` from ``ARIR_COEFFICIENT_TABLE``,
            or ``0.0`` when ``arir`` is unset.
        """
        for record in self:
            record.arir_coefficient = ARIR_COEFFICIENT_TABLE.get(record.arir, 0.0)

    @api.depends("tolerable_misstatement", "estimate_misstatement_ratio")
    def _compute_estimate_misstatement(self):
        """Derive the CVS/NSS estimate misstatement.

        :return: sets ``estimate_misstatement`` to ``tolerable_misstatement
            x estimate_misstatement_ratio``.
        """
        for record in self:
            record.estimate_misstatement = (
                record.tolerable_misstatement * record.estimate_misstatement_ratio
            )

    @api.depends("estimate_misstatement", "standard_deviation_ratio")
    def _compute_standard_deviation_estimate(self):
        """Derive the CVS/NSS standard deviation estimate.

        :return: sets ``standard_deviation_estimate`` to
            ``estimate_misstatement x standard_deviation_ratio``.
        """
        for record in self:
            record.standard_deviation_estimate = (
                record.estimate_misstatement * record.standard_deviation_ratio
            )

    @api.depends(
        "method_type",
        "sample_amount",
        "sampling_interval",
        "population_count",
        "performance_materiality",
        "estimate_misstatement",
        "standard_deviation_estimate",
        "aria_coefficient",
        "arir_coefficient",
        "nss_final_sample_size",
    )
    def _compute_computed_sample_size(self):
        """Derive the number of sample items to select from the pool.

        Branches by ``method_type``: MUS divides the sample pool amount by
        the sampling interval; CVS/NSS use the classical variables
        sampling size formula (see ``_compute_cvs_sample_size``). NSS additionally
        lets ``nss_final_sample_size`` override the statistically computed
        size with a professional-judgment figure.

        :return: sets ``computed_sample_size``, or ``0`` when the method's
            required inputs are incomplete.
        """
        for record in self:
            result = 0
            if record.method_type == "mus":
                if record.sampling_interval > 0:
                    result = math.ceil(record.sample_amount / record.sampling_interval)
            elif record.method_type in ("cvs", "nss"):
                result = record._compute_cvs_sample_size()
                if record.method_type == "nss" and record.nss_final_sample_size:
                    result = record.nss_final_sample_size
            record.computed_sample_size = result

    def _compute_cvs_sample_size(self):
        """Compute the Classical Variable Sampling sample size.

        Formula: ``ROUNDUP(((StdDev x (ARIA_coef + ARIR_coef) x
        PopulationCount) / (PerformanceMateriality - EstimateMisstatement))
        ^ 2)``. Shared by CVS and NSS (NSS may override the result via
        ``nss_final_sample_size``).

        :return: the computed sample size, or ``0`` when
            ``performance_materiality`` does not exceed
            ``estimate_misstatement``, or ``population_count`` is 0.
        """
        self.ensure_one()
        denominator = self.performance_materiality - self.estimate_misstatement
        if denominator <= 0 or self.population_count <= 0:
            return 0
        ratio = (
            self.standard_deviation_estimate
            * (self.aria_coefficient + self.arir_coefficient)
            * self.population_count
        ) / denominator
        return math.ceil(ratio**2)

    # --- Onchange methods ---

    @api.onchange("data_mode")
    def onchange_general_ledger_id(self):
        self.general_ledger_id = False

    @api.onchange("data_mode")
    def onchange_subledger_id(self):
        self.subledger_id = False

    @api.onchange("performance_materiality", "risk_factor")
    def onchange_tolerable_misstatement(self):
        self.tolerable_misstatement = self.performance_materiality * self.risk_factor

    @api.onchange("confidence_level")
    def onchange_reliability_factor(self):
        if self.confidence_level:
            self.reliability_factor = RELIABILITY_FACTOR_TABLE.get(
                self.confidence_level, 0.0
            )

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
        """Run sample determination and store the result in ``sampling_data``.

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
            is ``["Index", ...selected column labels..., "Type"]`` (plus a
            trailing ``"Chose?"`` column for Non-Statistical Sampling) and
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
        if self.method_type == "nss":
            output_header = output_header + ["Chose?"]
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

        The random start is drawn from ``[0, remainder)`` rather than the
        full ``[0, sample_interval)`` range, where ``remainder`` is
        ``total_sample_amount`` modulo ``sample_interval`` (or the full
        interval when the amount is an exact multiple of it). This is the
        sub-range of start values that walks to exactly ``sample_size``
        hits, so "Realized to sampling" always matches "Total Plan
        Examination" -- drawing from the full interval could land past the
        last item's cumulative amount and silently drop the final hit.

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
            remainder = total_sample_amount % sample_interval or sample_interval
            random_start = random.uniform(0, remainder)
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

    def _perform_simple_random_sample(self, items, key_count, sample_size):
        """Select an unweighted random sample from the pool.

        Unlike Monetary Unit Sampling, Classical Variable Sampling draws a
        plain random sample: every item remaining after key items are
        removed has an equal chance of selection, independent of its
        amount.

        :param items: list of ``{"index", "cells", "amount"}`` dicts, as
            produced by ``_build_items_from_csv``.
        :param key_count: number of largest-amount items to treat as key
            items (excluded from the random draw).
        :param sample_size: number of items to randomly select from the
            pool; capped to the pool size when larger.
        :return: a ``(sorted_by_amount, selected_indices)`` tuple, in the
            same shape as ``_perform_mus_sampling``'s return value.
        """
        sorted_by_amount = sorted(items, key=lambda x: x["amount"], reverse=True)
        key_item_indices = {item["index"] for item in sorted_by_amount[:key_count]}
        sample_pool = [item for item in items if item["index"] not in key_item_indices]
        draw_size = min(sample_size, len(sample_pool))
        selected_indices = set()
        if draw_size > 0:
            selected_items = random.sample(sample_pool, draw_size)
            selected_indices = {item["index"] for item in selected_items}
        return sorted_by_amount, selected_indices

    def _perform_nss_candidate_list(self, items, key_count):
        """List every non-key item as a manual-selection candidate.

        Non-Statistical Sampling does not select items automatically
        (unlike MUS/CVS): the source spreadsheet marks each candidate row
        by hand (a manually-typed ``Choose? = Yes`` column, not a
        formula). This method mirrors that: every item remaining after key
        items are removed is returned as a candidate, tagged
        ``Candidate`` rather than ``Sample`` by the caller, for the
        auditor to mark by professional judgment -- e.g. by retyping the
        ``Type`` cell to ``Sample`` in the editable table view
        (``ssi_web_widget_csv_table``, "Table" edit mode).

        :param items: list of ``{"index", "cells", "amount"}`` dicts, as
            produced by ``_build_items_from_csv``.
        :param key_count: number of largest-amount items to treat as key
            items (excluded from the candidate list).
        :return: a ``(sorted_by_amount, candidate_indices)`` tuple, in the
            same shape as ``_perform_mus_sampling``'s return value.
        """
        sorted_by_amount = sorted(items, key=lambda x: x["amount"], reverse=True)
        key_item_indices = {item["index"] for item in sorted_by_amount[:key_count]}
        candidate_indices = {
            item["index"] for item in items if item["index"] not in key_item_indices
        }
        return sorted_by_amount, candidate_indices

    def _is_sampling_ready(self):
        """Check whether the current method's inputs allow item selection.

        :return: ``True`` when MUS has a positive ``sampling_interval``,
            CVS has a positive ``computed_sample_size``, or NSS has a
            non-empty sample pool (``sample_count``). ``False`` otherwise.
        """
        self.ensure_one()
        if self.method_type == "mus":
            return self.sampling_interval > 0
        if self.method_type == "cvs":
            return self.computed_sample_size > 0
        return self.sample_count > 0

    def _select_sampling_items(self, items, key_count):
        """Dispatch item selection to the method matching ``method_type``.

        :param items: list of ``{"index", "cells", "amount"}`` dicts, as
            produced by ``_build_items_from_csv``.
        :param key_count: number of largest-amount items to treat as key
            items.
        :return: a ``(sorted_by_amount, selected_indices, selected_tag)``
            tuple. ``selected_tag`` is ``"Sample"`` for MUS/CVS (items were
            actually selected) or ``"Candidate"`` for NSS (nothing was
            auto-selected; every pool item is listed for the auditor to
            mark by hand).
        """
        self.ensure_one()
        if self.method_type == "mus":
            sorted_by_amount, selected_indices = self._perform_mus_sampling(
                items, key_count, self.sampling_interval
            )
            return sorted_by_amount, selected_indices, "Sample"
        if self.method_type == "cvs":
            sorted_by_amount, selected_indices = self._perform_simple_random_sample(
                items, key_count, self.computed_sample_size
            )
            return sorted_by_amount, selected_indices, "Sample"
        sorted_by_amount, selected_indices = self._perform_nss_candidate_list(
            items, key_count
        )
        return sorted_by_amount, selected_indices, "Candidate"

    def _generate_sampling(self):
        """Build ``sampling_data`` (key items + sample) as a CSV string.

        Reads the source raw data, extracts the configured columns, then
        delegates item selection to ``_select_sampling_items`` according
        to ``method_type``: MUS (size-weighted systematic selection), CVS
        (unweighted random draw), or NSS (every pool item listed as a
        ``Candidate`` for the auditor to mark by hand; nothing is
        auto-selected). Key items are always written first, tagged
        ``Key Item``.

        :return: ``None``. Sets ``sampling_data`` to ``False`` when the
            source, column configuration, or method parameters are
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
        if not self._is_sampling_ready():
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
            (
                sorted_by_amount,
                selected_indices,
                selected_tag,
            ) = self._select_sampling_items(items, key_count)
            is_nss = self.method_type == "nss"
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(output_header)
            for item in sorted_by_amount[:key_count]:
                row = [str(item["index"])] + item["cells"] + ["Key Item"]
                if is_nss:
                    row = row + ["TRUE"]
                writer.writerow(row)
            for item in items:
                if item["index"] in selected_indices:
                    row = [str(item["index"])] + item["cells"] + [selected_tag]
                    if is_nss:
                        row = row + ["TRUE" if selected_tag == "Sample" else "FALSE"]
                    writer.writerow(row)
            self.sampling_data = output.getvalue()
        except Exception:
            self.sampling_data = False

    @api.depends("sampling_data", "method_type", "sampling_process_filter")
    def _compute_sampling_process_data(self):
        """Derive the editable NSS "Sampling Process" table from ``sampling_data``.

        :return: sets ``sampling_process_data`` to the ``Candidate``/
            ``Sample`` rows of ``sampling_data`` (``Key Item`` rows
            excluded), optionally narrowed by ``sampling_process_filter``,
            for Non-Statistical Sampling, or ``False`` for other methods
            or when ``sampling_data`` is empty/unparseable.
        """
        for record in self:
            record.sampling_process_data = False
            if record.method_type != "nss" or not record.sampling_data:
                continue
            try:
                rows = list(csv.reader(io.StringIO(record.sampling_data)))
            except Exception:
                continue
            if not rows or "Type" not in rows[0]:
                continue
            type_idx = rows[0].index("Type")
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(rows[0])
            for row in rows[1:]:
                if len(row) > type_idx and row[type_idx] != "Key Item":
                    writer.writerow(row)
            candidate_csv = output.getvalue()
            if record.sampling_process_filter:
                candidate_csv = self._apply_where_clause(
                    candidate_csv, record.sampling_process_filter
                )
            record.sampling_process_data = candidate_csv

    @api.model
    def _apply_where_clause(self, raw_csv, where_clause):
        """Filter CSV data using a read-only SQL WHERE clause via SQLite.

        :param raw_csv: CSV text with a header row.
        :param where_clause: a SQL WHERE clause (without the ``WHERE``
            keyword) referencing the header's sanitised column names.
        :return: the filtered CSV text, or the original ``raw_csv``
            unchanged when it is empty, ``where_clause`` is blank/contains
            a forbidden keyword, or filtering fails for any reason.
        """
        where_clause = (where_clause or "").strip()
        if not where_clause or not raw_csv:
            return raw_csv
        if _FORBIDDEN_SQL.search(where_clause):
            return raw_csv

        reader = csv.reader(io.StringIO(raw_csv))
        headers = next(reader, None)
        rows = list(reader)
        if not headers or not rows:
            return raw_csv

        safe_cols = []
        for h in headers:
            col = re.sub(r"[^\w]", "_", h.strip())
            if not col or col[0].isdigit():
                col = "c_" + col
            safe_cols.append(col)
        col_defs = ", ".join('"{}" TEXT'.format(c) for c in safe_cols)
        placeholders = ", ".join(["?"] * len(safe_cols))

        try:
            conn = sqlite3.connect(":memory:")
            cur = conn.cursor()
            cur.execute("CREATE TABLE data ({})".format(col_defs))
            for row in rows:
                padded = list(row) + [""] * (len(safe_cols) - len(row))
                cur.execute(
                    "INSERT INTO data VALUES ({})".format(placeholders),
                    padded[: len(safe_cols)],
                )
            cur.execute("SELECT * FROM data WHERE {}".format(where_clause))
            filtered = cur.fetchall()
            conn.close()
        except Exception:
            return raw_csv

        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(headers)
        writer.writerows(filtered)
        return out.getvalue()

    def _inverse_sampling_process_data(self):
        """Write edited "Chose?"/Type values back into ``sampling_data``.

        Re-derives each edited row's ``Type`` from its ``Chose?`` checkbox
        (``TRUE`` -> ``Sample``, ``FALSE`` -> ``Candidate``), enforces that
        the resulting Sample count does not exceed
        ``computed_sample_size`` (already net of key items), then merges
        the result back into ``sampling_data``; ``Key Item`` rows are left
        untouched.

        :raise UserError: when the number of rows chosen (``Chose? =
            TRUE``) exceeds ``computed_sample_size``.
        :return: ``None``.
        """
        for record in self:
            if (
                record.method_type != "nss"
                or not record.sampling_process_data
                or not record.sampling_data
            ):
                continue
            try:
                process_rows = list(
                    csv.reader(io.StringIO(record.sampling_process_data))
                )
                full_rows = list(csv.reader(io.StringIO(record.sampling_data)))
            except Exception:
                continue
            if not process_rows or not full_rows:
                continue
            header = full_rows[0]
            if not {"Type", "Chose?", "Index"} <= set(header):
                continue
            type_idx = header.index("Type")
            chose_idx = header.index("Chose?")
            index_idx = header.index("Index")

            edits = {}
            chosen_count = 0
            for row in process_rows[1:]:
                if len(row) <= max(type_idx, chose_idx, index_idx):
                    continue
                row = list(row)
                chosen = row[chose_idx].strip().upper() == "TRUE"
                row[type_idx] = "Sample" if chosen else "Candidate"
                row[chose_idx] = "TRUE" if chosen else "FALSE"
                edits[row[index_idx]] = row
                if chosen:
                    chosen_count += 1

            if chosen_count > record.computed_sample_size:
                raise UserError(
                    _(
                        "You chose %(chosen)s sample item(s), which exceeds "
                        "the Computed Sample Size of %(limit)s (already "
                        "net of key items). Uncheck some candidates first."
                    )
                    % {
                        "chosen": chosen_count,
                        "limit": record.computed_sample_size,
                    }
                )

            merged_rows = [
                edits.get(row[index_idx], row) if len(row) > index_idx else row
                for row in full_rows[1:]
            ]

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(header)
            writer.writerows(merged_rows)
            record.sampling_data = output.getvalue()
