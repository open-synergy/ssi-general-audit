# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator

#: Upper-case Roman numeral for each calendar month (1-12), used by
#: ``_build_lai_number`` for its ``roman_month`` segment. A plain lookup
#: table is enough here -- unlike a general-purpose Roman numeral
#: converter, this domain is closed to exactly 12 values.
_ROMAN_NUMERAL_MONTHS = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
    8: "VIII",
    9: "IX",
    10: "X",
    11: "XI",
    12: "XII",
}


class GeneralAuditWSb66777d(models.Model):
    """
    WS.090.2 — Independent Auditor's Report (b66777d)

    Serves as the working-paper record for drafting and reviewing the
    **independent auditor's report** issued to the client's shareholders
    or other intended users.  The report is the primary means by which
    the auditor communicates the results of the engagement.  As required
    by ISA 700 / SA 700, the report must include:

    - A title clearly indicating it is the independent auditor's report.
    - The appropriate opinion (unmodified, qualified, adverse, or
      disclaimer) on the financial statements.
    - Basis for opinion paragraph.
    - Key Audit Matters section (where applicable under ISA 701 / SA 701).
    - Other reporting responsibilities.

    Under ISA 705 / SA 705 the form of the opinion may be modified; under
    ISA 706 / SA 706 emphasis-of-matter or other-matter paragraphs may be
    added.

    **ISA / SA references:** ISA 700 / SA 700 — Forming an Opinion and
    Reporting on Financial Statements; ISA 701 / SA 701 — Key Audit
    Matters; ISA 705 / SA 705 — Modifications to the Opinion;
    ISA 706 / SA 706 — Emphasis-of-Matter and Other-Matter Paragraphs
    """

    _name = "general_audit_ws_b66777d"
    _description = "Independen Auditor Report (b66777d)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_final_report." "worksheet_type_b66777d"

    lai_number = fields.Char(
        string="LAI Number",
        help="Document number of the Laporan Auditor Independen (LAI), "
        "the physical independent auditor's report handed to the "
        "client. Auto-filled (best-effort; see "
        "``_build_lai_number``'s docstring) when the worksheet is "
        "opened, but can still be overwritten manually.",
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_b66777d.detail",
        inverse_name="worksheet_id",
        readonly=True,
        help=(
            "Summary rows (Property/Value), one per active "
            "general_audit_ws_b66777d.property master record, "
            "(re)populated by clicking the Populate button "
            "(action_populate_detail) -- empty on a freshly created "
            "worksheet. See _populate_detail()."
        ),
    )

    # Final Audit Opinion
    #
    # draft_opinion_id (the "Draft Audit Opinion" Many2one shown at the
    # top of the "Final Audit Opinion" page, right before the nine
    # fields below) is NOT defined here. It is added as an extension
    # field by ssi_general_audit_worksheet_review, in
    # models/b66777d/general_audit_ws_b66777d.py of that module -- see
    # the docstring there for why: a static Many2one field on THIS
    # model with comodel_name="general_audit_ws_fc75636" (a model this
    # module never depends on) would work most of the time, but Odoo's
    # field setup caches its comodel resolution the first time it
    # runs. When this module and ssi_general_audit_worksheet_review
    # are updated together in one process (as `-u modA,modB` does, and
    # as CI's test runner does), this module's own module-load pass
    # completes -- and therefore triggers that first resolution --
    # before general_audit_ws_fc75636 is even registered, permanently
    # pinning the field to Odoo's internal "_unknown" placeholder
    # model for the rest of that process (verified with an `odoo
    # shell -u` probe; a later plain restart, with no -u flag, does
    # not hit this because then the field's first resolution happens
    # only after every module has finished loading). Declaring the
    # field in the *review* module instead sidesteps this entirely:
    # review already depends on this module, so by the time review's
    # own fields are set up, both general_audit_ws_b66777d and
    # general_audit_ws_fc75636 are already registered, in every
    # loading order.
    opinion = fields.Html(
        string="Opinion",
        help=(
            "Final narrative of the audit Opinion paragraph, meant to "
            "be filled by clicking Populate (copying "
            "general_audit_ws_fc75636's draft_opinion of the same "
            "General Audit) and then edited manually as needed -- "
            "always editable, regardless of this worksheet's state."
        ),
    )
    basis_for_opinion = fields.Html(
        string="Basis for Opinion",
        help=(
            "Final narrative of the Basis for Opinion paragraph, meant "
            "to be filled by clicking Populate (copying "
            "general_audit_ws_fc75636's draft_basis_for_opinion of the "
            "same General Audit) and then edited manually as needed -- "
            "always editable, regardless of this worksheet's state."
        ),
    )
    key_audit_matters = fields.Html(
        string="Key Audit Matters",
        help=(
            "Final narrative of the Key Audit Matters paragraph, meant "
            "to be filled by clicking Populate (copying "
            "general_audit_ws_fc75636's draft_key_audit_matters of the "
            "same General Audit) and then edited manually as needed -- "
            "always editable, regardless of this worksheet's state. "
            "Situational: only relevant for engagements that require a "
            "Key Audit Matters section."
        ),
    )
    other_information = fields.Html(
        string="Other Information",
        help=(
            "Final narrative of the Other Information paragraph, meant "
            "to be filled by clicking Populate (copying "
            "general_audit_ws_fc75636's draft_other_information of the "
            "same General Audit) and then edited manually as needed -- "
            "always editable, regardless of this worksheet's state. "
            "Situational: only relevant when the engagement includes "
            "other information."
        ),
    )
    responsibilities_of_management = fields.Html(
        string="Responsibilities of Management",
        help=(
            "Final narrative of the Responsibilities of Management "
            "paragraph, meant to be filled by clicking Populate "
            "(copying general_audit_ws_fc75636's "
            "draft_responsibilities_of_management of the same General "
            "Audit) and then edited manually as needed -- always "
            "editable, regardless of this worksheet's state."
        ),
    )
    auditor_responsibilities = fields.Html(
        string="Auditor's Responsibilities",
        help=(
            "Final narrative of the Auditor's Responsibilities "
            "paragraph, meant to be filled by clicking Populate "
            "(copying general_audit_ws_fc75636's "
            "draft_auditor_responsibilities of the same General Audit) "
            "and then edited manually as needed -- always editable, "
            "regardless of this worksheet's state."
        ),
    )
    other_legal_regulatory = fields.Html(
        string="Report on Other Legal and Regulatory Requirements",
        help=(
            "Final narrative of the Report on Other Legal and "
            "Regulatory Requirements section, meant to be filled by "
            "clicking Populate (copying general_audit_ws_fc75636's "
            "draft_other_legal_regulatory of the same General Audit) "
            "and then edited manually as needed -- always editable, "
            "regardless of this worksheet's state. Situational: only "
            "relevant when such requirements apply to the engagement."
        ),
    )
    emphasis_of_matter = fields.Html(
        string="Emphasis of Matter",
        help=(
            "Final narrative of the Emphasis of Matter paragraph, "
            "meant to be filled by clicking Populate (copying "
            "general_audit_ws_fc75636's draft_emphasis_of_matter of "
            "the same General Audit) and then edited manually as "
            "needed -- always editable, regardless of this worksheet's "
            "state. Situational: only relevant when an emphasis of "
            "matter paragraph is needed."
        ),
    )
    other_matter = fields.Html(
        string="Other Matter",
        help=(
            "Final narrative of the Other Matter paragraph, meant to "
            "be filled by clicking Populate (copying "
            "general_audit_ws_fc75636's draft_other_matter of the same "
            "General Audit) and then edited manually as needed -- "
            "always editable, regardless of this worksheet's state. "
            "Situational: only relevant when an other matter paragraph "
            "is needed."
        ),
    )

    def action_populate_final_opinion(self):
        """Button action: (re)populate this worksheet's final opinion.

        Thin dispatcher over ``_populate_final_opinion()``, mirroring
        ``action_populate_detail`` / ``_populate_detail`` above.

        :return: None
        """
        for record in self:
            record._populate_final_opinion()

    def _populate_final_opinion(self):
        """Fill this worksheet's still-empty opinion fields from fc75636.

        Reads ``self.draft_opinion_id`` -- the non-stored compute
        field added by ``ssi_general_audit_worksheet_review`` (see
        the comment above ``opinion`` for why it lives there, not on
        this model directly) -- and, when it resolves to a record,
        writes only the subset of the nine final opinion fields that
        are **currently empty** with the matching ``draft_*``
        narrative from it (``_prepare_final_opinion_vals`` does the
        filtering). A field the auditor already edited manually is
        left untouched -- this is an infill, not an overwrite, so
        clicking Populate again after manual edits is always safe.

        Best-effort like ``_build_lai_number``: checks ``"draft_
        opinion_id" in self._fields`` first (that module may not be
        installed, in which case the field does not exist on this
        model at all), then whether it is empty (fc75636 not
        installed despite the field existing cannot happen given the
        module dependency, but no matching fc75636 record yet for
        this engagement can) -- either way, this does nothing rather
        than raising.

        :return: None
        """
        self.ensure_one()
        if "draft_opinion_id" not in self._fields or not self.draft_opinion_id:
            return
        vals = self._prepare_final_opinion_vals(self.draft_opinion_id)
        if vals:
            self.write(vals)

    def _prepare_final_opinion_vals(self, draft):
        """Build the ``write()`` values copied from a fc75636 record.

        Only includes a key when this worksheet's matching final
        field is currently falsy (``False``/``None``/empty HTML
        string) -- fields already filled (manually or by a previous
        Populate click) are excluded so ``_populate_final_opinion()``
        never overwrites them.

        Extension point: override to add fields to the copy performed
        by ``_populate_final_opinion()``.

        :param draft: the ``general_audit_ws_fc75636`` record this
            worksheet's final opinion is populated from
        :type draft: recordset of ``general_audit_ws_fc75636``
        :return: dict of ``general_audit_ws_b66777d`` values, only
            for fields that are currently empty
        :rtype: dict
        """
        self.ensure_one()
        candidates = {
            "opinion": draft.draft_opinion,
            "basis_for_opinion": draft.draft_basis_for_opinion,
            "key_audit_matters": draft.draft_key_audit_matters,
            "other_information": draft.draft_other_information,
            "responsibilities_of_management": (
                draft.draft_responsibilities_of_management
            ),
            "auditor_responsibilities": (draft.draft_auditor_responsibilities),
            "other_legal_regulatory": draft.draft_other_legal_regulatory,
            "emphasis_of_matter": draft.draft_emphasis_of_matter,
            "other_matter": draft.draft_other_matter,
        }
        return {
            field_name: value
            for field_name, value in candidates.items()
            if not self[field_name]
        }

    team_allocation_ids = fields.One2many(
        string="Final Team Allocations",
        comodel_name="general_audit_ws_b66777d.team_allocation",
        inverse_name="worksheet_id",
        readonly=True,
        help=(
            "One row per hr.employee that contributed preparation "
            "and/or review time to this engagement, (re)populated by "
            "clicking the Populate button "
            "(action_populate_team_allocation) -- empty on a freshly "
            "created worksheet. See _populate_team_allocation()."
        ),
    )

    @api.depends(
        "team_allocation_ids",
        "team_allocation_ids.pe_allocation",
        "team_allocation_ids.ra_allocation",
        "team_allocation_ids.rr_allocation",
        "team_allocation_ids.reporting_allocation",
    )
    def _compute_team_allocation_total(self):
        """Aggregate ``team_allocation_ids``' realized phases, worksheet-wide.

        Mirrors ``general_audit_ws_cbbbaf4``'s own
        ``_compute_total_manhour()`` (Audit Working Plan): this is the
        worksheet-level "Total" the KKA layout shows once for the
        whole engagement, not once per Team Member -- see the
        docstring of ``general_audit_ws_b66777d.team_allocation``
        (row model) for why the per-row total was removed.

        :return: None
        """
        for record in self:
            pe = ra = rr = reporting = 0
            for line in record.team_allocation_ids:
                pe += line.pe_allocation
                ra += line.ra_allocation
                rr += line.rr_allocation
                reporting += line.reporting_allocation
            record.total_pe_allocation = pe
            record.total_ra_allocation = ra
            record.total_rr_allocation = rr
            record.total_reporting_allocation = reporting
            record.total_allocation = pe + ra + rr + reporting

    total_pe_allocation = fields.Integer(
        string="Total Pre-Engagement Allocation",
        compute="_compute_team_allocation_total",
        store=True,
        compute_sudo=True,
        help=(
            "Sum of team_allocation_ids.pe_allocation across every "
            "Team Member of this Independent Auditor's Report -- the "
            '"Total (Independent Auditor Report)" figure, worksheet-'
            "wide, not per employee."
        ),
    )
    total_ra_allocation = fields.Integer(
        string="Total Risk Assessment Allocation",
        compute="_compute_team_allocation_total",
        store=True,
        compute_sudo=True,
        help=(
            "Sum of team_allocation_ids.ra_allocation across every "
            "Team Member of this Independent Auditor's Report -- the "
            '"Total (Independent Auditor Report)" figure, worksheet-'
            "wide, not per employee."
        ),
    )
    total_rr_allocation = fields.Integer(
        string="Total Risk Responses Allocation",
        compute="_compute_team_allocation_total",
        store=True,
        compute_sudo=True,
        help=(
            "Sum of team_allocation_ids.rr_allocation across every "
            "Team Member of this Independent Auditor's Report -- the "
            '"Total (Independent Auditor Report)" figure, worksheet-'
            "wide, not per employee."
        ),
    )
    total_reporting_allocation = fields.Integer(
        string="Total Windup & Reporting Allocation",
        compute="_compute_team_allocation_total",
        store=True,
        compute_sudo=True,
        help=(
            "Sum of team_allocation_ids.reporting_allocation across "
            "every Team Member of this Independent Auditor's Report -- "
            'the "Total (Independent Auditor Report)" figure, '
            "worksheet-wide, not per employee."
        ),
    )
    total_allocation = fields.Integer(
        string="Total Allocation",
        compute="_compute_team_allocation_total",
        store=True,
        compute_sudo=True,
        help=(
            "total_pe_allocation + total_ra_allocation + "
            "total_rr_allocation + total_reporting_allocation -- the "
            'grand "Total (Independent Auditor Report)" figure.'
        ),
    )
    awp_total_pe_allocation = fields.Integer(
        string="AWP Total Pre-Engagement Allocation",
        readonly=True,
        help=(
            "Best-effort copy of this engagement's Audit Working "
            "Plan (general_audit_ws_cbbbaf4) total_pe_manhour -- 0 "
            "when the Audit Working Plan module is not installed, or "
            "no open/done AWP worksheet exists yet for this "
            "engagement. Written (not computed) by "
            "_populate_awp_total_allocation(), called from "
            "_populate_team_allocation() -- refreshed every time the "
            "Populate button is clicked, same as team_allocation_ids "
            "itself."
        ),
    )
    awp_total_ra_allocation = fields.Integer(
        string="AWP Total Risk Assessment Allocation",
        readonly=True,
        help=(
            "Best-effort copy of this engagement's Audit Working "
            "Plan (general_audit_ws_cbbbaf4) total_ra_manhour -- 0 on "
            "the same best-effort conditions as "
            "awp_total_pe_allocation."
        ),
    )
    awp_total_rr_allocation = fields.Integer(
        string="AWP Total Risk Responses Allocation",
        readonly=True,
        help=(
            "Best-effort copy of this engagement's Audit Working "
            "Plan (general_audit_ws_cbbbaf4) total_rr_manhour -- 0 on "
            "the same best-effort conditions as "
            "awp_total_pe_allocation."
        ),
    )
    awp_total_reporting_allocation = fields.Integer(
        string="AWP Total Windup & Reporting Allocation",
        readonly=True,
        help=(
            "Best-effort copy of this engagement's Audit Working "
            "Plan (general_audit_ws_cbbbaf4) total_reporting_manhour "
            "-- 0 on the same best-effort conditions as "
            "awp_total_pe_allocation."
        ),
    )
    awp_total_allocation = fields.Integer(
        string="AWP Total Allocation",
        readonly=True,
        help=(
            "Best-effort copy of this engagement's Audit Working "
            "Plan (general_audit_ws_cbbbaf4) total_manhour -- 0 on "
            "the same best-effort conditions as "
            "awp_total_pe_allocation."
        ),
    )

    @api.depends(
        "total_pe_allocation",
        "awp_total_pe_allocation",
        "total_ra_allocation",
        "awp_total_ra_allocation",
        "total_rr_allocation",
        "awp_total_rr_allocation",
        "total_reporting_allocation",
        "awp_total_reporting_allocation",
        "total_allocation",
        "awp_total_allocation",
    )
    def _compute_team_allocation_diff(self):
        """Compute worksheet-wide realized-vs-planned differences.

        Safe to depend directly on ``awp_total_*`` even though those
        are plain (non-computed) stored fields written by
        ``_populate_awp_total_allocation()``, not by an ``@api.depends``
        chain: both sides of the subtraction belong to ``self``, so
        this never triggers the cross-model ``comodel_name`` resolution
        risk documented above ``opinion``.

        :return: None
        """
        for record in self:
            record.diff_pe_allocation = (
                record.total_pe_allocation - record.awp_total_pe_allocation
            )
            record.diff_ra_allocation = (
                record.total_ra_allocation - record.awp_total_ra_allocation
            )
            record.diff_rr_allocation = (
                record.total_rr_allocation - record.awp_total_rr_allocation
            )
            record.diff_reporting_allocation = (
                record.total_reporting_allocation
                - record.awp_total_reporting_allocation
            )
            record.diff_allocation = (
                record.total_allocation - record.awp_total_allocation
            )

    diff_pe_allocation = fields.Integer(
        string="Difference Pre-Engagement Allocation",
        compute="_compute_team_allocation_diff",
        store=True,
        compute_sudo=True,
        help=(
            "total_pe_allocation minus awp_total_pe_allocation. "
            "Positive means the team worked more Pre-Engagement hours "
            "than planned; negative means less."
        ),
    )
    diff_ra_allocation = fields.Integer(
        string="Difference Risk Assessment Allocation",
        compute="_compute_team_allocation_diff",
        store=True,
        compute_sudo=True,
        help=(
            "total_ra_allocation minus awp_total_ra_allocation. "
            "Positive means the team worked more Risk Assessment "
            "hours than planned; negative means less."
        ),
    )
    diff_rr_allocation = fields.Integer(
        string="Difference Risk Responses Allocation",
        compute="_compute_team_allocation_diff",
        store=True,
        compute_sudo=True,
        help=(
            "total_rr_allocation minus awp_total_rr_allocation. "
            "Positive means the team worked more Risk Responses hours "
            "than planned; negative means less."
        ),
    )
    diff_reporting_allocation = fields.Integer(
        string="Difference Windup & Reporting Allocation",
        compute="_compute_team_allocation_diff",
        store=True,
        compute_sudo=True,
        help=(
            "total_reporting_allocation minus "
            "awp_total_reporting_allocation. Positive means the team "
            "worked more Windup & Reporting hours than planned; "
            "negative means less."
        ),
    )
    diff_allocation = fields.Integer(
        string="Difference Allocation",
        compute="_compute_team_allocation_diff",
        store=True,
        compute_sudo=True,
        help=(
            "total_allocation minus awp_total_allocation -- the grand "
            '"Difference" figure. Positive means the team worked '
            "more hours than planned overall; negative means less."
        ),
    )

    def action_populate_team_allocation(self):
        """Button action: (re)populate this worksheet's ``team_allocation_ids``.

        Thin dispatcher over ``_populate_team_allocation()``, mirroring
        ``action_populate_detail`` / ``_populate_detail`` above.

        :return: None
        """
        for record in self:
            record._populate_team_allocation()

    #: Maps a ``general_audit_worksheet_type_category``'s ``code`` to the
    #: matching realized/AWP phase field prefix on ``team_allocation``
    #: (``<prefix>_allocation`` / ``awp_<prefix>_allocation``). Closed set
    #: of 4, mirroring ``ssi_general_audit``'s ``general_audit_worksheet_
    #: type_category_data.xml`` (worksheet_type_category_pe/ra/rr/wr) --
    #: note code "RE" for Risk Responses, not "RR".
    _TEAM_ALLOCATION_CATEGORY_FIELD = {
        "PE": "pe",
        "RA": "ra",
        "RE": "rr",
        "WR": "reporting",
    }

    def _populate_team_allocation(self):
        """Replace ``team_allocation_ids`` with a fresh aggregation.

        Searches every ``general_audit_worksheet`` (the shared shadow
        model backing every worksheet type -- see
        ``ssi_general_audit``'s ``general_audit_worksheet``) sharing
        this worksheet's ``general_audit_id``, and sums each one's
        ``preparation_time`` onto its ``user_id.employee_id`` and
        ``review_time`` onto its ``reviewer_id.employee_id``, bucketed
        by audit phase (see ``_compute_team_allocation_totals()``). One
        row per ``hr.employee`` that contributed at least one of the
        two is (re)created.

        This doubles as the "Reload" behaviour requested for stale
        historical data (issue #383, open question #1): every click
        unlinks the previous snapshot and re-reads current worksheet
        data from scratch, so values filled in after the fact are
        picked up the next time Populate is clicked -- no separate
        field/button is needed.

        Like ``_populate_detail()``, this is unlink-then-recreate: a
        full snapshot taken at click time, not a live-reactive
        summary -- callers must not assume ``team_allocation_ids`` row
        ``id`` stability across two Populate clicks. A worksheet whose
        ``user_id``/``reviewer_id`` has no linked ``hr.employee``
        (``res.users.employee_id`` empty) contributes nothing for that
        half -- best-effort, matching ``_populate_final_opinion``'s
        treatment of missing data.

        Uses ``sudo()`` for the ``unlink()``/``create()`` calls, same
        rationale as ``_populate_detail()``: this model's ACL grants 0
        create/write/unlink to every group (rows are system-populated
        only), so without ``sudo()`` this would raise ``AccessError``
        for every user, including the one clicking Populate.

        Also refreshes this worksheet's own AWP total fields
        (``awp_total_pe_allocation`` etc., via
        ``_populate_awp_total_allocation()``) so the "Total (AWP)"
        group shown next to the tree stays in step with the latest
        Audit Working Plan data every time Populate is clicked --
        this worksheet's own realized totals (``total_pe_allocation``
        etc.) and their Difference need no such call, since those are
        plain computed fields that recompute on their own whenever
        ``team_allocation_ids`` changes.

        :return: None
        """
        self.ensure_one()
        self.team_allocation_ids.sudo().unlink()
        TeamAllocation = self.env["general_audit_ws_b66777d.team_allocation"].sudo()
        for employee_id, times in self._compute_team_allocation_totals().items():
            TeamAllocation.create(
                self._prepare_team_allocation_vals(employee_id, times)
            )
        self._populate_awp_total_allocation()

    def _compute_team_allocation_totals(self):
        """Aggregate preparation/review time per ``hr.employee`` & phase.

        Each ``general_audit_worksheet``'s audit phase is read from its
        own ``parent_type_id.category_id`` (NOT a flat single number
        per worksheet) -- see ``_TEAM_ALLOCATION_CATEGORY_FIELD``. A
        worksheet whose ``parent_type_id`` is empty, or whose
        ``parent_type_id.category_id`` is empty (e.g. legacy data),
        contributes 0 to every phase bucket rather than raising --
        its time is simply not attributable to a phase. It still
        counts this employee as "contributing" (gets a row) as long
        as some worksheet -- categorized or not -- recorded time for
        them.

        :return: mapping of ``hr.employee`` id to a four-key dict,
            ``{"pe": int, "ra": int, "rr": int, "reporting": int}``,
            summed across every ``general_audit_worksheet`` sharing
            this worksheet's ``general_audit_id``
        :rtype: dict
        """
        self.ensure_one()
        totals = {}
        worksheets = self.env["general_audit_worksheet"].search(
            [("general_audit_id", "=", self.general_audit_id.id)]
        )
        for worksheet in worksheets:
            category_field = None
            if worksheet.parent_type_id and worksheet.parent_type_id.category_id:
                category_field = self._TEAM_ALLOCATION_CATEGORY_FIELD.get(
                    worksheet.parent_type_id.category_id.code
                )
            prep_employee = worksheet.user_id.employee_id
            if prep_employee and worksheet.preparation_time:
                entry = totals.setdefault(
                    prep_employee.id,
                    {"pe": 0, "ra": 0, "rr": 0, "reporting": 0},
                )
                if category_field:
                    entry[category_field] += worksheet.preparation_time
            review_employee = worksheet.reviewer_id.employee_id
            if review_employee and worksheet.review_time:
                entry = totals.setdefault(
                    review_employee.id,
                    {"pe": 0, "ra": 0, "rr": 0, "reporting": 0},
                )
                if category_field:
                    entry[category_field] += worksheet.review_time
        return totals

    def _prepare_team_allocation_vals(self, employee_id, times):
        """Build the values of one ``team_allocation_ids`` row.

        No planned (AWP) figures are included here: since issue #383's
        design revision, "Total"/"AWP Total"/"Difference" are all
        worksheet-wide aggregates (``total_pe_allocation`` etc.,
        ``awp_total_pe_allocation`` etc.), not per-row columns -- see
        ``general_audit_ws_b66777d.team_allocation``'s docstring and
        ``_populate_awp_total_allocation()`` below.

        Extension point: override to add fields to each row created
        by ``_populate_team_allocation()``.

        :param employee_id: id of the ``hr.employee`` this row
            aggregates
        :type employee_id: int
        :param times: ``{"pe": int, "ra": int, "rr": int,
            "reporting": int}`` totals for this employee, as built by
            ``_compute_team_allocation_totals()``
        :type times: dict
        :return: dict of ``general_audit_ws_b66777d.team_allocation``
            values
        :rtype: dict
        """
        self.ensure_one()
        return {
            "worksheet_id": self.id,
            "team_id": employee_id,
            "pe_allocation": times["pe"],
            "ra_allocation": times["ra"],
            "rr_allocation": times["rr"],
            "reporting_allocation": times["reporting"],
        }

    def _get_awp_worksheet(self):
        """Best-effort lookup of this engagement's Audit Working Plan.

        Looks up the ``general_audit_ws_cbbbaf4`` (Audit Working Plan)
        record sharing this worksheet's ``general_audit_id``, whose
        ``state`` is ``open`` or ``done`` -- a draft/cancelled AWP is
        not treated as this engagement's planned figures.

        ``ssi_general_audit_worksheet_audit_working_plan`` (the module
        providing ``general_audit_ws_cbbbaf4``) neither depends on
        this module nor is depended on by it, so that model is not
        guaranteed to be registered when this method runs -- checked
        via ``in self.env`` before searching, same pattern as
        ``_populate_final_opinion``. Returns ``None`` (never raises)
        when the model is not installed or no matching AWP worksheet
        exists yet for this engagement -- callers treat ``None`` as
        all-zero.

        Reads with ``sudo()``, same rationale as
        ``_populate_final_opinion``: the two worksheets can be
        assigned to different users within the same engagement.

        :return: the matching AWP worksheet, or ``None``
        :rtype: recordset of ``general_audit_ws_cbbbaf4`` or ``None``
        """
        self.ensure_one()
        if "general_audit_ws_cbbbaf4" not in self.env:
            return None
        awp = (
            self.env["general_audit_ws_cbbbaf4"]
            .sudo()
            .search(
                [
                    ("general_audit_id", "=", self.general_audit_id.id),
                    ("state", "in", ["open", "done"]),
                ],
                limit=1,
                order="id desc",
            )
        )
        return awp or None

    def _populate_awp_total_allocation(self):
        """(Re)fill this worksheet's ``awp_total_*`` fields from the AWP.

        Copies ``general_audit_ws_cbbbaf4``'s own worksheet-wide
        ``total_pe_manhour``/``total_ra_manhour``/``total_rr_manhour``/
        ``total_reporting_manhour``/``total_manhour`` (``Float``) into
        this worksheet's ``awp_total_pe_allocation`` etc. (``Integer``,
        ``int()``-ed here). These are plain stored fields, NOT
        ``compute=``, deliberately: a field-level
        ``fields.Many2one(comodel_name="general_audit_ws_cbbbaf4", ...)``
        anywhere on this module's models risks the same "_unknown"
        comodel bug already documented above ``opinion`` for
        ``draft_opinion_id`` -- resolving the model by string inside
        this method's body at call time (via
        ``_get_awp_worksheet()``) is safe because every module is
        fully loaded by the time a Populate click actually runs.

        Called from ``_populate_team_allocation()`` so these fields
        are refreshed on every Populate click, same "Reload" semantics
        as ``team_allocation_ids`` itself -- best-effort all-zero (see
        ``_get_awp_worksheet()``) when no AWP is available.

        :return: None
        """
        self.ensure_one()
        awp = self._get_awp_worksheet()
        self.awp_total_pe_allocation = int(awp.total_pe_manhour) if awp else 0
        self.awp_total_ra_allocation = int(awp.total_ra_manhour) if awp else 0
        self.awp_total_rr_allocation = int(awp.total_rr_manhour) if awp else 0
        self.awp_total_reporting_allocation = (
            int(awp.total_reporting_manhour) if awp else 0
        )
        self.awp_total_allocation = int(awp.total_manhour) if awp else 0

    def action_populate_detail(self):
        """Button action: (re)populate this worksheet's ``detail_ids``.

        Thin dispatcher over ``_populate_detail()``, mirroring
        ``ssi_custom_information_mixin``'s own
        ``action_reload_custom_info`` / ``_reload_custom_info`` split
        (``mixin_custom_info.py``).

        :return: None
        """
        for record in self:
            record._populate_detail()

    def _populate_detail(self):
        """Replace ``detail_ids`` with a fresh snapshot of every active
        ``general_audit_ws_b66777d.property``.

        The properties themselves are master data now (Configuration
        menu), not a fixed Python constant -- so unlike the previous
        revision of this method there is no closed set of "11 rows" to
        reason about: whatever is active in
        ``general_audit_ws_b66777d.property`` at the moment Populate is
        clicked is exactly what gets snapshotted. There is still no
        "still relevant" existing row to preserve the way
        ``ssi_custom_information_mixin._reload_custom_info`` preserves
        rows that still match its template: every property is
        (re)evaluated fresh on every click, so the correct behaviour
        remains unlink-everything-then-create-everything -- callers
        must not assume ``detail_ids`` row ``id`` stability across two
        Populate clicks.

        Uses ``sudo()`` for both the ``unlink()`` and the ``create()``
        calls because ``general_audit_ws_b66777d.detail``'s own
        ``ir.model.access.csv`` grants 0 create/write/unlink to every
        group (the issue's Keputusan Desain: "Details" rows are
        system-populated only, via this method, never manually
        editable) -- without ``sudo()`` this would raise
        ``AccessError`` for every user, including the one clicking
        Populate. ``general_audit_ws_b66777d.property`` itself is a
        regular master data model (full CRUD for this worksheet's user
        group) and is only ever read here, never written.

        :return: None
        """
        self.ensure_one()
        self.detail_ids.sudo().unlink()
        Detail = self.env["general_audit_ws_b66777d.detail"].sudo()
        properties = self.env["general_audit_ws_b66777d.property"].search(
            [], order="sequence, id"
        )
        for prop in properties:
            Detail.create(self._prepare_detail_vals(prop))

    def _prepare_detail_vals(self, prop):
        """Build the values of one ``detail_ids`` row.

        ``python_code`` is COPIED from ``prop.python_code`` here (not
        ``related=`` on the field) so this row's snapshot is unaffected
        by the master data being edited afterwards -- see
        ``general_audit_ws_b66777d.detail.python_code``'s own help
        text.

        Extension point: override to add fields to each row created by
        ``_populate_detail()``.

        :param prop: the ``general_audit_ws_b66777d.property`` master
            record this row is populated from
        :type prop: recordset of ``general_audit_ws_b66777d.property``
        :return: dict of ``general_audit_ws_b66777d.detail`` values
        :rtype: dict
        """
        self.ensure_one()
        return {
            "worksheet_id": self.id,
            "property_id": prop.id,
            "python_code": prop.python_code,
        }

    @ssi_decorator.post_open_action()
    def _10_generate_lai_number(self):
        """Fill ``lai_number`` from ``_build_lai_number`` when opened.

        Runs after ``action_open`` (``post_open_action`` hook). Only fills
        ``lai_number`` when it is still empty, so a value entered manually
        before opening the worksheet is never overwritten.

        :return: None
        """
        self.ensure_one()
        if not self.lai_number:
            self.lai_number = self._build_lai_number()

    def _build_lai_number(self):
        """Build the physical LAI Number for this worksheet.

        LAI = Laporan Auditor Independen, the physical independent
        auditor's report handed to the client. Its numbering format was
        confirmed against the client's own instance (``kapswr.id`` /
        MCP ``odoo14-hwr``, ``sequence.template`` id=67, model
        ``accountant.assurance_report``) and is reproduced here segment
        by segment, joined with ``/`` (``AP`` and ``subsequence`` are
        joined with ``-`` into one segment):

        - ``seq`` -- running number from the ``ir.sequence`` with code
          ``general_audit_ws_b66777d.lai_number`` (5-digit, no
          prefix/suffix of its own -- every other segment below is
          appended in Python, not by the sequence), e.g. ``"00086"``.
        - ``office_code`` -- last 6 characters of the CPA firm's own
          license number: this worksheet's own ``company_id.partner_id``
          (the audit firm, NOT the audited client -- unlike every other
          segment below this one is not read from ``general_audit_id``),
          its ``res.partner.id_number`` with ``category_id.code ==
          "cpa_firm_license"`` and ``status == "open"``, e.g.
          ``"2.1470"``. Best-effort: ``""`` when no such record exists.
        - ``service_code`` -- ``general_audit_id.service_id.code``,
          e.g. ``"AU.1"``. Best-effort: ``""`` when ``service_id`` (or
          its ``code``) is unset.
        - ``sector_code`` --
          ``general_audit_id.industry_id.accountant_service_code``,
          e.g. ``"05"``. Best-effort: ``""`` when ``industry_id`` (or
          its code) is unset.
        - ``AP`` -- last 4 characters of
          ``general_audit_id.accountant_id.cpa_license``, e.g.
          ``"1983"``. Best-effort: ``"0000"`` when ``accountant_id`` or
          its CPA license is unset.
        - ``subsequence`` --
          ``general_audit_id.num_of_consecutive_audit_accountant`` as a
          plain string, e.g. ``"1"``.
        - ``npwp_flag`` -- ``"1"`` when ``general_audit_id.partner_id.vat``
          is set, else ``"0"``.
        - ``roman_month`` -- month of ``general_audit_id.date`` as an
          upper-case Roman numeral (``"VIII"`` for August).
        - ``year`` -- year of ``general_audit_id.date``, e.g. ``"2026"``.

        Final shape (example): ``"00086/2.1470/AU.1/05/1983-1/1/VIII/
        2026"``.

        Every segment above is **best-effort**: a General Audit with
        incomplete data (missing ``accountant_id``, ``industry_id``,
        ``service_id``, CPA license, or the audit firm's own CPA firm
        license) does not stop ``action_open`` from succeeding -- the
        corresponding segment is simply left blank or placeholder, and
        the auditor is expected to complete/correct ``lai_number``
        manually afterwards. ``general_audit_id.date`` is the only
        source field treated as always present, since it is
        ``required=True`` on ``general_audit`` itself; it still falls
        back to an empty ``roman_month``/``year`` rather than raising if
        that assumption is ever violated.

        :return: the formatted LAI Number string
        :rtype: str
        """
        self.ensure_one()
        audit = self.general_audit_id

        seq = (
            self.env["ir.sequence"].next_by_code("general_audit_ws_b66777d.lai_number")
            or ""
        )

        office_code = ""
        firm_partner = self.company_id.partner_id
        if firm_partner:
            id_number = self.env["res.partner.id_number"].search(
                [
                    ("partner_id", "=", firm_partner.id),
                    ("category_id.code", "=", "cpa_firm_license"),
                    ("status", "=", "open"),
                ],
                limit=1,
                order="id desc",
            )
            if id_number.name:
                office_code = id_number.name[-6:]

        service_code = ""
        if audit and audit.service_id and audit.service_id.code:
            service_code = audit.service_id.code

        sector_code = ""
        if audit and audit.industry_id and audit.industry_id.accountant_service_code:
            sector_code = audit.industry_id.accountant_service_code

        ap = "0000"
        if audit and audit.accountant_id and audit.accountant_id.cpa_license:
            ap = audit.accountant_id.cpa_license[-4:]

        subsequence = str(audit.num_of_consecutive_audit_accountant) if audit else "0"

        npwp_flag = "1" if audit and audit.partner_id and audit.partner_id.vat else "0"

        roman_month = ""
        year = ""
        if audit and audit.date:
            roman_month = _ROMAN_NUMERAL_MONTHS.get(audit.date.month, "")
            year = str(audit.date.year)

        return "/".join(
            [
                seq,
                office_code,
                service_code,
                sector_code,
                f"{ap}-{subsequence}",
                npwp_flag,
                roman_month,
                year,
            ]
        )
