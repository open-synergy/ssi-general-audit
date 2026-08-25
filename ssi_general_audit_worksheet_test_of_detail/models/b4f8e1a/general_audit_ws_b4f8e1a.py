# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io
import math

from odoo import _, api, fields, models
from odoo.exceptions import UserError

# Confidence coefficient per ARIA, identical to the "Table" sheet
# (columns A/B/D, keyed by ARIA%) in both ``ToD_akun_260821.ods`` and the
# Sample Determination worksheet's own source spreadsheets -- duplicated
# here (rather than imported from ``general_audit_ws_a916660``) so this
# module does not reach into another module's model implementation.
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
ARIA_SELECTION = [(k, "{}%".format(k)) for k in ARIA_COEFFICIENT_TABLE]


class GeneralAuditWsB4f8e1a(models.Model):
    """
    Test of Detail worksheet: records the substantive test result for each
    item selected by the corresponding Sample Determination worksheet.

    Implements the Difference Estimation evaluation method (per
    ``ToD_akun_260821.ods``, HT/26/000689): the auditor links a Sample
    Determination worksheet, generates one examination row per sampled
    item (``examination_data``), fills in the Audited Amount found for
    each, and the population misstatement projection, precision
    interval, confidence limits, and conclusion are derived
    automatically.
    """

    _name = "general_audit_ws_b4f8e1a"
    _description = "Test of Detail (b4f8e1a)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_test_of_detail" ".worksheet_type_b4f8e1a"
    )

    allowed_sample_determination_ids = fields.Many2many(
        comodel_name="general_audit_ws_a916660",
        string="Allowed Sample Determination",
        compute="_compute_allowed_sample_determination_ids",
        store=False,
        compute_sudo=True,
        help="Sample Determination worksheets belonging to the same "
        "general audit engagement as this worksheet.",
    )
    sample_determination_id = fields.Many2one(
        comodel_name="general_audit_ws_a916660",
        string="# Sample Determination",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Reference to the Sample Determination worksheet whose "
        "sampling result is examined by this Test of Detail.",
    )
    sampling_data = fields.Text(
        string="Sampling Data",
        related="sample_determination_id.sampling_data",
        store=True,
        compute_sudo=True,
        help="Sampling data inherited from the referenced Sample "
        "Determination worksheet -- the source of the Item/Sample/"
        "Recorded Amount columns in 'Generate Examination Data'.",
    )
    population_count = fields.Integer(
        string="Population Count",
        related="sample_determination_id.population_count",
        store=True,
        compute_sudo=True,
        help="Total population size, inherited from the referenced "
        "Sample Determination worksheet.",
    )
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
    tolerable_misstatement = fields.Monetary(
        string="Tolerable Misstatement",
        currency_field="currency_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Maximum monetary misstatement acceptable for this "
        "account. Auto-fills as Performance Materiality x Risk Factor "
        "when either changes, but can still be typed over directly.",
    )
    aria = fields.Selection(
        string="ARIA (%)",
        selection=ARIA_SELECTION,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Acceptable Risk of Incorrect Acceptance, used to look up "
        "the confidence coefficient for the precision interval.",
    )
    aria_coefficient = fields.Float(
        string="ARIA Coefficient",
        compute="_compute_aria_coefficient",
        store=True,
        compute_sudo=True,
        digits=(12, 4),
        help="Confidence coefficient looked up from the reliability "
        "table for the chosen ARIA.",
    )
    examination_data = fields.Text(
        string="Examination Data",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="CSV table (Seq, Item, Sample, Recorded Amount, Audited "
        "Amount), one row per item examined. Seeded by 'Generate "
        "Examination Data' from the linked Sample Determination "
        "worksheet's sampling result; fill in Audited Amount for each "
        "row as the substantive test is performed. A blank or "
        "non-numeric Audited Amount is treated as a difference of 0 "
        "(not yet examined), matching ``IFERROR(Recorded-Audited,0)`` "
        "in the reference spreadsheet.",
    )
    sample_count = fields.Integer(
        string="Sample Count",
        compute="_compute_examination_totals",
        store=True,
        compute_sudo=True,
        help="Number of item rows in ``examination_data``.",
    )
    sum_difference = fields.Monetary(
        string="Sum of Difference",
        currency_field="currency_id",
        compute="_compute_examination_totals",
        store=False,
        compute_sudo=True,
        help="Total of (Recorded Amount - Audited Amount) across every "
        "row in ``examination_data``.",
    )
    sum_difference_squared = fields.Float(
        string="Sum of Difference Squared",
        compute="_compute_examination_totals",
        store=False,
        compute_sudo=True,
        help="Total of (Recorded Amount - Audited Amount)^2 across "
        "every row in ``examination_data``.",
    )
    average_difference = fields.Monetary(
        string="Average Difference per Item",
        currency_field="currency_id",
        compute="_compute_average_difference",
        store=True,
        compute_sudo=True,
        help="``sum_difference / sample_count``.",
    )
    population_difference_projection = fields.Monetary(
        string="Population Difference Projection",
        currency_field="currency_id",
        compute="_compute_population_difference_projection",
        store=True,
        compute_sudo=True,
        help="``average_difference`` extrapolated to the whole "
        "population: ``average_difference x population_count``.",
    )
    population_standard_deviation = fields.Float(
        string="Population Standard Deviation",
        compute="_compute_population_standard_deviation",
        store=True,
        compute_sudo=True,
        digits=(16, 4),
        help="Standard deviation of the sample differences, replicating "
        "``ToD_akun_260821.ods`` cell ``D223`` literally (including its "
        "``/ sample_count - 1`` grouping, not the textbook ``/ "
        "(sample_count - 1)`` Bessel correction).",
    )
    computed_precision_interval = fields.Monetary(
        string="Computed Precision Interval",
        currency_field="currency_id",
        compute="_compute_computed_precision_interval",
        store=True,
        compute_sudo=True,
        help="``population_count x aria_coefficient x "
        "(population_standard_deviation / SQRT(sample_count))``.",
    )
    upper_confidence_limit = fields.Monetary(
        string="Computed Upper Confidence Limit",
        currency_field="currency_id",
        compute="_compute_upper_confidence_limit",
        store=True,
        compute_sudo=True,
        help="``population_difference_projection + " "computed_precision_interval``.",
    )
    lower_confidence_limit = fields.Monetary(
        string="Computed Lower Confidence Limit",
        currency_field="currency_id",
        compute="_compute_lower_confidence_limit",
        store=True,
        compute_sudo=True,
        help="``population_difference_projection - " "computed_precision_interval``.",
    )
    conclusion_text = fields.Selection(
        string="Conclusion",
        selection=[
            ("no_misstatement", "TIDAK TERJADI SALAH SAJI"),
            ("misstatement", "TERJADI SALAH SAJI"),
        ],
        compute="_compute_conclusion_text",
        store=True,
        compute_sudo=True,
        help="'TERJADI SALAH SAJI' when the upper confidence limit "
        "exceeds Tolerable Misstatement, or the lower confidence limit "
        "is below its negative -- 'TIDAK TERJADI SALAH SAJI' otherwise.",
    )

    @api.depends("general_audit_id")
    def _compute_allowed_sample_determination_ids(self):
        """Restrict the Sample Determination picker to this engagement.

        :return: nothing; assigns ``allowed_sample_determination_ids``
        """
        SD = self.env["general_audit_ws_a916660"]  # pylint: disable=invalid-name
        for record in self:
            result = []
            if record.general_audit_id:
                result = SD.search(
                    [("general_audit_id", "=", record.general_audit_id.id)]
                ).ids
            record.allowed_sample_determination_ids = result

    @api.depends("aria")
    def _compute_aria_coefficient(self):
        """Look up the confidence coefficient for the chosen ARIA.

        :return: nothing; assigns ``aria_coefficient`` from
            ``ARIA_COEFFICIENT_TABLE``, or ``0.0`` when ``aria`` is
            unset.
        """
        for record in self:
            record.aria_coefficient = ARIA_COEFFICIENT_TABLE.get(record.aria, 0.0)

    @api.depends("examination_data")
    def _compute_examination_totals(self):
        """Total the sample count and Difference/Difference-squared sums.

        Mirrors ``IFERROR(Recorded-Audited,0)`` in the reference
        spreadsheet (``ToD_akun_260821.ods``, cells ``F19:F218`` /
        ``G19:G218``): a row whose Audited Amount is blank or
        non-numeric contributes a difference of ``0.0`` -- it is not
        excluded from ``sample_count``, only from contributing a
        nonzero difference.

        :return: nothing; assigns ``sample_count``, ``sum_difference``,
            and ``sum_difference_squared``.
        """
        for record in self:
            count = 0
            sum_diff = 0.0
            sum_diff_sq = 0.0
            if record.examination_data:
                rows = list(csv.reader(io.StringIO(record.examination_data)))
                for row in rows[1:]:
                    count += 1
                    diff = 0.0
                    if len(row) >= 5:
                        try:
                            recorded = float(row[3].strip() or 0.0)
                            audited_raw = row[4].strip()
                            if audited_raw:
                                diff = recorded - float(audited_raw)
                        except ValueError:
                            diff = 0.0
                    sum_diff += diff
                    sum_diff_sq += diff * diff
            record.sample_count = count
            record.sum_difference = sum_diff
            record.sum_difference_squared = sum_diff_sq

    @api.depends("sum_difference", "sample_count")
    def _compute_average_difference(self):
        """Derive the average Recorded-Audited difference per item.

        :return: nothing; assigns ``average_difference``, or ``0.0``
            when ``sample_count`` is 0.
        """
        for record in self:
            result = 0.0
            if record.sample_count > 0:
                result = record.sum_difference / record.sample_count
            record.average_difference = result

    @api.depends("average_difference", "population_count")
    def _compute_population_difference_projection(self):
        """Extrapolate the average difference to the whole population.

        :return: nothing; assigns ``population_difference_projection``
        """
        for record in self:
            record.population_difference_projection = (
                record.average_difference * record.population_count
            )

    @api.depends(
        "population_count",
        "sample_count",
        "sum_difference_squared",
        "average_difference",
    )
    def _compute_population_standard_deviation(self):
        """Derive the sample standard deviation of the differences.

        Literal replication of ``ToD_akun_260821.ods`` cell ``D223``:
        ``IFERROR(IF(population=sample,0,SQRT((sum_diff_sq -
        sample*average^2)/sample - 1)),0)`` -- the division is by
        ``sample_count`` alone, with ``- 1`` applied *outside* that
        division (not the textbook Bessel-corrected ``/ (sample_count -
        1)``). Kept as-is, per the same faithful-replication precedent
        as ``general_audit_ws_a916660._perform_mus_sampling``.

        :return: nothing; assigns ``population_standard_deviation``, or
            ``0.0`` when ``sample_count`` is 0, the population equals
            the sample, or the formula's inner value is negative.
        """
        for record in self:
            result = 0.0
            if record.sample_count > 0 and record.population_count != (
                record.sample_count
            ):
                inner = (
                    record.sum_difference_squared
                    - record.sample_count * (record.average_difference**2)
                ) / record.sample_count - 1
                try:
                    result = math.sqrt(inner)
                except ValueError:
                    result = 0.0
            record.population_standard_deviation = result

    @api.depends(
        "population_count",
        "aria_coefficient",
        "population_standard_deviation",
        "sample_count",
    )
    def _compute_computed_precision_interval(self):
        """Derive the Computed Precision Interval (CPI).

        :return: nothing; assigns ``computed_precision_interval``, or
            ``0.0`` when ``sample_count`` is 0.
        """
        for record in self:
            result = 0.0
            if record.sample_count > 0:
                result = (
                    record.population_count
                    * record.aria_coefficient
                    * (
                        record.population_standard_deviation
                        / math.sqrt(record.sample_count)
                    )
                )
            record.computed_precision_interval = result

    @api.depends("population_difference_projection", "computed_precision_interval")
    def _compute_upper_confidence_limit(self):
        """Derive the Computed Upper Confidence Limit.

        :return: nothing; assigns ``upper_confidence_limit``
        """
        for record in self:
            record.upper_confidence_limit = (
                record.population_difference_projection
                + record.computed_precision_interval
            )

    @api.depends("population_difference_projection", "computed_precision_interval")
    def _compute_lower_confidence_limit(self):
        """Derive the Computed Lower Confidence Limit.

        :return: nothing; assigns ``lower_confidence_limit``
        """
        for record in self:
            record.lower_confidence_limit = (
                record.population_difference_projection
                - record.computed_precision_interval
            )

    @api.depends(
        "upper_confidence_limit", "lower_confidence_limit", "tolerable_misstatement"
    )
    def _compute_conclusion_text(self):
        """Derive the Difference Estimation conclusion.

        :return: nothing; assigns ``conclusion_text`` to
            ``"misstatement"`` when the upper confidence limit exceeds
            ``tolerable_misstatement`` or the lower confidence limit is
            below its negative, else ``"no_misstatement"``.
        """
        for record in self:
            result = "no_misstatement"
            if (
                record.upper_confidence_limit > record.tolerable_misstatement
                or record.lower_confidence_limit < -record.tolerable_misstatement
            ):
                result = "misstatement"
            record.conclusion_text = result

    @api.onchange("performance_materiality", "risk_factor")
    def onchange_tolerable_misstatement(self):
        """Prefill Tolerable Misstatement as Performance Materiality x Risk Factor."""
        self.tolerable_misstatement = self.performance_materiality * self.risk_factor

    @api.onchange("sample_determination_id")
    def onchange_examination_data(self):
        """Clear the stale examination table when the linked SD changes."""
        self.examination_data = False

    def _get_recorded_amount_cell_index(self):
        """Locate the Recorded Amount cell within a ``sampling_data`` row.

        Mirrors ``general_audit_ws_a916660._build_unique_columns``: that
        method de-duplicates ``[identifier_col_number,
        monetary_col_number, additional_info_col_number]`` (in that
        order, skipping unset columns) into the CSV column order
        actually emitted after ``Index``. The monetary value's position
        in that de-duplicated list is therefore its 0-based position
        among a data row's non-Index cells.

        :return: the 0-based index into a ``sampling_data`` data row's
            cells (excluding the leading ``Index`` cell) holding the
            Recorded Amount, or ``None`` when the linked Sample
            Determination has no monetary column configured.
        """
        self.ensure_one()
        sd = self.sample_determination_id
        monetary_col = sd.monetary_col_number
        if not monetary_col:
            return None
        columns = [
            c
            for c in [
                sd.identifier_col_number,
                sd.monetary_col_number,
                sd.additional_info_col_number,
            ]
            if c and c > 0
        ]
        unique_columns = []
        for c in columns:
            if c not in unique_columns:
                unique_columns.append(c)
        return unique_columns.index(monetary_col)

    def action_generate_examination_data(self):
        """(Re)build ``examination_data`` from the linked Sample Determination.

        Seeds one row per item in ``sampling_data`` (its Key Item and
        Sample rows), carrying over ``Item`` (the Sample Determination
        row's Index) and ``Sample`` (its identifier column, always the
        second ``sampling_data`` column -- see
        ``general_audit_ws_b4f7d9c._parse_ref_values`` for the same
        convention) and ``Recorded Amount`` (via
        ``_get_recorded_amount_cell_index``). ``Audited Amount`` starts
        blank for the auditor to fill in.

        :raise UserError: when ``sampling_data`` is empty, or the
            linked Sample Determination has no monetary column
            configured.
        :return: ``None``.
        """
        for record in self:
            if not record.sampling_data:
                raise UserError(
                    _(
                        "No sampling data available. Please select a "
                        "Sample Determination worksheet with a generated "
                        "sample first."
                    )
                )
            cell_index = record._get_recorded_amount_cell_index()
            if cell_index is None:
                raise UserError(
                    _(
                        "The linked Sample Determination worksheet has no "
                        "monetary column configured."
                    )
                )
            rows = list(csv.reader(io.StringIO(record.sampling_data)))
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(
                ["Seq", "Item", "Sample", "Recorded Amount", "Audited Amount"]
            )
            amount_pos = 1 + cell_index
            for seq, row in enumerate(rows[1:], start=1):
                item = row[0] if len(row) >= 1 else ""
                sample = row[1] if len(row) >= 2 else ""
                recorded = row[amount_pos] if len(row) > amount_pos else ""
                writer.writerow([seq, item, sample, recorded, ""])
            record.examination_data = output.getvalue()
