# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io
import math

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class GeneralAuditWsB4f8e1a(models.Model):
    """
    Test of Detail worksheet: records the substantive test result for
    each item examined, either a sample (via a linked Sample
    Determination worksheet) or 100% of a General Ledger/Subledger
    population selected directly (``data_source``).

    Implements the Difference Estimation evaluation method (per
    ``ToD_akun_260821.ods``, HT/26/000689) when ``data_source`` is
    Sample: the auditor links a Sample Determination worksheet,
    generates one examination row per sampled item
    (``examination_data``), fills in the Audited Amount found for
    each, and the population misstatement projection, precision
    interval, confidence limits, and conclusion are derived
    automatically. When ``data_source`` is Population, the confidence
    interval/limit projection is not meaningful (100% of the
    population is already examined) and is skipped -- the conclusion
    is instead based directly on whether any difference was found.

    ``risk_factor``, ``aria``, and ``aria_coefficient`` are **not**
    re-entered here -- they stay ``related`` mirrors of the linked
    Sample Determination worksheet's own fields (read-only, and only
    meaningful for the Sample data source). ``performance_materiality``
    and ``population_count`` are ``compute=`` fields that branch on
    ``data_source``: mirroring the linked Sample Determination
    worksheet for Sample, or derived directly from the selected
    General Ledger/Subledger for Population.
    """

    _name = "general_audit_ws_b4f8e1a"
    _description = "Test of Detail (b4f8e1a)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_test_of_detail" ".worksheet_type_b4f8e1a"
    )

    data_mode = fields.Selection(
        string="Data Mode",
        selection=[("gl", "General Ledger"), ("subledger", "Subledger")],
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Determines whether to use General Ledger or Subledger "
        "data as population for this Test of Detail.",
    )
    allowed_general_ledger_ids = fields.Many2many(
        comodel_name="general_audit_ws_d209914",
        string="Allowed General Ledgers",
        compute="_compute_allowed_general_ledger_ids",
        store=False,
        compute_sudo=True,
        help="General Ledger worksheets belonging to the same general "
        "audit engagement as this worksheet.",
    )
    general_ledger_id = fields.Many2one(
        comodel_name="general_audit_ws_d209914",
        string="General Ledger",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The general ledger data used as population for this Test " "of Detail.",
    )
    allowed_subledger_ids = fields.Many2many(
        comodel_name="general_audit_ws_b5e3d9f",
        string="Allowed Subledgers",
        compute="_compute_allowed_subledger_ids",
        store=False,
        compute_sudo=True,
        help="Subledger worksheets belonging to the same general audit "
        "engagement as this worksheet.",
    )
    subledger_id = fields.Many2one(
        comodel_name="general_audit_ws_b5e3d9f",
        string="Subledger",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The subledger data used as population for this Test of " "Detail.",
    )
    data_source = fields.Selection(
        string="Data Source",
        selection=[("population", "Population"), ("sample", "Sample")],
        required=True,
        default="population",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Population examines 100% of the selected General Ledger/"
        "Subledger directly. Sample uses the sampling result of a "
        "linked Sample Determination worksheet (existing behaviour, "
        "unchanged).",
    )
    subledger_amount_id = fields.Many2one(
        comodel_name="general_audit_ws_b5e3d9f.amount",
        string="Subledger Amount Column",
        domain="[('worksheet_id', '=', subledger_id)]",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Which Subledger amount column ("
        "general_audit_ws_b5e3d9f.amount line) to use as Recorded "
        "Amount when Data Mode is Subledger and Data Source is "
        "Population. Required in that combination -- Subledger, "
        "unlike General Ledger, has no fixed debit/credit column "
        "pair, only a user-defined list of labelled amount columns "
        "(amount_ids); the auditor picks which one represents the "
        "recorded transaction amount to examine.",
    )
    allowed_sample_determination_ids = fields.Many2many(
        comodel_name="general_audit_ws_a916660",
        string="Allowed Sample Determination",
        compute="_compute_allowed_sample_determination_ids",
        store=False,
        compute_sudo=True,
        help="Sample Determination worksheets sharing this record's "
        "selected General Ledger or Subledger.",
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
        compute="_compute_population_count",
        store=True,
        compute_sudo=True,
        help="Total population size. When Data Source is Sample, "
        "inherited from the referenced Sample Determination "
        "worksheet. When Data Source is Population, the number of "
        "data rows (excluding header) in the selected General "
        "Ledger/Subledger's Raw Data.",
    )
    sample_type = fields.Selection(
        string="Sampling Method",
        related="sample_determination_id.method_type",
        store=True,
        compute_sudo=True,
        help="Sampling method used to select the items, inherited from "
        "the referenced Sample Determination worksheet.",
    )
    performance_materiality = fields.Monetary(
        string="Performance Materiality",
        currency_field="currency_id",
        compute="_compute_performance_materiality",
        readonly=True,
        store=True,
        compute_sudo=True,
        help="Performance materiality for this account. When Data "
        "Source is Sample, inherited from the referenced Sample "
        "Determination worksheet (edit it there). When Data Source "
        "is Population: the Materiality mapping override for the "
        "selected General Ledger/Subledger's account type on this "
        "engagement, if one is set; otherwise the engagement's Final "
        "Materiality worksheet figure (the same threshold used by "
        "every account by default). See Materiality Mapping Source / "
        "Final Materiality Source below for which one supplied it.",
    )
    materiality_mapping_id = fields.Many2one(
        comodel_name="general_audit_ws_6dcda0e_materiality_mapping",
        string="Materiality Mapping Source",
        compute="_compute_performance_materiality",
        store=True,
        compute_sudo=True,
        help="The Specific Materiality mapping line that supplied "
        "Performance Materiality above via its "
        "use_specific_materiality override. Set only when Data "
        "Source is Population and such an override is active for "
        "the selected account -- open it to verify the figure.",
    )
    final_materiality_id = fields.Many2one(
        comodel_name="general_audit_ws_bb33b94",
        string="Final Materiality Source",
        compute="_compute_performance_materiality",
        store=True,
        compute_sudo=True,
        help="The engagement's Final Materiality worksheet used for "
        "Tolerable Misstatement above, and for Performance "
        "Materiality above when no mapping override is active. Set "
        "whenever Data Source is Population and the engagement has "
        "a Final Materiality worksheet -- open it to verify the "
        "figures.",
    )
    risk_factor = fields.Float(
        string="Risk Factor",
        digits=(3, 2),
        related="sample_determination_id.risk_factor",
        readonly=True,
        store=True,
        compute_sudo=True,
        help="Combined audit risk factor, inherited from the "
        "referenced Sample Determination worksheet -- edit it there, "
        "not here, so both worksheets stay consistent.",
    )
    tolerable_misstatement = fields.Monetary(
        string="Tolerable Misstatement",
        currency_field="currency_id",
        compute="_compute_performance_materiality",
        readonly=True,
        store=True,
        compute_sudo=True,
        help="Maximum monetary misstatement acceptable for this "
        "account. When Data Source is Sample, inherited from the "
        "referenced Sample Determination worksheet (edit it there). "
        "When Data Source is Population: Performance Materiality "
        "above times the engagement's Final Materiality worksheet "
        "Tolerable Misstatement Percentage -- the same policy "
        "percentage applied engagement-wide, scaled to whichever "
        "Performance Materiality actually applies to this account.",
    )
    aria = fields.Selection(
        string="ARIA (%)",
        related="sample_determination_id.aria",
        readonly=True,
        store=True,
        compute_sudo=True,
        help="Acceptable Risk of Incorrect Acceptance, inherited from "
        "the referenced Sample Determination worksheet -- only set "
        "there for Classical Variable / Non-Statistical Sampling, so "
        "it stays blank when the linked worksheet used Monetary Unit "
        "Sampling.",
    )
    aria_coefficient = fields.Float(
        string="ARIA Coefficient",
        related="sample_determination_id.aria_coefficient",
        readonly=True,
        store=True,
        compute_sudo=True,
        digits=(12, 4),
        help="Confidence coefficient looked up from the reliability "
        "table for the chosen ARIA, inherited from the referenced "
        "Sample Determination worksheet.",
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
        string="Difference Estimation Conclusion",
        selection=[
            ("no_misstatement", "No Misstatement"),
            ("misstatement", "Misstatement Detected"),
        ],
        compute="_compute_conclusion_text",
        store=True,
        compute_sudo=True,
        help="'Misstatement Detected' when the upper confidence limit "
        "exceeds Tolerable Misstatement, or the lower confidence limit "
        "is below its negative -- 'No Misstatement' otherwise.",
    )

    @api.depends("general_audit_id")
    def _compute_allowed_general_ledger_ids(self):
        """Restrict the General Ledger picker to this audit engagement.

        :return: nothing; assigns ``allowed_general_ledger_ids``
        """
        GL = self.env["general_audit_ws_d209914"]  # pylint: disable=invalid-name
        for record in self:
            result = []
            if record.general_audit_id:
                result = GL.search(
                    [("general_audit_id", "=", record.general_audit_id.id)]
                ).ids
            record.allowed_general_ledger_ids = result

    @api.depends("general_audit_id")
    def _compute_allowed_subledger_ids(self):
        """Restrict the Subledger picker to this audit engagement.

        :return: nothing; assigns ``allowed_subledger_ids``
        """
        SL = self.env["general_audit_ws_b5e3d9f"]  # pylint: disable=invalid-name
        for record in self:
            result = []
            if record.general_audit_id:
                result = SL.search(
                    [("general_audit_id", "=", record.general_audit_id.id)]
                ).ids
            record.allowed_subledger_ids = result

    @api.depends("data_mode", "general_ledger_id", "subledger_id")
    def _compute_allowed_sample_determination_ids(self):
        """Restrict the Sample Determination picker to the matching source.

        :return: nothing; assigns ``allowed_sample_determination_ids``
            to the ``general_audit_ws_a916660`` records sharing this
            record's selected General Ledger or Subledger, or an
            empty recordset when no source is selected.
        """
        SD = self.env["general_audit_ws_a916660"]  # pylint: disable=invalid-name
        for record in self:
            record.allowed_sample_determination_ids = False
            if record.data_mode == "gl" and record.general_ledger_id:
                record.allowed_sample_determination_ids = SD.search(
                    [("general_ledger_id", "=", record.general_ledger_id.id)]
                )
            elif record.data_mode == "subledger" and record.subledger_id:
                record.allowed_sample_determination_ids = SD.search(
                    [("subledger_id", "=", record.subledger_id.id)]
                )

    @api.depends(
        "data_source",
        "sample_determination_id.performance_materiality",
        "sample_determination_id.tolerable_misstatement",
        "data_mode",
        "general_ledger_id.account_type_id",
        "general_ledger_id.account_id.type_id",
        "subledger_id.account_type_id",
        "subledger_id.account_id.type_id",
        "general_audit_id",
    )
    def _compute_performance_materiality(self):
        """Derive Performance Materiality and Tolerable Misstatement.

        For Population, ``specific_materiality`` on the matching
        ``general_audit_ws_6dcda0e_materiality_mapping`` line is an
        auditor override that only applies when
        ``use_specific_materiality`` is set on that line -- it is
        ``0.0`` by design for the common case where no override was
        made. When no override applies (no matching line, or the line
        has ``use_specific_materiality`` unset), Performance
        Materiality falls back to the engagement-wide figure computed
        by the Final Materiality worksheet
        (``general_audit_ws_bb33b94.performance_materiality``), which
        is the same threshold used by every account unless overridden.
        ``materiality_mapping_id``/``final_materiality_id`` record
        which of these actually supplied Performance Materiality, so
        the auditor can trace it back.

        Tolerable Misstatement for Population is Performance
        Materiality (whichever value above) times the engagement's
        Final Materiality worksheet Tolerable Misstatement Percentage
        -- mirroring ``ToD_akun_260821.ods``'s own Difference
        Estimation formulas (cells D223/D224), which need a real
        Tolerable Misstatement to compare against, not the ``0.0``
        that would otherwise apply here. This is why
        ``final_materiality_id`` is populated whenever a Final
        Materiality worksheet is found, even when Performance
        Materiality itself came from the mapping override -- Tolerable
        Misstatement still depends on it.

        :return: nothing; assigns ``performance_materiality``,
            ``tolerable_misstatement``, ``materiality_mapping_id``, and
            ``final_materiality_id``. For Sample, both amounts mirror
            the linked Sample Determination worksheet and both source
            fields are cleared (that path has its own reference,
            ``sample_determination_id``). For Population,
            ``materiality_mapping_id`` is set when a matching mapping
            line has ``use_specific_materiality`` set (Performance
            Materiality source); ``final_materiality_id`` is set
            whenever the engagement has a Final Materiality worksheet
            (Tolerable Misstatement source, and Performance
            Materiality source when no mapping override applies).
            Amounts are ``0.0`` and both source fields cleared when
            neither is found.
        """
        Mapping = self.env[  # pylint: disable=invalid-name
            "general_audit_ws_6dcda0e_materiality_mapping"
        ]
        FinalMateriality = self.env[  # pylint: disable=invalid-name
            "general_audit_ws_bb33b94"
        ]
        for record in self:
            performance_materiality = 0.0
            tolerable_misstatement = 0.0
            mapping_source = Mapping.browse()
            final_materiality_source = FinalMateriality.browse()
            if record.data_source == "sample":
                performance_materiality = (
                    record.sample_determination_id.performance_materiality
                )
                tolerable_misstatement = (
                    record.sample_determination_id.tolerable_misstatement
                )
            elif record.data_source == "population":
                type_id = False
                if record.data_mode == "gl":
                    type_id = (
                        record.general_ledger_id.account_type_id
                        or record.general_ledger_id.account_id.type_id
                    )
                elif record.data_mode == "subledger":
                    type_id = (
                        record.subledger_id.account_type_id
                        or record.subledger_id.account_id.type_id
                    )
                mapping = Mapping.browse()
                if type_id and record.general_audit_id:
                    mapping = Mapping.search(
                        [
                            ("type_id", "=", type_id.id),
                            (
                                "worksheet_id.general_audit_id",
                                "=",
                                record.general_audit_id.id,
                            ),
                        ],
                        order="sequence, id",
                        limit=1,
                    )
                final_materiality = FinalMateriality.browse()
                if record.general_audit_id:
                    final_materiality = FinalMateriality.search(
                        [
                            (
                                "worksheet_id.general_audit_id",
                                "=",
                                record.general_audit_id.id,
                            ),
                        ],
                        limit=1,
                    )
                if mapping and mapping.use_specific_materiality:
                    performance_materiality = mapping.specific_materiality
                    mapping_source = mapping
                elif final_materiality:
                    performance_materiality = final_materiality.performance_materiality
                if final_materiality:
                    final_materiality_source = final_materiality
                    tolerable_misstatement = performance_materiality * (
                        final_materiality.tolerable_misstatement_percentage / 100.0
                    )
            record.performance_materiality = performance_materiality
            record.tolerable_misstatement = tolerable_misstatement
            record.materiality_mapping_id = mapping_source
            record.final_materiality_id = final_materiality_source

    @api.depends(
        "data_source",
        "sample_determination_id.population_count",
        "data_mode",
        "general_ledger_id.raw_data",
        "subledger_id.raw_data",
    )
    def _compute_population_count(self):
        """Derive Population Count from the selected Data Source.

        :return: nothing; assigns ``population_count`` -- mirrors the
            linked Sample Determination worksheet when Data Source is
            Sample, or counts the data rows (excluding header) of the
            selected General Ledger/Subledger's Raw Data when Data
            Source is Population, or ``0`` otherwise.
        """
        for record in self:
            result = 0
            if record.data_source == "sample":
                result = record.sample_determination_id.population_count
            elif record.data_source == "population":
                raw_data = False
                if record.data_mode == "gl":
                    raw_data = record.general_ledger_id.raw_data
                elif record.data_mode == "subledger":
                    raw_data = record.subledger_id.raw_data
                if raw_data:
                    try:
                        reader = csv.reader(io.StringIO(raw_data))
                        count = sum(1 for _row in reader) - 1
                        result = max(0, count)
                    except Exception:  # pylint: disable=broad-except
                        result = 0
            record.population_count = result

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

        Same formula for both Data Source values -- when Data Source
        is Population, ``population_count`` equals ``sample_count``
        (100% examined), which already forces
        ``population_standard_deviation`` to ``0.0``
        (``_compute_population_standard_deviation``'s own guard,
        replicating ``ToD_akun_260821.ods`` cell ``D223``'s
        ``IF(population=sample,0,...)``), so this collapses to ``0.0``
        without needing a separate branch here.

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

        Same formula for both Data Source values: ``"misstatement"``
        when the upper confidence limit exceeds
        ``tolerable_misstatement`` or the lower confidence limit is
        below its negative, else ``"no_misstatement"``. When Data
        Source is Population, both confidence limits collapse to the
        total difference found (see
        ``_compute_computed_precision_interval``), so this reduces to
        comparing that total against ``tolerable_misstatement`` --
        exactly ``ToD_akun_260821.ods``'s own degenerate case for a
        100%-examined population, not a bespoke Population rule.

        :return: nothing; assigns ``conclusion_text`` to
            ``"misstatement"`` when the upper confidence limit
            exceeds Tolerable Misstatement, or the lower confidence
            limit is below its negative -- ``"no_misstatement"``
            otherwise.
        """
        for record in self:
            result = "no_misstatement"
            if (
                record.upper_confidence_limit > record.tolerable_misstatement
                or record.lower_confidence_limit < -record.tolerable_misstatement
            ):
                result = "misstatement"
            record.conclusion_text = result

    @api.onchange("data_mode")
    def onchange_general_ledger_id(self):
        """Clear the selected General Ledger when Data Mode changes."""
        self.general_ledger_id = False

    @api.onchange("data_mode")
    def onchange_subledger_id(self):
        """Clear the selected Subledger when Data Mode changes."""
        self.subledger_id = False

    @api.onchange("data_mode", "general_ledger_id", "subledger_id")
    def onchange_sample_determination_id(self):
        """Clear the stale Sample Determination when the source changes."""
        self.sample_determination_id = False

    @api.onchange("subledger_id")
    def onchange_subledger_amount_id(self):
        """Clear the Subledger Amount column when Subledger changes."""
        self.subledger_amount_id = False

    @api.onchange(
        "sample_determination_id",
        "data_source",
        "general_ledger_id",
        "subledger_id",
        "subledger_amount_id",
    )
    def onchange_examination_data(self):
        """Clear the stale examination table when the data source changes."""
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
        """(Re)build ``examination_data`` from the selected Data Source.

        Dispatches to the Sample or Population builder according to
        ``data_source`` -- see ``_generate_examination_data_sample``
        and ``_generate_examination_data_population``.

        :raise UserError: when the source data required by the
            selected Data Source/Data Mode combination is missing --
            see the dispatched method for the exact condition.
        :return: ``None``.
        """
        for record in self:
            if record.data_source == "sample":
                record._generate_examination_data_sample()
            else:
                record._generate_examination_data_population()

    def _generate_examination_data_sample(self):
        """Seed ``examination_data`` from the linked Sample Determination.

        Seeds one row per item in ``sampling_data`` (its Key Item and
        Sample rows), carrying over ``Item`` (the Sample Determination
        row's Index) and ``Sample`` (its identifier column, always the
        second ``sampling_data`` column -- see
        ``general_audit_ws_b4f7d9c._parse_ref_values`` for the same
        convention) and ``Recorded Amount`` (via
        ``_get_recorded_amount_cell_index``). ``Audited Amount`` starts
        blank for the auditor to fill in. Unchanged from the
        pre-Data-Source behaviour of this worksheet.

        :raise UserError: when ``sampling_data`` is empty, or the
            linked Sample Determination has no monetary column
            configured.
        :return: ``None``.
        """
        self.ensure_one()
        if not self.sampling_data:
            raise UserError(
                _(
                    "No sampling data available. Please select a "
                    "Sample Determination worksheet with a generated "
                    "sample first."
                )
            )
        cell_index = self._get_recorded_amount_cell_index()
        if cell_index is None:
            raise UserError(
                _(
                    "The linked Sample Determination worksheet has no "
                    "monetary column configured."
                )
            )
        rows = list(csv.reader(io.StringIO(self.sampling_data)))
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Seq", "Item", "Data", "Recorded Amount", "Audited Amount"])
        amount_pos = 1 + cell_index
        for seq, row in enumerate(rows[1:], start=1):
            item = row[0] if len(row) >= 1 else ""
            sample = row[1] if len(row) >= 2 else ""
            recorded = row[amount_pos] if len(row) > amount_pos else ""
            writer.writerow([seq, item, sample, recorded, ""])
        self.examination_data = output.getvalue()

    def _generate_examination_data_population(self):
        """Seed ``examination_data`` from the selected GL/Subledger.

        Builds one row per data row (excluding header) of the
        selected General Ledger/Subledger's ``raw_data``: ``Item`` is
        the row's sequence number (Seq), ``Data`` is the value of the
        selected General Ledger/Subledger's own
        ``identifier_col_number`` (blank when not configured there),
        and ``Recorded Amount`` is Debit minus Credit (General Ledger, not
        adjusted for the account's normal balance) or the raw value of
        the selected ``subledger_amount_id`` column (Subledger, no
        netting). ``Audited Amount`` starts blank for the auditor to
        fill in.

        :raise UserError: when ``data_mode`` is not set, when the
            General Ledger/Subledger required by ``data_mode`` is not
            selected, or (Subledger only) when
            ``subledger_amount_id`` is not selected.
        :return: ``None``.
        """
        self.ensure_one()
        amount_col = None
        if self.data_mode == "gl":
            if not self.general_ledger_id:
                raise UserError(_("Please select a General Ledger first."))
            source = self.general_ledger_id
            debit_col = source.debit_col_number
            credit_col = source.credit_col_number
        elif self.data_mode == "subledger":
            if not self.subledger_id:
                raise UserError(_("Please select a Subledger first."))
            if not self.subledger_amount_id:
                raise UserError(_("Please select a Subledger Amount column first."))
            source = self.subledger_id
            amount_col = self.subledger_amount_id.col_number
        else:
            raise UserError(_("Please select a General Ledger or Subledger first."))

        thousand_sep = source.thousand_separator or ","
        decimal_sep = source.decimal_separator or "."
        identifier_col = source.identifier_col_number
        rows = list(csv.reader(io.StringIO(source.raw_data or "")))
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Seq", "Item", "Data", "Recorded Amount", "Audited Amount"])
        for seq, row in enumerate(rows[1:], start=1):
            sample = ""
            if identifier_col and len(row) >= identifier_col:
                sample = row[identifier_col - 1].strip()
            if self.data_mode == "gl":
                recorded = self._parse_raw_amount(
                    row, debit_col, thousand_sep, decimal_sep
                ) - self._parse_raw_amount(row, credit_col, thousand_sep, decimal_sep)
            else:
                recorded = self._parse_raw_amount(
                    row, amount_col, thousand_sep, decimal_sep
                )
            writer.writerow([seq, seq, sample, recorded, ""])
        self.examination_data = output.getvalue()

    @staticmethod
    def _parse_raw_amount(row, col_number, thousand_sep, decimal_sep):
        """Parse one Raw Data CSV cell as a float.

        :param row: the CSV data row (list of cell strings).
        :param col_number: 1-based column number to read, or a falsy
            value to skip parsing.
        :param thousand_sep: thousand separator character to strip.
        :param decimal_sep: decimal separator character normalised
            to ``.``.
        :return: the parsed ``float`` value, or ``0.0`` when
            ``col_number`` is falsy, the row is too short, the cell
            is blank, or parsing fails.
        """
        if not col_number or len(row) < col_number:
            return 0.0
        value_str = row[col_number - 1].strip()
        if not value_str:
            return 0.0
        try:
            value_str = value_str.replace(thousand_sep, "").replace(decimal_sep, ".")
            return float(value_str)
        except ValueError:
            return 0.0
