# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSfc75636(models.Model):
    """
    WS: Independent Auditor's Report Review Checklist (fc75636) — ISA 700 / SA 700.

    A structured Yes / No / N-A checklist for reviewing the **draft
    independent auditor's report** before it is issued, ensuring compliance
    with the applicable ISA / SA reporting standards.

    Checklist item types (``checklist_type``):

    * ``unmodified``       — Requirements for an unmodified (clean) opinion
      under ISA 700 / SA 700.
    * ``modified``         — Additional requirements when a modified opinion
      (qualified, adverse, disclaimer) is issued per ISA 705 / SA 705.
    * ``emphasis_other``   — Requirements for Emphasis of Matter and Other
      Matter paragraphs per ISA 706 / SA 706.

    Items are further grouped by ``category_id``
    (``general_audit_ws_fc75636.category``) to organise the review by
    report section or paragraph type.

    Also cross-references the Audit Final Memorandum (``a8c54f3``) KKA of
    the same engagement in a "Links" tab: ``audit_final_memorandum_id``
    (compute+store) and the related ``proposed_audit_opinion_id`` it
    mirrors. Filled in automatically whenever the engagement's sibling
    changes state, and can also be refreshed on demand with the
    ``action_reload_links`` button, following the pattern established by
    ``general_audit_ws_de69c2f``.
    """

    _name = "general_audit_ws_fc75636"
    _description = "Independen Auditor Report Review(fc75636)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_review." "worksheet_type_fc75636"
    _checklist_model_name = "general_audit_ws_fc75636.checklist"
    _item_model_name = "general_audit_ws_fc75636.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_fc75636.checklist",
        help="Checklist lines for this worksheet.",
    )

    # Audit Final Memorandum
    @api.depends(
        "general_audit_id",
    )
    def _compute_audit_final_memorandum_id(self):
        """Compute the linked Audit Final Memorandum worksheet.

        :return: None; sets ``audit_final_memorandum_id`` on every
            record in ``self``.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a8c54f3"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            audit_final_memorandum_id = obj.search(criteria)
            if audit_final_memorandum_id:
                result = audit_final_memorandum_id.id
            record.audit_final_memorandum_id = result

    audit_final_memorandum_id = fields.Many2one(
        string="Audit Final Memorandum",
        comodel_name="general_audit_ws_a8c54f3",
        compute_sudo=True,
        compute="_compute_audit_final_memorandum_id",
        store=True,
        help=(
            "Link to the Audit Final Memorandum (a8c54f3) worksheet of "
            "the same General Audit. Automatically computed and stored."
        ),
    )
    proposed_audit_opinion_id = fields.Many2one(
        string="Proposed Audit Opinion",
        related="audit_final_memorandum_id.proposed_audit_opinion_id",
        store=True,
        help=(
            "Proposed audit opinion, mirrored from the linked Audit "
            "Final Memorandum worksheet. Read-only."
        ),
    )

    def action_reload_links(self):
        """Refresh the Audit Final Memorandum reference on the Links tab.

        :return: None; calls ``_reload_links`` on every record in
            ``self``, run with ``sudo()`` so users without direct write
            access on the linked worksheet can still trigger the reload
            from the button.
        """
        for record in self.sudo():
            record._reload_links()

    def _reload_links(self):
        """Recompute the Links tab reference.

        :return: None; re-runs ``_compute_audit_final_memorandum_id`` on
            this record.
        """
        self.ensure_one()
        self._compute_audit_final_memorandum_id()
