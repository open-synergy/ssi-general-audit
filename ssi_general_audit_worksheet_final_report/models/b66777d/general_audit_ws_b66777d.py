# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models

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
        """Copy the nine opinion fields from this engagement's fc75636.

        Looks up the ``general_audit_ws_fc75636`` (Independen Auditor
        Report Review) record sharing this worksheet's
        ``general_audit_id`` and, when found, copies its nine
        ``draft_*`` narrative fields onto this worksheet's matching
        final fields via ``write()`` (not ``related=``, so the copy is
        a point-in-time snapshot the auditor can then freely edit).

        ``ssi_general_audit_worksheet_review`` (the module providing
        ``general_audit_ws_fc75636``) depends on *this* module, never
        the other way around, so that model is not guaranteed to be
        registered when this method runs -- checked via ``in
        self.env`` before searching. Best-effort like
        ``_build_lai_number``: when the model is not installed, or no
        matching fc75636 record exists yet for this engagement, this
        does nothing rather than raising.

        Reads the fc75636 record with ``sudo()`` (same rationale as
        ``_compute_audit_final_memorandum_id``'s ``compute_sudo=True``
        above): the two worksheets can be assigned to different users
        within the same engagement, and this best-effort copy should
        not fail with an ``AccessError`` for a user who can open this
        worksheet but was not also granted read access on fc75636.

        :return: None
        """
        self.ensure_one()
        if "general_audit_ws_fc75636" not in self.env:
            return
        draft = (
            self.env["general_audit_ws_fc75636"]
            .sudo()
            .search(
                [("general_audit_id", "=", self.general_audit_id.id)],
                limit=1,
                order="id desc",
            )
        )
        if not draft:
            return
        self.write(self._prepare_final_opinion_vals(draft))

    def _prepare_final_opinion_vals(self, draft):
        """Build the ``write()`` values copied from a fc75636 record.

        Extension point: override to add fields to the copy performed
        by ``_populate_final_opinion()``.

        :param draft: the ``general_audit_ws_fc75636`` record this
            worksheet's final opinion is populated from
        :type draft: recordset of ``general_audit_ws_fc75636``
        :return: dict of ``general_audit_ws_b66777d`` values
        :rtype: dict
        """
        self.ensure_one()
        return {
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
