# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io
import math

from odoo import _, api, fields, models
from odoo.exceptions import UserError

# ---------------------------------------------------------------------------
# AICPA Attribute Sampling Tables
# Source: AICPA Audit Guide - Audit Sampling (2014)
# Rows = EPER (Expected Population Error Rate, %)
# Cols = TDR (Tolerable Deviation Rate, %)  [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]
# None = sample size not applicable (EPER >= TDR or too large)
# ---------------------------------------------------------------------------
_TDR_COLS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]

_AICPA_5PCT = {
    0.00: [149, 99, 74, 59, 49, 42, 36, 32, 29, 19, 14],
    0.25: [236, 157, 117, 93, 78, 66, 58, 51, 46, 30, 22],
    0.50: [None, 157, 117, 93, 78, 66, 58, 51, 46, 30, 22],
    0.75: [None, 208, 117, 93, 78, 66, 58, 51, 46, 30, 22],
    1.00: [None, None, 156, 93, 78, 66, 58, 51, 46, 30, 22],
    1.25: [None, None, 156, 124, 78, 66, 58, 51, 46, 30, 22],
    1.50: [None, None, 192, 124, 103, 66, 58, 51, 46, 30, 22],
    1.75: [None, None, 227, 153, 103, 88, 77, 51, 46, 30, 22],
    2.00: [None, None, None, 181, 127, 88, 77, 68, 46, 30, 22],
    2.25: [None, None, None, 208, 127, 88, 77, 68, 61, 30, 22],
    2.50: [None, None, None, None, 150, 109, 77, 68, 61, 30, 22],
    2.75: [None, None, None, None, 173, 109, 95, 68, 61, 30, 22],
    3.00: [None, None, None, None, 195, 129, 95, 84, 61, 30, 22],
    3.25: [None, None, None, None, None, 148, 112, 84, 61, 30, 22],
    3.50: [None, None, None, None, None, 167, 112, 84, 76, 40, 22],
    3.75: [None, None, None, None, None, 185, 129, 100, 76, 40, 22],
    4.00: [None, None, None, None, None, None, 146, 100, 89, 40, 22],
    4.50: [None, None, None, None, None, None, None, 108, 103, 40, 26],
    5.00: [None, None, None, None, None, None, None, 115, 116, 40, 30],
    5.50: [None, None, None, None, None, None, None, None, 148, 45, 30],
    6.00: [None, None, None, None, None, None, None, None, 179, 50, 30],
    6.50: [None, None, None, None, None, None, None, None, None, 59, 34],
    7.00: [None, None, None, None, None, None, None, None, None, 68, 37],
    7.50: [None, None, None, None, None, None, None, None, None, None, 40],
    8.00: [None, None, None, None, None, None, None, None, None, None, 25],
}

_AICPA_10PCT = {
    0.00: [114, 76, 57, 45, 38, 32, 28, 25, 22, 15, 11],
    0.25: [194, 129, 96, 77, 64, 55, 48, 42, 38, 25, 18],
    0.50: [194, 129, 96, 77, 64, 55, 48, 42, 38, 25, 18],
    0.75: [265, 129, 96, 77, 64, 55, 48, 42, 38, 25, 18],
    1.00: [None, 176, 96, 77, 64, 55, 48, 42, 38, 25, 18],
    1.25: [None, 221, 132, 77, 64, 55, 48, 42, 38, 25, 18],
    1.50: [None, None, 132, 105, 64, 55, 48, 42, 38, 25, 18],
    1.75: [None, None, 166, 105, 88, 55, 48, 42, 38, 25, 18],
    2.00: [None, None, 198, 132, 88, 75, 48, 42, 38, 25, 18],
    2.25: [None, None, None, 132, 88, 75, 65, 42, 38, 25, 18],
    2.50: [None, None, None, 158, 110, 75, 65, 42, 38, 25, 18],
    2.75: [None, None, None, 209, 132, 94, 65, 58, 38, 25, 18],
    3.00: [None, None, None, None, 132, 94, 65, 58, 52, 25, 18],
    3.25: [None, None, None, None, 153, 113, 82, 58, 52, 25, 18],
    3.50: [None, None, None, None, 194, 113, 82, 58, 52, 25, 18],
    3.75: [None, None, None, None, None, 131, 98, 73, 52, 25, 18],
    4.00: [None, None, None, None, None, 149, 98, 73, 52, 25, 18],
    4.50: [None, None, None, None, None, 218, 130, 73, 65, 25, 18],
    5.00: [None, None, None, None, None, None, 160, 87, 65, 34, 18],
    5.50: [None, None, None, None, None, None, None, 115, 78, 34, 18],
    6.00: [None, None, None, None, None, None, None, 142, 103, 34, 18],
    6.50: [None, None, None, None, None, None, None, 182, 116, 45, 25],
}


def _aicpa_lookup(eper, tdr, table):
    """
    Look up sample size from AICPA attribute sampling table.
    Finds the nearest EPER row (rounding up) and exact TDR column.
    Returns 0 if combination is not feasible (TDR <= EPER or value is None).
    """
    if tdr <= eper or tdr not in _TDR_COLS:
        return 0
    tdr_idx = _TDR_COLS.index(tdr)

    # Exact or nearest EPER row (round up to next available)
    available_epers = sorted(table.keys())
    selected_eper = None
    for e in available_epers:
        if e >= eper:
            selected_eper = e
            break
    if selected_eper is None:
        return 0

    row = table[selected_eper]
    if tdr_idx >= len(row) or row[tdr_idx] is None:
        return 0
    return row[tdr_idx]


def _finite_population_correction(n_initial, population):
    """
    Apply finite population correction to the initial sample size.
    Formula: n' = n / (1 + n/N) where N is the population size.
    Returns the corrected sample size (rounded up).
    """
    if not population or population <= 0 or not n_initial or n_initial <= 0:
        return n_initial
    corrected = n_initial / (1 + n_initial / population)
    return math.ceil(corrected)


def _chi2_ppf_approx(p, df):
    """
    Chi-square inverse CDF approximation using Wilson-Hilferty method.
    For df=2: uses exact formula -2*ln(1-p).
    p  = confidence level (e.g. 0.95 for 5% risk)
    df = degrees of freedom
    Returns the chi-square quantile.
    """
    if df <= 0 or p <= 0 or p >= 1:
        return 0.0
    if df == 2:
        return -2.0 * math.log(1.0 - p)

    # Normal quantile (probit) via Beasley-Springer-Moro approximation
    if p >= 0.5:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        z = q - (2.515517 + 0.802853 * q + 0.010328 * q * q) / (
            1.0 + 1.432788 * q + 0.189269 * q * q + 0.001308 * q * q * q
        )
    else:
        q = math.sqrt(-2.0 * math.log(p))
        z = -(
            q
            - (2.515517 + 0.802853 * q + 0.010328 * q * q)
            / (1.0 + 1.432788 * q + 0.189269 * q * q + 0.001308 * q * q * q)
        )

    # Wilson-Hilferty transformation
    v = float(df)
    term = 1.0 - 2.0 / (9.0 * v) + z * math.sqrt(2.0 / (9.0 * v))
    if term <= 0:
        return 0.0
    return v * (term**3)


# ---------------------------------------------------------------------------
# CUER Lookup Tables (standard AICPA attribute sampling CUER tables)
# Rows = Sample Size (n), Cols index = Deviations Found k (0..10)
# None = not applicable (CUER exceeds meaningful table limit, ~>20%)
# ---------------------------------------------------------------------------
_CUER_5PCT = {
    20: [None, None, None, None, None, None, None, None, None, None, None],
    25: [11.3, 17.6, None, None, None, None, None, None, None, None, None],
    30: [9.5, 14.9, 19.5, None, None, None, None, None, None, None, None],
    35: [8.2, 12.9, 16.9, None, None, None, None, None, None, None, None],
    40: [7.2, 11.3, 14.9, 18.3, None, None, None, None, None, None, None],
    45: [6.4, 10.1, 13.3, 16.3, 19.2, None, None, None, None, None, None],
    50: [5.8, 9.1, 12.1, 14.8, 17.4, 19.9, None, None, None, None, None],
    55: [5.3, 8.3, 11.0, 13.5, 15.9, 18.1, None, None, None, None, None],
    60: [4.9, 7.7, 10.1, 12.4, 14.6, 16.7, 18.8, None, None, None, None],
    65: [4.5, 7.1, 9.4, 11.5, 13.5, 15.5, 17.4, 19.3, None, None, None],
    70: [4.2, 6.6, 8.7, 10.7, 12.6, 14.4, 16.2, 18.0, 19.7, None, None],
    75: [3.9, 6.2, 8.2, 10.0, 11.8, 13.5, 15.2, 16.9, 18.4, 20.0, None],
    80: [3.7, 5.8, 7.7, 9.4, 11.1, 12.7, 14.3, 15.8, 17.3, 18.8, None],
    90: [3.3, 5.2, 6.8, 8.4, 9.9, 11.3, 12.7, 14.1, 15.5, 16.8, 18.1],
    100: [3.0, 4.7, 6.2, 7.6, 8.9, 10.2, 11.5, 12.7, 14.0, 15.2, 16.4],
    125: [2.4, 3.7, 4.9, 6.1, 7.2, 8.2, 9.3, 10.3, 11.3, 12.2, 13.2],
    150: [2.0, 3.1, 4.1, 5.1, 6.0, 6.9, 7.7, 8.6, 9.4, 10.2, 11.0],
    200: [1.5, 2.3, 3.1, 3.8, 4.5, 5.2, 5.8, 6.5, 7.1, 7.7, 8.3],
}

_CUER_10PCT = {
    20: [10.9, 18.1, None, None, None, None, None, None, None, None, None],
    25: [8.8, 14.7, 19.9, None, None, None, None, None, None, None, None],
    30: [7.4, 12.4, 16.8, None, None, None, None, None, None, None, None],
    35: [6.4, 10.7, 14.5, 18.1, None, None, None, None, None, None, None],
    40: [5.6, 9.4, 12.8, 15.9, 19.0, None, None, None, None, None, None],
    45: [5.0, 8.4, 11.4, 14.2, 17.0, 19.6, None, None, None, None, None],
    50: [4.5, 7.6, 10.3, 12.9, 15.4, 17.8, None, None, None, None, None],
    55: [4.1, 6.9, 9.4, 11.7, 14.0, 16.2, 18.4, None, None, None, None],
    60: [3.8, 6.3, 8.6, 10.8, 12.9, 14.9, 16.9, 18.8, None, None, None],
    65: [3.5, 5.9, 8.0, 10.1, 12.0, 13.9, 15.8, 17.5, None, None, None],
    70: [3.2, 5.4, 7.4, 9.3, 11.1, 12.8, 14.6, 16.2, 17.9, 19.5, None],
    75: [3.0, 5.1, 7.0, 8.8, 10.4, 12.1, 13.7, 15.3, 16.8, 18.4, None],
    80: [2.8, 4.8, 6.5, 8.3, 9.7, 11.3, 12.8, 14.3, 15.7, 17.2, 18.6],
    90: [2.5, 4.3, 5.8, 7.3, 8.7, 10.1, 11.4, 12.7, 14.0, 15.3, 16.6],
    100: [2.3, 3.8, 5.2, 6.6, 7.8, 9.1, 10.3, 11.5, 12.7, 13.8, 15.0],
    125: [1.9, 3.2, 4.4, 5.5, 6.6, 7.6, 8.6, 9.6, 10.6, 11.6, 12.5],
    150: [1.4, 2.4, 3.3, 4.1, 4.9, 5.7, 6.5, 7.2, 8.0, 8.7, 9.5],
    200: [1.1, 1.9, 2.6, 3.3, 4.0, 4.6, 5.2, 5.8, 6.4, 7.0, 7.6],
}


def _compute_cuer(deviation_count, sample_actual, aro):
    """
    Compute the Computed Upper Exception Rate (CUER) using the standard
    AICPA attribute sampling CUER table. For sample sizes between table rows,
    linear interpolation is used. For n > 200 or k > 10, or for None table
    cells, falls back to the chi-square approximation.

    deviation_count : number of deviations found in sample (k)
    sample_actual   : actual sample size tested (n)
    aro             : Acceptable Risk of Overreliance (% integer: 5 or 10)
    Returns CUER as percentage (float), or 0.0 if not determinable.
    """
    if sample_actual <= 0:
        return 0.0
    k = deviation_count
    n = sample_actual

    def _chi2_fallback():
        confidence = 1.0 - aro / 100.0
        df = 2 * (k + 1)
        chi2_val = _chi2_ppf_approx(confidence, df)
        return round(chi2_val / (2.0 * n) * 100.0, 2)

    table = _CUER_5PCT if aro == 5 else _CUER_10PCT

    # k outside table column range → chi-square fallback
    if k < 0 or k > 10:
        return _chi2_fallback()

    sorted_ns = sorted(table.keys())
    min_n = sorted_ns[0]
    max_n = sorted_ns[-1]

    # n outside table row range → chi-square fallback
    if n < min_n or n > max_n:
        return _chi2_fallback()

    # Exact match
    if n in table:
        val = table[n][k]
        return round(val, 2) if val is not None else _chi2_fallback()

    # Linear interpolation between bracketing rows
    n_low = max(ns for ns in sorted_ns if ns < n)
    n_high = min(ns for ns in sorted_ns if ns > n)
    val_low = table[n_low][k]
    val_high = table[n_high][k]

    if val_low is None and val_high is None:
        return _chi2_fallback()
    if val_low is None:
        return round(val_high, 2)
    if val_high is None:
        return round(val_low, 2)

    ratio = (n - n_low) / (n_high - n_low)
    return round(val_low + ratio * (val_high - val_low), 2)


class GeneralAuditWSe3f4a5bAttribute(models.Model):
    """
    Attribute Sampling — Test of Control (e3f4a5b).

    Represents a single control attribute tested within a Test of Control
    worksheet (``general_audit_ws_e3f4a5b``). Each record manages four
    stages: planning, population correction, execution, and conclusion.

    **Sampling Plan**
    From the EPER, TDR, and ARO parameters, the system computes the initial
    sample sizes (``sample_5pct`` / ``sample_10pct``) using the AICPA table.
    ``sample_initial`` is selected based on the active ARO level; FPC
    (Finite Population Correction) is then applied to derive ``sample_final``.

    **Sampling Execution**
    ``action_generate_sample`` copies the master sample from ``ws.sample_data``
    into this attribute's ``sample_data``, resetting Deviation→FALSE and
    Note→"" so the auditor can record fieldwork results.

    After the auditor fills in the Deviation column, the **Compute Deviation**
    button (``action_compute_deviation``) calls ``_compute_sample_actual_deviation``
    which re-reads ``sample_data`` to calculate:
    - ``sample_actual``: number of non-empty data rows.
    - ``deviation_count``: rows where Deviation is TRUE / 1 / YES / X.

    **CUER and Conclusion**
    - ``deviation_rate_sample`` / ``deviation_rate_population``: computed as
      ``deviation_count / sample_actual × 100%`` (``@api.depends``).
    - ``cuer_5pct`` / ``cuer_10pct``: CUER from the AICPA table with linear
      interpolation between rows; falls back to chi-square approximation for
      sample sizes outside the table range or k > 10.
    - ``cuer``: effective CUER based on the selected ARO level.
    - ``conclusion``: Effective if CUER ≤ TDR, Not Effective if CUER > TDR.

    Reference standards: ISA 530 / SA 530 — Audit Sampling;
    ISA 330 / SA 330 — Auditor Responses to Assessed Risks.
    """

    _name = "general_audit_ws_e3f4a5b.attribute"
    _description = "Test of Control (e3f4a5b) - Attribute Sampling"
    _order = "worksheet_id, sequence"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_e3f4a5b",
        string="Worksheet",
        required=True,
        ondelete="cascade",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="worksheet_id.currency_id",
        store=True,
    )
    sequence = fields.Integer(
        string="No.",
        default=10,
        help="Sequence number for ordering attributes.",
    )
    name = fields.Char(
        string="Attribute",
        required=True,
        help="Name of the control attribute being tested (e.g. Otorisasi, Verifikasi).",
    )
    description = fields.Text(
        string="Description",
        help="Detail description of what is checked for this attribute.",
    )
    eper = fields.Float(
        string="EPER (%)",
        digits=(5, 2),
        default=0.0,
        help=(
            "Expected Population Error Rate — auditor's estimated"
            " deviation rate in the population (%)."
        ),
    )
    tdr = fields.Integer(
        string="TDR (%)",
        default=5,
        help="Tolerable Deviation Rate — maximum deviation rate the auditor can accept (%). "
        "Standard values: 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20.",
    )
    aro = fields.Selection(
        string="ARO (%)",
        selection=[("5", "5%"), ("10", "10%")],
        default="5",
        required=True,
        help="Acceptable Risk of Overreliance — risk that the auditor will rely on the "
        "control even though its actual deviation rate exceeds TDR.",
    )
    sample_5pct = fields.Integer(
        string="Sample (5% Risk)",
        compute="_compute_sample_sizes",
        store=True,
        compute_sudo=True,
        help="Required sample size at 5% Acceptable Risk of Overreliance (from AICPA table).",
    )
    sample_10pct = fields.Integer(
        string="Sample (10% Risk)",
        compute="_compute_sample_sizes",
        store=True,
        compute_sudo=True,
        help="Required sample size at 10% Acceptable Risk of Overreliance (from AICPA table).",
    )
    sample_initial = fields.Integer(
        string="Initial Sample",
        compute="_compute_sample_initial",
        store=True,
        compute_sudo=True,
        help="Initial sample size before finite population correction, "
        "selected based on ARO setting.",
    )
    population_count = fields.Integer(
        string="Population",
        related="worksheet_id.population_count",
        store=False,
        compute_sudo=True,
        help="Total population size (number of items) from the worksheet.",
    )
    sample_final = fields.Integer(
        string="Final Sample",
        compute="_compute_sample_final",
        store=True,
        compute_sudo=True,
        help="Final sample size after finite population correction.",
    )
    sample_data = fields.Text(
        string="Sample Data",
        help="CSV data of sampled items. "
        "Generated by 'Generate Sample' button. "
        "User fills Deviation (TRUE/FALSE) and Note columns.",
    )
    sample_actual = fields.Integer(
        string="Actual Sample",
        compute="_compute_sample_actual_deviation",
        store=True,
        compute_sudo=True,
        help="Actual number of items tested (counted from sample data rows).",
    )
    deviation_count = fields.Integer(
        string="Deviations Found",
        compute="_compute_sample_actual_deviation",
        store=True,
        compute_sudo=True,
        help="Number of deviations found (rows where Deviation=TRUE).",
    )
    deviation_rate_sample = fields.Float(
        string="Sample Deviation Rate (%)",
        digits=(5, 2),
        compute="_compute_deviation_rates",
        store=True,
        compute_sudo=True,
        help="Deviation rate found in the sample (deviation_count / sample_actual × 100%).",
    )
    deviation_rate_population = fields.Float(
        string="Projected Population Deviation Rate (%)",
        digits=(5, 2),
        compute="_compute_deviation_rates",
        store=True,
        compute_sudo=True,
        help="Projected deviation rate in the population based on the sample.",
    )
    cuer_5pct = fields.Float(
        string="CUER (5% Risk) (%)",
        digits=(5, 2),
        compute="_compute_cuer_fields",
        store=True,
        compute_sudo=True,
        help="Computed Upper Exception Rate at 5% Acceptable Risk of Overreliance.",
    )
    cuer_10pct = fields.Float(
        string="CUER (10% Risk) (%)",
        digits=(5, 2),
        compute="_compute_cuer_fields",
        store=True,
        compute_sudo=True,
        help="Computed Upper Exception Rate at 10% Acceptable Risk of Overreliance.",
    )
    cuer = fields.Float(
        string="CUER (%)",
        digits=(5, 2),
        compute="_compute_cuer_effective",
        store=True,
        compute_sudo=True,
        help="Effective CUER based on the selected ARO level.",
    )
    conclusion = fields.Selection(
        string="Conclusion",
        selection=[
            ("effective", "Effective"),
            ("not_effective", "Not Effective"),
        ],
        compute="_compute_conclusion",
        store=True,
        compute_sudo=True,
        help="Conclusion: Effective if CUER ≤ TDR, Not Effective if CUER > TDR.",
    )

    @api.depends("eper", "tdr")
    def _compute_sample_sizes(self):
        for record in self:
            tdr = record.tdr
            eper = record.eper
            record.sample_5pct = _aicpa_lookup(eper, tdr, _AICPA_5PCT)
            record.sample_10pct = _aicpa_lookup(eper, tdr, _AICPA_10PCT)

    @api.depends("aro", "sample_5pct", "sample_10pct")
    def _compute_sample_initial(self):
        for record in self:
            if record.aro == "5":
                record.sample_initial = record.sample_5pct
            else:
                record.sample_initial = record.sample_10pct

    @api.depends("sample_initial", "population_count")
    def _compute_sample_final(self):
        for record in self:
            record.sample_final = _finite_population_correction(
                record.sample_initial, record.population_count
            )

    def _compute_sample_actual_deviation(self):
        for record in self:
            sample_actual = 0
            deviation_count = 0
            if record.sample_data:
                try:
                    reader = csv.reader(io.StringIO(record.sample_data))
                    header = next(reader, None)
                    if header:
                        header_lower = [h.strip().lower() for h in header]
                        dev_idx = None
                        if "deviation" in header_lower:
                            dev_idx = header_lower.index("deviation")
                        for row in reader:
                            if row and any(cell.strip() for cell in row):
                                sample_actual += 1
                                if dev_idx is not None and dev_idx < len(row):
                                    val = row[dev_idx].strip().upper()
                                    if val in ("TRUE", "1", "YES", "X"):
                                        deviation_count += 1
                except Exception:
                    pass
            record.sample_actual = sample_actual
            record.deviation_count = deviation_count

    def action_compute_deviation(self):
        self._compute_sample_actual_deviation()

    def action_generate_sample(self):
        self.ensure_one()
        ws = self.worksheet_id
        if not ws.sample_data:
            raise UserError(
                _(
                    "No sample data available on worksheet. "
                    "Please generate worksheet sample first."
                )
            )

        reader = csv.reader(io.StringIO(ws.sample_data))
        header = next(reader, None)
        if not header:
            raise UserError(_("Worksheet sample data has no header row."))

        header_lower = [h.strip().lower() for h in header]
        note_idx = header_lower.index("note") if "note" in header_lower else None

        # Insert "Deviation" column before "Note" (or append if no Note column)
        if note_idx is not None:
            out_header = header[:note_idx] + ["Deviation"] + header[note_idx:]
            dev_col = note_idx
            note_col = note_idx + 1
        else:
            out_header = header + ["Deviation"]
            dev_col = len(header)
            note_col = None

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(out_header)

        for row in reader:
            if not row or not any(cell.strip() for cell in row):
                continue
            new_row = list(row)
            new_row = new_row[:dev_col] + ["FALSE"] + new_row[dev_col:]
            if note_col is not None and note_col < len(new_row):
                new_row[note_col] = ""
            writer.writerow(new_row)

        self.sample_data = output.getvalue()

    @api.depends("deviation_count", "sample_actual")
    def _compute_deviation_rates(self):
        for record in self:
            n = record.sample_actual
            d = record.deviation_count
            if n > 0:
                record.deviation_rate_sample = round(d / n * 100.0, 2)
                record.deviation_rate_population = round(d / n * 100.0, 2)
            else:
                record.deviation_rate_sample = 0.0
                record.deviation_rate_population = 0.0

    @api.depends("deviation_count", "sample_actual")
    def _compute_cuer_fields(self):
        for record in self:
            k = record.deviation_count
            n = record.sample_actual
            record.cuer_5pct = _compute_cuer(k, n, 5)
            record.cuer_10pct = _compute_cuer(k, n, 10)

    @api.depends("aro", "cuer_5pct", "cuer_10pct")
    def _compute_cuer_effective(self):
        for record in self:
            if record.aro == "5":
                record.cuer = record.cuer_5pct
            else:
                record.cuer = record.cuer_10pct

    @api.depends("cuer", "tdr")
    def _compute_conclusion(self):
        for record in self:
            if record.sample_actual > 0 and record.tdr > 0:
                if record.cuer <= record.tdr:
                    record.conclusion = "effective"
                else:
                    record.conclusion = "not_effective"
            else:
                record.conclusion = False
