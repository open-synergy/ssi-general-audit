# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAudit(models.Model):
    _inherit = "general_audit"

    # The opinion and its date now come from the Independent Auditor
    # Report instead of being typed in, and stay empty until that
    # report has them. ``states={}`` drops the "editable while open"
    # rule of the base field, so both fields are read-only in every
    # state.
    opinion_id = fields.Many2one(
        readonly=True,
        states={},
        help=(
            "Audit opinion of the engagement. Filled automatically "
            "from the Independent Auditor Report and empty until that "
            "report has an opinion; read-only."
        ),
    )
    opinion_date = fields.Date(
        readonly=True,
        states={},
        help=(
            "Date of the audit opinion. Filled automatically from the "
            "Independent Auditor Report and empty until that report has "
            "one; read-only."
        ),
    )

    def _sync_opinion_from_audit_report(self):
        """Make the opinion of the audit mirror its Independent Auditor Report.

        The source is the newest Independent Auditor Report
        (``general_audit_ws_b66777d``) of the engagement that is open
        or done. ``opinion_id`` and ``opinion_date`` take its Audit
        Opinion and Opinion Date, and are emptied when the engagement
        has no such report or the report has no opinion yet, so the
        audit never keeps an opinion that no report backs. A field is
        only written when its value actually changes. The write uses
        ``sudo()``, because worksheet users are not required to hold
        write access on ``general_audit``.

        :return: None
        """
        report_model = self.env["general_audit_ws_b66777d"].sudo()
        for record in self.sudo():
            report = report_model.search(
                [
                    ("general_audit_id", "=", record.id),
                    ("state", "in", ["open", "done"]),
                ],
                limit=1,
                order="id desc",
            )
            vals = {}
            opinion = report.audit_opinion_id
            opinion_date = report.audit_opinion_date or False
            if record.opinion_id != opinion:
                vals["opinion_id"] = opinion.id
            if record.opinion_date != opinion_date:
                vals["opinion_date"] = opinion_date
            if vals:
                record.write(vals)
