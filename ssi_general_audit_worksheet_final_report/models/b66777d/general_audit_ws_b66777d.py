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


def _computation_item_python_code(item_name):
    """Build the ``python_code`` for a "Details" row #4-10.

    Each of these rows looks up its amount from
    ``general_audit.computation_ids`` by the linked
    ``trial_balance_computation_item.name`` (NOT ``code`` -- the issue's
    Keputusan Desain is explicit about this, since ``code`` values like
    ``T100`` carry no meaning for a reader of this table), taking the
    first matching line's ``audited_amount``. Falls back to ``0.0``
    when no such computation item exists on the General Audit (e.g. a
    General Audit created before that computation item existed, or one
    whose account type set never seeded it).

    :param item_name: exact ``trial_balance_computation_item.name`` to
        match, e.g. ``"Total Revenue"``
    :type item_name: str
    :return: ``python_code`` source, ready for ``safe_eval``
    :rtype: str
    """
    return (
        "result = 0.0\n"
        "lines = document.worksheet_id.general_audit_id.computation_ids"
        ".filtered(\n"
        '    lambda c: c.computation_item_id.name == "{}"\n'
        ")\n"
        "if lines:\n"
        "    result = lines[0].audited_amount\n"
    ).format(item_name)


#: Python code for "Details" row #3 (Data Laporan Keuangan Yang Digunakan),
#: exactly as specified by the issue's Keputusan Desain: the audit period
#: length in whole calendar months, counted inclusively (Jan-Dec = 12).
_FINANCIAL_REPORT_PERIOD_PYTHON_CODE = (
    "ga = document.worksheet_id.general_audit_id\n"
    "months = 0\n"
    "if ga.date_start and ga.date_end:\n"
    "    months = (\n"
    "        (ga.date_end.year - ga.date_start.year) * 12\n"
    "        + (ga.date_end.month - ga.date_start.month)\n"
    "        + 1\n"
    "    )\n"
    "if months == 12:\n"
    '    result = "Yearly Financial Report"\n'
    "elif months and months < 12:\n"
    '    result = "Interim Financial Report"\n'
    "elif months > 12:\n"
    '    result = "More than 12 months"\n'
    "else:\n"
    '    result = ""\n'
)

#: The 11 fixed "Details" rows (re)populated by
#: ``GeneralAuditWSb66777d._populate_detail()`` -- ``(property,
#: python_code)``. Deliberately a Python constant, not XML master data:
#: these rows are specific to this one worksheet model, never reused or
#: user-editable elsewhere (issue's Keputusan Desain).
_DETAIL_ROWS = [
    (
        "Standar Akuntansi Keuangan yang Digunakan oleh klien",
        "result = (\n"
        "    document.worksheet_id.general_audit_id\n"
        '    .financial_accounting_standard_id.name or ""\n'
        ")\n",
    ),
    (
        "Mata Uang Yang Digunakan",
        "result = (\n"
        "    document.worksheet_id.general_audit_id.currency_id.name\n"
        '    or ""\n'
        ")\n",
    ),
    (
        "Data Laporan Keuangan Yang Digunakan",
        _FINANCIAL_REPORT_PERIOD_PYTHON_CODE,
    ),
    ("Revenue", _computation_item_python_code("Total Revenue")),
    ("Total Asset", _computation_item_python_code("Total Asset")),
    ("Total Liability", _computation_item_python_code("Total Liability")),
    ("EBIT", _computation_item_python_code("EBIT")),
    ("Tax Expense", _computation_item_python_code("Tax Expense")),
    ("Total Net Profit", _computation_item_python_code("Total Net Profit")),
    (
        "Total Net Profit & OCI",
        _computation_item_python_code("Total Net Profit & OCI"),
    ),
    (
        "Konsolidasi",
        "result = (\n"
        "    document.worksheet_id.general_audit_id.partner_id\n"
        '    .entity_type_id.name or ""\n'
        ")\n",
    ),
]


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
            "11 fixed summary rows (Property/Value), (re)populated by "
            "clicking the Populate button (action_populate_detail) -- "
            "empty on a freshly created worksheet. See "
            "_populate_detail()."
        ),
    )

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
        """Replace ``detail_ids`` with a fresh snapshot of the 11 rows.

        Unlike ``ssi_custom_information_mixin._reload_custom_info``
        (which diffs against a configurable template and only
        unlinks/creates the rows that actually changed), this worksheet
        has no such template: ``_DETAIL_ROWS`` is a fixed constant of
        exactly 11 properties, so there is never a "still relevant"
        existing row to preserve. The correct behaviour degenerates to
        unlink-everything-then-create-everything, every time this is
        called -- callers must not assume row ``id`` stability across
        two Populate clicks.

        Uses ``sudo()`` for both the ``unlink()`` and the ``create()``
        calls because this model's own ``ir.model.access.csv`` grants 0
        create/write/unlink to every group (the issue's Keputusan
        Desain: "Details" is system-populated only, via this method,
        never manually editable) -- without ``sudo()`` this would raise
        ``AccessError`` for every user, including the one clicking
        Populate.

        :return: None
        """
        self.ensure_one()
        self.detail_ids.sudo().unlink()
        Detail = self.env["general_audit_ws_b66777d.detail"].sudo()
        for property_name, python_code in _DETAIL_ROWS:
            Detail.create(self._prepare_detail_vals(property_name, python_code))

    def _prepare_detail_vals(self, property_name, python_code):
        """Build the values of one ``detail_ids`` row.

        Extension point: override to add fields to each of the 11 rows
        created by ``_populate_detail()`` (e.g. a glue module adding a
        12th property without rewriting ``_DETAIL_ROWS``).

        :param property_name: label for the row, e.g. ``"Revenue"``
        :type property_name: str
        :param python_code: source evaluated to fill the row's Value
        :type python_code: str
        :return: dict of ``general_audit_ws_b66777d.detail`` values
        :rtype: dict
        """
        self.ensure_one()
        return {
            "worksheet_id": self.id,
            "property": property_name,
            "python_code": python_code,
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
