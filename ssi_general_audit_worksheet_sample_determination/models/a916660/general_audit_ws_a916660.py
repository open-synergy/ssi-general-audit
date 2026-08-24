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


def _round_half_up(value):
    """Round a non-negative float like Excel's ``ROUND(value, 0)``.

    Python's builtin ``round()`` uses round-half-to-even, which disagrees
    with Excel's round-half-away-from-zero for ``.5`` boundaries. Sample
    amounts are always non-negative here, so half-away-from-zero reduces
    to half-up.

    :param value: a non-negative float.
    :return: ``value`` rounded to the nearest integer, ``.5`` rounding up.
    """
    return math.floor(value + 0.5)


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
        help="The final result of the sample determination: only key "
        "items (100%% examination) and the chosen sample items -- "
        "``Candidate`` rows never appear here. For Non-Statistical "
        "Sampling, choose which candidates become 'Sample' in the "
        "'Sampling Process' tab (``nss_candidate_pool``); this field is "
        "rebuilt from that choice every time it is saved. Always "
        "read-only here -- for NSS, edit via 'Sampling Process' instead.",
    )
    nss_candidate_pool = fields.Text(
        string="NSS Candidate Pool",
        readonly=True,
        help="Non-Statistical Sampling only: every pool item (all items "
        "minus key items), each tagged 'Candidate' or 'Sample' with a "
        "'Chose?' flag -- the full working set 'Sampling Process' choices "
        "are made against and merged back into. Not shown directly in any "
        "tab; kept separate from ``sampling_data`` so that field can stay "
        "'key items + chosen samples only'.",
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
        help="Non-Statistical Sampling only: ``nss_candidate_pool``, "
        "optionally narrowed by ``sampling_process_filter``, each row "
        "with a 'Chose?' checkbox. Check it to promote a candidate to "
        "'Sample'; uncheck to send a 'Sample' back to 'Candidate'. Key "
        "items are not shown here -- they are always chosen "
        "automatically and are not affected by this tab.",
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
    tolerable_misstatement = fields.Monetary(
        string="Tolerable Misstatement",
        currency_field="currency_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Maximum monetary misstatement acceptable for this account.",
    )
    confidence_factor = fields.Float(
        string="Confidence Factor",
        digits=(12, 4),
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Confidence factor for Monetary Unit Sampling, a manual "
        "input based on professional judgment (e.g. 1.5). Used to derive "
        "``Sampling Interval``.",
    )
    multiplier_random = fields.Monetary(
        string="Multiplier Random",
        currency_field="currency_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Manual input: upper bound for the ``Random`` draw (``Random "
        "= RAND() x Multiplier Random``) used to pick the MUS "
        "systematic-sampling start point. Not necessarily related to "
        "``Sampling Interval`` -- see ``Random``'s help.",
    )
    random_start = fields.Monetary(
        string="Random",
        currency_field="currency_id",
        readonly=True,
        help="The random start point actually used the last time "
        "'Generate Sampling' ran for Monetary Unit Sampling: a value "
        "drawn uniformly from ``[0, Multiplier Random)``. Not clamped to "
        "``Sampling Interval`` -- it is often larger, which is expected "
        "(matches ``SD_akun_MUS_terbaru.ods`` cell ``Data!U2``); see "
        "``_perform_mus_sampling`` for how the walk still keeps "
        "'Realized to sampling' capped at 'Total Plan Examination'.",
    )
    sampling_interval = fields.Monetary(
        string="Sampling Interval",
        currency_field="currency_id",
        compute="_compute_sampling_interval",
        store=True,
        compute_sudo=True,
        help="Sampling interval = Tolerable Misstatement / (Risk Factor / "
        "30%) / Confidence Factor.",
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
    total_plan_examination = fields.Integer(
        string="Total Plan Examination",
        compute="_compute_total_plan_examination",
        store=True,
        compute_sudo=True,
        help="Total Plan Examination = Total Plan Sample Examination "
        "(``Computed Sample Size``) + Key Item Count -- the full "
        "examination plan, sample and 100%% key items combined.",
    )

    # --- Data to sampling (Monetary Unit Sampling only) ---
    beginning_to_sampling = fields.Integer(
        string="Beginning to Sampling",
        compute="_compute_beginning_to_sampling",
        store=True,
        compute_sudo=True,
        help="1-based row position where sampling begins in the "
        "descending-amount-sorted population: ``Key Item Count`` + 1 "
        "(the row right after the last key item).",
    )
    realized_to_sampling = fields.Integer(
        string="Realized to Sampling",
        readonly=True,
        help="Number of items actually marked as a hit (key items and "
        "MUS samples combined) the last time 'Generate Sampling' ran. "
        "Set by ``_perform_mus_sampling``; expected to equal "
        "``Total Plan Examination`` -- see ``Sampling Variance``.",
    )
    sampling_variance = fields.Integer(
        string="Sampling Variance",
        compute="_compute_sampling_variance",
        compute_sudo=True,
        help="``Total Plan Examination`` minus ``Realized to Sampling``. "
        "Expected to be 0; a nonzero value means the population did not "
        "have enough qualifying items to reach the planned examination "
        "count the last time 'Generate Sampling' ran.",
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

    @api.depends("tolerable_misstatement", "risk_factor", "confidence_factor")
    def _compute_sampling_interval(self):
        """Derive the MUS sampling interval.

        Formula (verified against ``SD_akun_MUS_terbaru.ods`` cell
        ``Data!S6``): ``Tolerable Misstatement / (Risk Factor / 30%) /
        Confidence Factor`` -- the ``30%`` is a fixed constant in the
        source spreadsheet, not a configurable field.

        :return: sets ``sampling_interval`` accordingly, or ``0.0`` when
            ``risk_factor`` or ``confidence_factor`` is not positive.
        """
        for record in self:
            if record.risk_factor > 0 and record.confidence_factor > 0:
                record.sampling_interval = (
                    record.tolerable_misstatement
                    / (record.risk_factor / 0.30)
                    / record.confidence_factor
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
        """Derive the number of sample items to select from the pool
        (excludes key items -- see ``total_plan_examination`` for the
        full plan including them).

        Branches by ``method_type``: MUS rounds the sample pool amount
        divided by the sampling interval to the nearest integer (matching
        ``ROUND(S13/S6,0)`` in ``SD_akun_MUS_terbaru.ods`` cell
        ``Data!S14`` -- round-half-up, not round-down/up like CVS); CVS/NSS
        use the classical variables sampling size formula (see
        ``_compute_cvs_sample_size``), minus ``key_item_count`` -- that
        formula's raw result is the *combined* key+sample total (matching
        ``SD_akun_CVS_260821.ods`` cell ``Data!S14`` "Total Plan
        Examination", verified there against ``Data!S13`` "Sampling
        Examination" = ``S14-S12`` where ``S12`` is the key item count).
        NSS additionally lets ``nss_final_sample_size`` override the
        statistically computed pool size with a professional-judgment
        figure (matching ``SD_akun_NSS_260821.ods`` cell ``Data!S15``
        "Total Plan Examination (M)" -- a manual figure, distinct from
        ``Data!S14``'s "(A)" automatic one); the override is the pool
        size directly, not reduced by ``key_item_count`` again.

        :return: sets ``computed_sample_size``, or ``0`` when the method's
            required inputs are incomplete.
        """
        for record in self:
            result = 0
            if record.method_type == "mus":
                if record.sampling_interval > 0:
                    result = _round_half_up(
                        record.sample_amount / record.sampling_interval
                    )
            elif record.method_type in ("cvs", "nss"):
                result = max(
                    0,
                    record._compute_cvs_sample_size() - (record.key_item_count or 0),
                )
                if record.method_type == "nss" and record.nss_final_sample_size:
                    result = record.nss_final_sample_size
            record.computed_sample_size = result

    @api.depends("computed_sample_size", "key_item_count")
    def _compute_total_plan_examination(self):
        """Derive the full examination plan (sample + key items).

        :return: sets ``total_plan_examination`` to ``computed_sample_size
            + key_item_count`` (matching ``S15 = S14+L12`` in
            ``SD_akun_MUS_terbaru.ods``).
        """
        for record in self:
            record.total_plan_examination = record.computed_sample_size + (
                record.key_item_count or 0
            )

    @api.depends("key_item_count")
    def _compute_beginning_to_sampling(self):
        """Derive the 1-based row where sampling begins.

        :return: sets ``beginning_to_sampling`` to ``key_item_count + 1``
            (matching ``U11 = L12+1`` in ``SD_akun_MUS_terbaru.ods``).
        """
        for record in self:
            record.beginning_to_sampling = (record.key_item_count or 0) + 1

    @api.depends("total_plan_examination", "realized_to_sampling")
    def _compute_sampling_variance(self):
        """Derive the gap between planned and realized examination counts.

        :return: sets ``sampling_variance`` to ``total_plan_examination -
            realized_to_sampling`` (matching ``U15 = S15-U14`` in
            ``SD_akun_MUS_terbaru.ods``).
        """
        for record in self:
            record.sampling_variance = (
                record.total_plan_examination - record.realized_to_sampling
            )

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
            trailing ``"Chose?"`` column for Non-Statistical Sampling, or
            ``"From", "Up To"`` for Monetary Unit Sampling) and ``items``
            is a list of ``{"index", "cells", "amount"}`` dicts, one per
            data row.
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
        elif self.method_type == "mus":
            output_header = output_header + ["From", "Up To"]
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

        Faithfully replicates the row-by-row walk in
        ``SD_akun_MUS_terbaru.ods`` (sheet ``Data``, columns ``Q18:AA2737``)
        rather than a textbook cumulative-interval walk, per HT/26/000687:
        Sets ``self.random_start`` to ``RAND() * Multiplier Random``
        (``Data!U2``), drawn once for this run -- unlike a textbook
        systematic sample, this is **not** clamped to ``[0,
        sample_interval)``: it can (and typically does) exceed the
        interval when ``Multiplier Random`` is set well above it. Also
        sets ``self.realized_to_sampling`` to the total hit count (key
        items and MUS samples combined; matches ``Data!U14 = V16``).

        Identifies key items as the top ``key_count`` by amount
        (``Data!J18:N2737``'s "Direct Examination" rows are amount-sorted
        the same way), then walks key items (amount-descending) followed
        by the sample pool in its *original* order -- ``Data!J18:N2737``
        keeps the "Sample Examination" rows in the underlying
        population's order, not re-sorted by amount. The walk maintains a
        running cumulative position that starts at the random draw and
        either keeps accumulating (``position += amount``) or resets back
        to the random draw, exactly like ``Data!R18:R2737``:

        - a "hit" is declared when ``amount + position - 1 >=
          sample_interval`` (``Data!T18:T2737``);
        - the position for the *next* item is the random draw again if
          this item was a hit, otherwise this item's own ``amount +
          position - 1`` (``Data!R19:R2737``) -- so once a hit occurs,
          the next item is tested against the random draw alone, not
          cumulative amount;
        - a zero-amount item's own From/Up To are blank
          (``Data!R_n = IF(M_n=0,"",...)``) and it can never be a hit;
          the *next* item then inherits that blank as its From, and
          ``amount + blank - 1`` errors in Excel, so ``IFERROR`` resets
          Up To to 0 (``Data!S_n = IFERROR(M_n+R_n-1,0)``) -- this is
          what lets genuine accumulation (a varying From) resume for
          Sample items after a zero-amount row, rather than every item
          latching onto ``random_start`` forever once one hit occurs;
        - a running hit counter is capped at ``total_planned =
          computed_sample_size + key_count`` (``Data!AA18:AA2737``
          against ``$U$13+$U$11-1``): once that many hits have been
          counted, no further item is marked, so "Realized to sampling"
          never exceeds "Total Plan Examination" -- though when
          ``Multiplier Random`` towers over ``sample_interval`` (so most
          items hit immediately), it also means the walk degenerates to
          "the first ``total_planned`` items in descending-amount order",
          which is no longer probability-proportional-to-size the way a
          classic MUS interval walk is. That degenerate behaviour is
          inherited as-is from the source spreadsheet.

        :param items: list of ``{"index", "cells", "amount"}`` dicts, as
            produced by ``_build_items_from_csv``.
        :param key_count: number of largest-amount items to treat as key
            items; still walked (they consume the hit cap exactly like
            the source sheet), but never added to the returned set.
        :param sample_interval: MUS sampling interval; must be positive for
            any sample item to be selected.
        :return: a ``(sorted_by_amount, mus_selected_indices, walk_trace)``
            tuple: all items sorted by amount descending, the set of item
            ``index`` values selected as MUS samples (excluding key
            items), and ``walk_trace`` = ``{index: (from, up_to,
            is_threshold_crossed)}`` for every walked item -- ``from``/
            ``up_to`` are ``None`` (blank) for a zero-amount item.
        """
        self.ensure_one()
        sorted_by_amount = sorted(items, key=lambda x: x["amount"], reverse=True)
        key_items_desc = sorted_by_amount[:key_count]
        key_item_indices = {item["index"] for item in key_items_desc}
        sample_pool_amount = sum(
            item["amount"]
            for item in sorted_by_amount
            if item["index"] not in key_item_indices
        )
        sample_size = (
            _round_half_up(sample_pool_amount / sample_interval)
            if sample_interval > 0 and sample_pool_amount > 0
            else 0
        )
        total_planned = sample_size + key_count

        self.random_start = 0.0
        if sample_interval > 0 and self.multiplier_random > 0:
            self.random_start = random.uniform(0, self.multiplier_random)

        # The walk order is key items (amount-descending, matching
        # ``Data!J18:N2737``'s "Direct Examination" block) followed by the
        # sample pool in its *original* input order, NOT amount-sorted --
        # verified against the source spreadsheet: only its first 20
        # (Direct Examination) rows are amount-sorted, the remaining
        # "Sample Examination" rows keep the underlying population's
        # order. Walking the pool in amount order instead (as an earlier
        # version of this method did) suppresses the zero-amount reset
        # mechanic above and makes "From" latch onto ``random_start`` for
        # far more rows than the source spreadsheet does.
        walk_sequence = key_items_desc + [
            item for item in items if item["index"] not in key_item_indices
        ]

        mus_selected_indices = set()
        walk_trace = {}
        hit_count = 0
        if sample_interval > 0 and total_planned > 0:
            position = self.random_start
            for item in walk_sequence:
                amount = item["amount"]
                if amount == 0:
                    # `Data!R_n = IF(M_n=0,"",...)`: a zero-amount item's own
                    # From/Up To are blank, and its ``crossed`` (T) is
                    # forced False -- it can never itself be a hit.
                    from_val = None
                    up_to_val = None
                    is_threshold_crossed = False
                else:
                    from_val = position
                    if from_val is None:
                        # `Data!S_n = IFERROR(M_n+R_n-1, 0)`: adding a
                        # blank From (inherited from a prior zero-amount
                        # item) errors in Excel, and IFERROR falls back to
                        # 0 -- this is what lets accumulation genuinely
                        # restart for Sample items instead of latching
                        # onto ``random_start`` forever.
                        up_to_val = 0.0
                    else:
                        up_to_val = amount + from_val - 1
                    is_threshold_crossed = sample_interval <= up_to_val
                walk_trace[item["index"]] = (from_val, up_to_val, is_threshold_crossed)
                if is_threshold_crossed and hit_count < total_planned:
                    hit_count += 1
                    if item["index"] not in key_item_indices:
                        mus_selected_indices.add(item["index"])
                position = self.random_start if is_threshold_crossed else up_to_val
        self.realized_to_sampling = hit_count
        return sorted_by_amount, mus_selected_indices, walk_trace

    def _perform_simple_random_sample(self, items, key_count, total_planned):
        """Select a random sample from the pool for Classical Variable Sampling.

        Faithfully replicates ``SD_akun_CVS_260821.ods`` (sheet ``Data``,
        columns ``Q18:V1017``) rather than a plain ``random.sample`` draw,
        per HT/26/000687: walks key items (amount-descending, matching
        ``Data!J18:N1017``'s "Direct Examination" rows) followed by the
        sample pool in its *original* input order (matching "Sample
        Examination" rows -- verified the same way as
        ``_perform_mus_sampling``'s walk order). Key items are always
        accepted (``Data!S_n = IF(Q_n<U$11, K_n, ...)``); each pool item
        independently draws ``RANDBETWEEN(key_count+1, population_count)``
        (``Data!R_n``) and is accepted only if that draw falls strictly
        between ``key_count`` and ``total_planned`` (``Data!S_n``'s other
        branch) -- unlike MUS, nothing here is weighted by amount, so
        acceptance is a per-item coin flip, not a systematic walk. A
        running hit counter capped at ``total_planned`` (``Data!AA18:AA1017``
        against ``$U$13``, matching ``_perform_mus_sampling``'s cap) stops
        accepting once the plan is filled -- but because each row's draw
        is independent, running out of pool rows before enough draws land
        in the acceptance window is possible (unlike MUS's amount-driven
        walk), so "Realized to sampling" can fall short of the plan for a
        small enough pool. That behaviour is inherited as-is from the
        source spreadsheet.

        :param items: list of ``{"index", "cells", "amount"}`` dicts, as
            produced by ``_build_items_from_csv``.
        :param key_count: number of largest-amount items to treat as key
            items; always accepted, consuming the hit cap like the source
            sheet, but never added to the returned set.
        :param total_planned: the combined key+sample target (matches
            ``total_plan_examination``, i.e. ``Data!S14``/``S15`` -- NOT
            the pool-only ``computed_sample_size``).
        :return: a ``(sorted_by_amount, selected_indices)`` tuple, in the
            same shape as ``_perform_mus_sampling``'s return value. Also
            sets ``self.realized_to_sampling`` to the total hit count.
        """
        self.ensure_one()
        sorted_by_amount = sorted(items, key=lambda x: x["amount"], reverse=True)
        key_items_desc = sorted_by_amount[:key_count]
        key_item_indices = {item["index"] for item in key_items_desc}
        walk_sequence = key_items_desc + [
            item for item in items if item["index"] not in key_item_indices
        ]
        population_count = len(items)

        selected_indices = set()
        hit_count = 0
        for position, item in enumerate(walk_sequence, start=1):
            if position <= key_count:
                crossed = True
            elif population_count >= key_count + 1:
                draw = random.randint(key_count + 1, population_count)
                crossed = key_count < draw < total_planned
            else:
                crossed = False
            if crossed and hit_count < total_planned:
                hit_count += 1
                if item["index"] not in key_item_indices:
                    selected_indices.add(item["index"])
        self.realized_to_sampling = hit_count
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
            same shape as ``_perform_mus_sampling``'s return value. Also
            sets ``self.realized_to_sampling`` to ``key_count`` -- nothing
            is chosen yet at generation time; ``_inverse_sampling_process_data``
            updates it again as the auditor checks "Chose?" boxes.
        """
        self.ensure_one()
        sorted_by_amount = sorted(items, key=lambda x: x["amount"], reverse=True)
        key_item_indices = {item["index"] for item in sorted_by_amount[:key_count]}
        candidate_indices = {
            item["index"] for item in items if item["index"] not in key_item_indices
        }
        self.realized_to_sampling = key_count
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
        :return: a ``(sorted_by_amount, selected_indices, selected_tag,
            walk_trace)`` tuple. ``selected_tag`` is ``"Sample"`` for
            MUS/CVS (items were actually selected) or ``"Candidate"`` for
            NSS (nothing was auto-selected; every pool item is listed for
            the auditor to mark by hand). ``walk_trace`` is MUS's
            ``{index: (from, up_to, is_threshold_crossed)}`` (see
            ``_perform_mus_sampling``), or ``{}`` for CVS/NSS.
        """
        self.ensure_one()
        if self.method_type == "mus":
            (
                sorted_by_amount,
                selected_indices,
                walk_trace,
            ) = self._perform_mus_sampling(items, key_count, self.sampling_interval)
            return sorted_by_amount, selected_indices, "Sample", walk_trace
        if self.method_type == "cvs":
            sorted_by_amount, selected_indices = self._perform_simple_random_sample(
                items, key_count, self.total_plan_examination
            )
            return sorted_by_amount, selected_indices, "Sample", {}
        sorted_by_amount, selected_indices = self._perform_nss_candidate_list(
            items, key_count
        )
        return sorted_by_amount, selected_indices, "Candidate", {}

    def _generate_sampling(self):
        """Build ``sampling_data`` (key items + sample) as a CSV string.

        Reads the source raw data, extracts the configured columns, then
        delegates item selection to ``_select_sampling_items`` according
        to ``method_type``: MUS (size-weighted systematic selection), CVS
        (unweighted random draw), or NSS (every pool item listed as a
        ``Candidate`` in ``nss_candidate_pool`` for the auditor to mark by
        hand via the "Sampling Process" tab; nothing is auto-selected, so
        ``sampling_data`` itself gets no Sample rows yet -- only Key Item
        ones). Key items are always written first, tagged ``Key Item``.

        :return: ``None``. Sets ``sampling_data`` (and ``nss_candidate_pool``
            for NSS) to ``False`` when the source, column configuration, or
            method parameters are incomplete, or when parsing fails.
        """
        self.ensure_one()
        raw_data = self._get_source_raw_data()
        monetary_col = self.monetary_col_number
        unique_columns = self._build_unique_columns(
            self.identifier_col_number, monetary_col, self.additional_info_col_number
        )
        if (
            not raw_data
            or not monetary_col
            or not unique_columns
            or not self._is_sampling_ready()
        ):
            self.sampling_data = False
            self.nss_candidate_pool = False
            return
        try:
            all_rows = list(csv.reader(io.StringIO(raw_data)))
            if len(all_rows) < 2:
                self.sampling_data = False
                self.nss_candidate_pool = False
                return
            output_header, items = self._build_items_from_csv(
                all_rows, unique_columns, monetary_col
            )
            key_count = self.key_item_count or 0
            (
                sorted_by_amount,
                selected_indices,
                selected_tag,
                walk_trace,
            ) = self._select_sampling_items(items, key_count)

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(output_header)
            for item in sorted_by_amount[:key_count]:
                row = [str(item["index"])] + item["cells"] + ["Key Item"]
                row += self._sampling_row_suffix(item["index"], "Key Item", walk_trace)
                writer.writerow(row)

            if self.method_type == "nss":
                # Candidates go to the working pool, never to
                # sampling_data -- see the "Sample data isn't clean"
                # HT/26/000687 report: sampling_data must be "key items +
                # chosen samples only".
                pool_output = io.StringIO()
                pool_writer = csv.writer(pool_output)
                pool_writer.writerow(output_header)
                for item in items:
                    if item["index"] in selected_indices:
                        pool_writer.writerow(
                            [str(item["index"])]
                            + item["cells"]
                            + ["Candidate", "FALSE"]
                        )
                self.nss_candidate_pool = pool_output.getvalue()
            else:
                self.nss_candidate_pool = False
                for item in items:
                    if item["index"] in selected_indices:
                        row = [str(item["index"])] + item["cells"] + [selected_tag]
                        row += self._sampling_row_suffix(
                            item["index"], selected_tag, walk_trace
                        )
                        writer.writerow(row)
            self.sampling_data = output.getvalue()
        except Exception:
            self.sampling_data = False
            self.nss_candidate_pool = False

    def _sampling_row_suffix(self, item_index, tag, walk_trace):
        """Build the CSV columns appended after ``Type`` for one row.

        :param item_index: the item's ``index`` (key into ``walk_trace``).
        :param tag: the row's ``Type`` value (``"Key Item"`` or
            ``selected_tag``); only used to derive NSS's ``Chose?``.
        :param walk_trace: MUS's ``{index: (from, up_to,
            is_threshold_crossed)}`` from ``_perform_mus_sampling``, or
            ``{}`` for CVS/NSS.
        :return: ``["Chose?" value]`` for NSS, ``[From, Up To]`` for MUS,
            or ``[]`` for CVS.
        """
        if self.method_type == "nss":
            return ["TRUE" if tag in ("Key Item", "Sample") else "FALSE"]
        if self.method_type == "mus":
            from_val, up_to_val, _crossed = walk_trace.get(
                item_index, (0.0, 0.0, False)
            )
            return [
                "" if from_val is None else str(round(from_val, 2)),
                "" if up_to_val is None else str(round(up_to_val, 2)),
            ]
        return []

    @api.depends("nss_candidate_pool", "method_type", "sampling_process_filter")
    def _compute_sampling_process_data(self):
        """Derive the editable NSS "Sampling Process" table.

        :return: sets ``sampling_process_data`` to ``nss_candidate_pool``
            (already Key-Item-free), optionally narrowed by
            ``sampling_process_filter``, for Non-Statistical Sampling, or
            ``False`` for other methods or when ``nss_candidate_pool`` is
            empty.
        """
        for record in self:
            record.sampling_process_data = False
            if record.method_type != "nss" or not record.nss_candidate_pool:
                continue
            candidate_csv = record.nss_candidate_pool
            if record.sampling_process_filter:
                candidate_csv = self._apply_where_clause(
                    candidate_csv, record.sampling_process_filter
                )
            record.sampling_process_data = candidate_csv

    @api.model
    def _apply_where_clause(self, raw_csv, where_clause):
        """Filter CSV data using a read-only SQL WHERE clause via SQLite.

        Columns whose values are entirely numeric (or blank) get NUMERIC
        affinity so comparisons like ``Amount > 10000000`` are evaluated
        by value, not lexicographically as strings.

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

        # A column declared TEXT gets TEXT affinity, so SQLite compares it
        # lexicographically even against a bare numeric literal in the
        # WHERE clause -- "4440000" > "10000000" is TRUE as strings (the
        # leading "4" beats "1"), even though 4,440,000 < 10,000,000.
        # Give a column that looks entirely numeric NUMERIC affinity
        # instead, so ``Amount > 10000000``-style filters compare by
        # value, not by leading digit.
        def _looks_numeric(value):
            value = (value or "").strip()
            if not value:
                return True
            try:
                float(value)
                return True
            except ValueError:
                return False

        col_types = []
        for i in range(len(safe_cols)):
            values = [row[i] for row in rows if len(row) > i]
            numeric_col = bool(values) and all(_looks_numeric(v) for v in values)
            col_types.append("NUMERIC" if numeric_col else "TEXT")

        col_defs = ", ".join(
            '"{}" {}'.format(c, t) for c, t in zip(safe_cols, col_types)
        )
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
        """Write edited "Chose?"/Type values back into ``nss_candidate_pool``
        and rebuild ``sampling_data`` from the result.

        Re-derives each edited row's ``Type`` from its ``Chose?`` checkbox
        (``TRUE`` -> ``Sample``, ``FALSE`` -> ``Candidate``).

        Edits are merged into ``nss_candidate_pool`` (the full working
        set, which may be larger than what was visible/edited when
        ``sampling_process_filter`` hides some rows -- previously-chosen
        rows outside the current filter keep their state). ``sampling_data``
        is then rebuilt from scratch as the existing ``Key Item`` rows plus
        every ``Sample``-tagged row in the merged pool, so it never carries
        ``Candidate`` rows.

        :raise UserError: when the total number of rows chosen (``Chose?
            = TRUE``) across the whole pool exceeds ``computed_sample_size``.
        :return: ``None``.
        """
        for record in self:
            if (
                record.method_type != "nss"
                or not record.sampling_process_data
                or not record.nss_candidate_pool
                or not record.sampling_data
            ):
                continue
            try:
                process_rows = list(
                    csv.reader(io.StringIO(record.sampling_process_data))
                )
                pool_rows = list(csv.reader(io.StringIO(record.nss_candidate_pool)))
                full_rows = list(csv.reader(io.StringIO(record.sampling_data)))
            except Exception:
                continue
            if not process_rows or not pool_rows or not full_rows:
                continue
            header = pool_rows[0]
            if not {"Type", "Chose?", "Index"} <= set(header):
                continue
            type_idx = header.index("Type")
            chose_idx = header.index("Chose?")
            index_idx = header.index("Index")

            edits = {}
            for row in process_rows[1:]:
                if len(row) <= max(type_idx, chose_idx, index_idx):
                    continue
                row = list(row)
                chosen = row[chose_idx].strip().upper() == "TRUE"
                row[type_idx] = "Sample" if chosen else "Candidate"
                row[chose_idx] = "TRUE" if chosen else "FALSE"
                edits[row[index_idx]] = row

            merged_pool_rows = [
                edits.get(row[index_idx], row) if len(row) > index_idx else row
                for row in pool_rows[1:]
            ]
            sample_rows = [row for row in merged_pool_rows if row[type_idx] == "Sample"]
            chosen_count = len(sample_rows)

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

            pool_output = io.StringIO()
            pool_writer = csv.writer(pool_output)
            pool_writer.writerow(header)
            pool_writer.writerows(merged_pool_rows)
            record.nss_candidate_pool = pool_output.getvalue()

            full_header = full_rows[0]
            full_type_idx = full_header.index("Type")
            key_item_rows = [
                row
                for row in full_rows[1:]
                if len(row) > full_type_idx and row[full_type_idx] == "Key Item"
            ]
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(full_header)
            writer.writerows(key_item_rows)
            writer.writerows(sample_rows)
            record.sampling_data = output.getvalue()
            record.realized_to_sampling = len(key_item_rows) + chosen_count
