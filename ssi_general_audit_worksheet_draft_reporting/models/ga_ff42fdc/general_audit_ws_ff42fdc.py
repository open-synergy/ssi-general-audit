# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSff42fdc(models.Model):
    """Worksheet — Audit Result / Opinion Formalisation (ff42fdc).

    Records and formalises the final audit opinion for the engagement:
    * ``financial_statement_opinion_id`` — the type of opinion issued
      (e.g., Unmodified, Qualified, Adverse, Disclaimer), linked to and
      stored back on the General Audit record.
    * ``financial_statement_opinion_date`` — the date of the opinion,
      also synchronised with the General Audit record.

    It also records two further opinions, local to this worksheet only
    (not written back to the General Audit):
    * ``compliance_law_opinion_id`` / ``compliance_law_opinion_date`` --
      opinion on compliance with laws and regulations.
    * ``compliance_internal_control_opinion_id`` /
      ``compliance_internal_control_opinion_date`` -- opinion on
      compliance with internal control.

    It also presents the engagement's Posture Report (``posture_ids``):
    one ``general_audit_ws_ff42fdc.posture`` line per client account
    group plus nine fixed Total/Subtotal lines (Total Asset, Total
    Liability, Total Equity, Total Liability and Equity, Gross Profit,
    Operating Profit, Profit Before Tax, Profit After Tax,
    Comprehensive Profit), summarising Unaudited, Adjustment
    (Debit/Credit), Audited, and Previous amounts. Use
    ``action_load_posture`` to synchronise the posture lines with the
    account groups in use on the General Audit.

    This worksheet provides the definitive audit-file record of the opinion
    and serves as evidence that the engagement-level decision was made and
    documented in accordance with ISA 700 / SA 700.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 700/SA 700 (Forming an Opinion);
    ISA 705/SA 705 (Modifications to the Opinion).
    """

    _name = "general_audit_ws_ff42fdc"
    _description = "Audit Result (ff42fdc)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_draft_reporting." "worksheet_type_ff42fdc"
    )

    # Fixed display order of posture_ids: (line_type, code) pairs, where
    # code is group_id.code for "group" lines and total_type for
    # "total" lines. Position in this list drives `sequence` via
    # `_resequence_posture_lines` -- Total rows are interleaved right
    # after their last component group, per the WR.170.1 reference
    # sheet layout.
    _POSTURE_LINE_ORDER = (
        ("group", "T001"),
        ("group", "T002"),
        ("total", "total_asset"),
        ("group", "T003"),
        ("group", "T004"),
        ("total", "total_liability"),
        ("group", "T005"),
        ("group", "T007"),
        ("total", "total_equity"),
        ("total", "total_liability_equity"),
        ("group", "T009"),
        ("group", "T011"),
        ("total", "gross_profit"),
        ("group", "T012"),
        ("total", "operating_profit"),
        ("group", "T010"),
        ("group", "T013"),
        ("total", "profit_before_tax"),
        ("group", "T014"),
        ("total", "profit_after_tax"),
        # T015 (Other Comprehensive Income) contributes to
        # `comprehensive_profit`, so it is interleaved right here.
        ("group", "T015"),
        ("total", "comprehensive_profit"),
    )

    financial_statement_opinion_id = fields.Many2one(
        comodel_name="accountant.opinion",
        string="Opinion on Financial Statement",
        related="general_audit_id.opinion_id",
        store=True,
        readonly=False,
        inverse="_inverse_financial_statement_opinion_id",
        states={
            "open": [("readonly", False)],
        },
        help="Audit opinion issued for the engagement. Writing this "
        "field also updates ``opinion_id`` on the General Audit.",
    )
    financial_statement_opinion_date = fields.Date(
        string="Date of Opinion on Financial Statement",
        related="general_audit_id.opinion_date",
        store=True,
        readonly=False,
        inverse="_inverse_financial_statement_opinion_date",
        states={
            "open": [("readonly", False)],
        },
        help="Date of the audit opinion. Writing this field also "
        "updates ``opinion_date`` on the General Audit.",
    )
    compliance_law_opinion_id = fields.Many2one(
        comodel_name="accountant.opinion",
        string="Opinion on Compliance with Laws and Regulations",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Opinion on the engagement's compliance with applicable "
        "laws and regulations. Local to this worksheet; not written "
        "back to the General Audit.",
    )
    compliance_law_opinion_date = fields.Date(
        string="Date of Opinion on Compliance with Laws and Regulations",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Date of the opinion on compliance with laws and "
        "regulations. Local to this worksheet.",
    )
    compliance_internal_control_opinion_id = fields.Many2one(
        comodel_name="accountant.opinion",
        string="Opinion on Compliance with Internal Control",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Opinion on the engagement's compliance with internal "
        "control. Local to this worksheet; not written back to the "
        "General Audit.",
    )
    compliance_internal_control_opinion_date = fields.Date(
        string="Date of Opinion on Compliance with Internal Control",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Date of the opinion on compliance with internal "
        "control. Local to this worksheet.",
    )
    posture_ids = fields.One2many(
        comodel_name="general_audit_ws_ff42fdc.posture",
        inverse_name="worksheet_id",
        string="Posture Report",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
        help="Financial statement posture: one line per client account "
        "group in use plus nine fixed Total/Subtotal lines, loaded "
        "from the General Audit's account detail lines.",
    )

    def action_load_posture(self):
        """Synchronise ``posture_ids`` with the audited account groups.

        Calls ``_load_posture`` on every record in ``self``, run with
        ``sudo()`` so users without direct write access on
        ``general_audit_ws_ff42fdc.posture`` can still trigger the
        reload from the button.
        """
        for record in self.sudo():
            record._load_posture()

    def _load_posture(self):
        """Add/remove posture lines to match the audited account groups.

        Diffs the account groups derived from
        ``general_audit_id.detail_ids.account_id.group_id`` against the
        Account Group lines already present on ``posture_ids``: a line
        is created for every group newly in use, and a line is removed
        for every group no longer represented in the audit detail.
        Mirrors ``general_audit_ws_b26d482._load_detail``.

        The nine Total lines (one per ``total_type``) are created once
        each, the first time this worksheet loads posture -- they
        always exist afterwards, regardless of whether their component
        groups have any data. Every line's ``sequence`` is (re)assigned
        via ``_resequence_posture_lines``. Finally, every existing
        Total line's amounts are force-recomputed: they are not
        reactively linked to
        ``general_audit_ws_ff42fdc.total_formula`` (an
        ``@api.depends`` cannot express "any formula row for my
        total_type"), so this Reload is what applies an edited
        formula to a worksheet that already has its Total lines.

        :return: nothing; writes ``posture_ids``
        """
        self.ensure_one()
        posture_model = self.env["general_audit_ws_ff42fdc.posture"]

        group_lines = self.posture_ids.filtered(lambda p: p.line_type == "group")
        all_groups = self.general_audit_id.mapped("detail_ids.account_id.group_id")
        existing_groups = group_lines.mapped("group_id")

        groups_to_add = all_groups - existing_groups
        groups_to_remove = existing_groups - all_groups

        # Add posture line
        for group in groups_to_add:
            posture_model.create(
                {
                    "worksheet_id": self.id,
                    "line_type": "group",
                    "group_id": group.id,
                }
            )

        # Remove posture line
        postures_to_remove = group_lines.filtered(
            lambda p: p.group_id in groups_to_remove
        )
        if postures_to_remove:
            postures_to_remove.unlink()

        # Ensure every Total line exists; they are never removed.
        total_lines = self.posture_ids.filtered(lambda p: p.line_type == "total")
        existing_total_types = total_lines.mapped("total_type")
        total_type_field = posture_model._fields["total_type"]
        for total_type, _label in total_type_field.selection:
            if total_type not in existing_total_types:
                posture_model.create(
                    {
                        "worksheet_id": self.id,
                        "line_type": "total",
                        "total_type": total_type,
                    }
                )

        self._resequence_posture_lines()

        # Force-recompute Total lines so an edited
        # general_audit_ws_ff42fdc.total_formula takes effect now,
        # instead of waiting for an unrelated detail_ids change.
        total_lines = self.posture_ids.filtered(lambda p: p.line_type == "total")
        total_lines._compute_amounts()

    def _resequence_posture_lines(self):
        """Assign ``sequence`` on ``posture_ids`` for the fixed layout.

        Lines whose ``(line_type, code)`` pair is listed in
        ``_POSTURE_LINE_ORDER`` are placed at ten times their position
        in that list, leaving gaps between them. A group line whose
        account group is not part of the formula table (a custom
        ``client_account_group`` code, outside T001-T015) is placed
        after every listed line, ordered by the group's own
        ``sequence``/``id``, so the table still renders
        deterministically.

        :return: nothing; writes ``sequence`` on every line of
            ``posture_ids``
        """
        self.ensure_one()
        order_index = {
            key: position for position, key in enumerate(self._POSTURE_LINE_ORDER)
        }
        unmatched = self.posture_ids.filtered(
            lambda p: p._posture_line_order_key() not in order_index
        ).sorted(key=lambda p: (p.group_id.sequence, p.group_id.id))
        fallback_base = len(self._POSTURE_LINE_ORDER) * 10
        unmatched_sequence = {
            posture.id: fallback_base + position * 10
            for position, posture in enumerate(unmatched)
        }
        for posture in self.posture_ids:
            key = posture._posture_line_order_key()
            if key in order_index:
                posture.sequence = order_index[key] * 10
            else:
                posture.sequence = unmatched_sequence[posture.id]

    def _inverse_financial_statement_opinion_id(self):
        """Write ``financial_statement_opinion_id`` back to the audit.

        Odoo attaches the automatic related-field inverse only when
        neither the related field nor its target is ``readonly`` at the
        Python level (``Field._setup_related_full``). The target here,
        ``general_audit.opinion_id``, is declared ``readonly=True`` and
        is unlocked for the form through ``states`` only (``states``
        drives the view, not ``Field.readonly``), so no inverse is ever
        generated and the value would be kept on the worksheet alone.
        This explicit inverse restores the write-through documented on
        the model.

        Side effect: writes ``opinion_id`` on the linked
        ``general_audit`` record. The write is done with ``sudo()``
        because worksheet users are not required to hold write access
        on ``general_audit`` itself.
        """
        for record in self.sudo():
            if record.general_audit_id:
                opinion = record.financial_statement_opinion_id
                record.general_audit_id.write({"opinion_id": opinion.id})

    def _inverse_financial_statement_opinion_date(self):
        """Write ``financial_statement_opinion_date`` back to the audit.

        Counterpart of ``_inverse_financial_statement_opinion_id`` for
        ``general_audit.opinion_date``, which is readonly at the Python
        level for the same reason and therefore also needs an explicit
        inverse.

        Side effect: writes ``opinion_date`` on the linked
        ``general_audit`` record, with ``sudo()`` for the same reason.
        """
        for record in self.sudo():
            if record.general_audit_id:
                opinion_date = record.financial_statement_opinion_date
                record.general_audit_id.write({"opinion_date": opinion_date})
