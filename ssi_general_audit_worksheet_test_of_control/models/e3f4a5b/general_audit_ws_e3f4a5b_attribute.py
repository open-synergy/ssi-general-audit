# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io
import math
import random

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


def _compute_cuer(deviation_count, sample_actual, aro):
    """
    Compute the Computed Upper Exception Rate (CUER) using the chi-square formula.
    CUER = chi2(2*(k+1), 1-ARO/100) / (2*n) * 100 (as %)

    deviation_count : number of deviations found in sample (k)
    sample_actual   : actual sample size tested (n)
    aro             : Acceptable Risk of Overreliance (% integer: 5 or 10)
    Returns CUER as percentage (float).
    """
    if sample_actual <= 0:
        return 0.0
    k = deviation_count
    n = sample_actual
    confidence = 1.0 - aro / 100.0
    df = 2 * (k + 1)
    chi2_val = _chi2_ppf_approx(confidence, df)
    return round(chi2_val / (2.0 * n) * 100.0, 2)


class GeneralAuditWSe3f4a5bAttribute(models.Model):
    """
    Attribute Sampling — Test of Control (e3f4a5b).

    Merepresentasikan satu atribut pengendalian yang diuji dalam
    worksheet Test of Control. Setiap record mencakup:

    - **Rencana sampling**: EPER, TDR, ARO, dan ukuran sampel yang
      dihitung otomatis dari tabel AICPA (5% dan 10% risk).
    - **Koreksi populasi terbatas**: ukuran sampel final dihitung
      menggunakan finite population correction (FPC).
    - **Pelaksanaan sampling**: data sampel acak yang di-generate
      dari raw data populasi worksheet induk.
    - **Kesimpulan**: perbandingan CUER terhadap TDR untuk menentukan
      apakah pengendalian efektif atau tidak efektif.

    Referensi standar: ISA 530 / SA 530 — Audit Sampling.
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

    @api.depends("sample_data")
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

    def action_generate_sample(self):
        self.ensure_one()
        ws = self.worksheet_id
        if not ws.raw_data:
            raise UserError(
                _("No raw data available. Please select a data source first.")
            )
        if self.sample_final <= 0:
            raise UserError(
                _("Sample size is zero. " "Please configure EPER, TDR, and ARO first.")
            )

        reader = csv.reader(io.StringIO(ws.raw_data))
        header = next(reader, None)
        if not header:
            raise UserError(_("Raw data has no header row."))

        data_rows = []
        for idx, row in enumerate(reader, start=1):
            if row and any(cell.strip() for cell in row):
                data_rows.append((idx, row))

        if not data_rows:
            raise UserError(_("Raw data has no data rows."))

        n = min(self.sample_final, len(data_rows))
        selected = sorted(random.sample(data_rows, n), key=lambda x: x[0])

        ref_col_header = "Document Ref"
        if ws.ref_col_number and ws.ref_col_number <= len(header):
            ref_col_header = header[ws.ref_col_number - 1].strip() or ref_col_header

        amount_col_header = "Amount"
        if ws.amount_col_number and ws.amount_col_number <= len(header):
            amount_col_header = (
                header[ws.amount_col_number - 1].strip() or amount_col_header
            )

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            ["Seq", "Item No", ref_col_header, amount_col_header, "Deviation", "Note"]
        )

        for seq, (item_no, row) in enumerate(selected, start=1):
            ref = ""
            if ws.ref_col_number and ws.ref_col_number <= len(row):
                ref = row[ws.ref_col_number - 1].strip()

            amount = ""
            if ws.amount_col_number and ws.amount_col_number <= len(row):
                amount = row[ws.amount_col_number - 1].strip()

            writer.writerow([seq, item_no, ref, amount, "FALSE", ""])

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
