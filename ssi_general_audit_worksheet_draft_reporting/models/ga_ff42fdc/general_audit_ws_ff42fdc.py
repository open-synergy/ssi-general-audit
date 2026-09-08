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

    It also presents the engagement's Posture Report: one
    ``general_audit_ws_ff42fdc.posture`` line per client account group
    (``posture_ids``), summarising Unaudited, Adjustment (Debit/Credit),
    and Audited amounts. Use ``action_load_posture`` to synchronise the
    posture lines with the account groups in use on the General Audit.

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
    posture_ids = fields.One2many(
        comodel_name="general_audit_ws_ff42fdc.posture",
        inverse_name="worksheet_id",
        string="Posture Report",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
        help="Financial statement posture per client account group, "
        "loaded from the General Audit's account detail lines.",
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
        groups already present on ``posture_ids``: a line is created
        for every group newly in use, and a line is removed for every
        group no longer represented in the audit detail. Mirrors
        ``general_audit_ws_b26d482._load_detail``.
        """
        self.ensure_one()
        posture_model = self.env["general_audit_ws_ff42fdc.posture"]

        all_groups = self.general_audit_id.mapped("detail_ids.account_id.group_id")
        existing_groups = self.posture_ids.mapped("group_id")

        groups_to_add = all_groups - existing_groups
        groups_to_remove = existing_groups - all_groups

        # Add posture line
        for group in groups_to_add:
            posture_model.create(
                {
                    "worksheet_id": self.id,
                    "group_id": group.id,
                }
            )

        # Remove posture line
        postures_to_remove = self.posture_ids.filtered(
            lambda p: p.group_id in groups_to_remove
        )
        if postures_to_remove:
            postures_to_remove.unlink()

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
