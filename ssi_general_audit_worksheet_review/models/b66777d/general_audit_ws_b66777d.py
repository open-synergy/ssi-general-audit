# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSb66777d(models.Model):
    _inherit = "general_audit_ws_b66777d"

    @api.depends("general_audit_id")
    def _compute_draft_opinion_id(self):
        """Find this engagement's Draft Audit Opinion (fc75636) worksheet.

        Non-stored on purpose (no ``store=True``): unlike the
        ``store=True`` + manual "Reload" button pattern used by
        ``general_audit_ws_fc75636.audit_final_memorandum_id`` below,
        this field must resolve correctly even when the matching
        fc75636 record is created *after* this worksheet already
        exists -- Odoo's ORM cannot auto-invalidate a stored compute
        just because an unrelated model's record was created, so
        storing it would require the same kind of manual reload
        trigger. Recomputing on every access guarantees it is always
        current with no user action needed.

        Defined HERE, on this module's extension of
        ``general_audit_ws_b66777d`` (owned by
        ``ssi_general_audit_worksheet_final_report``), rather than
        directly on that model -- see the comment above ``opinion``
        in that module's ``general_audit_ws_b66777d.py`` for why: a
        static Many2one there with ``comodel_name=
        "general_audit_ws_fc75636"`` would have its comodel
        resolution permanently pinned to Odoo's internal "_unknown"
        placeholder whenever both modules are updated together in one
        process, because that module's fields get set up before this
        one's model is even registered. Declaring it here instead,
        where ``general_audit_ws_fc75636`` is defined in the SAME
        module, guarantees both models are already registered by the
        time this field's setup runs, in every loading order.

        :return: None
        """
        for record in self:
            result = False
            draft = (
                self.env["general_audit_ws_fc75636"]
                .sudo()
                .search(
                    [
                        ("general_audit_id", "=", record.general_audit_id.id),
                        ("state", "in", ["open", "done"]),
                    ],
                    limit=1,
                    order="id desc",
                )
            )
            if draft:
                result = draft.id
            record.draft_opinion_id = result

    draft_opinion_id = fields.Many2one(
        string="Draft Audit Opinion",
        comodel_name="general_audit_ws_fc75636",
        compute="_compute_draft_opinion_id",
        compute_sudo=True,
        help=(
            "The Draft Audit Opinion (fc75636) worksheet of this same "
            "engagement, found by general_audit_id. Not stored -- "
            "always recomputed live, so it resolves correctly even if "
            "the fc75636 record is created after this worksheet."
        ),
    )
