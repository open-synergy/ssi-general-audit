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
