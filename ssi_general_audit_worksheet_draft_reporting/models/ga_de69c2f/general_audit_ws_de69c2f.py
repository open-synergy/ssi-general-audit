# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSde69c2f(models.Model):
    """Worksheet — Final Discussion (de69c2f).

    A checklist-driven worksheet guiding the engagement team through the
    final pre-issuance quality review before the audit report is signed.  Each
    checklist item (``checklist_ids``) represents a required step or check that
    must be completed and documented before the opinion can be issued.

    Typical items include: confirming all open points are resolved, verifying
    the completeness of the audit file, reviewing subsequent events through
    the report date, confirming management representations are obtained, and
    obtaining partner approval sign-off.

    Also cross-references the other Windup & Reporting KKAs of the same
    engagement -- Audit Result (``audit_result_id``), Management Letter
    (``management_letter_id``), and Management Representation
    (``management_representation_id``) -- in a single "Links" tab. Each
    reference is filled in automatically (compute+store) whenever the
    engagement's siblings change state, and can also be refreshed on
    demand with the single ``action_reload_links`` button, following the
    pattern established by ``general_audit_ws_fbbe0f8``.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 560/SA 560 (Subsequent Events);
    ISA 700/SA 700 (Forming an Opinion);
    ISA 220/SA 220 (Quality Control for an Audit).
    """

    _name = "general_audit_ws_de69c2f"
    _description = "Final Discussion (de69c2f)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_draft_reporting." "worksheet_type_de69c2f"
    )
    _checklist_model_name = "general_audit_ws_de69c2f.checklist"
    _item_model_name = "general_audit_ws_de69c2f.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_de69c2f.checklist",
        help="Checklist lines for this worksheet.",
    )

    # Audit Result
    # LINK - 1 ff42fdc (WR.170.1)
    @api.depends(
        "general_audit_id",
    )
    def _compute_audit_result_id(self):
        """Compute the linked Audit Result worksheet.

        :return: None; sets ``audit_result_id`` on every record in
            ``self``.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ff42fdc"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            audit_result_id = obj.search(criteria)
            if audit_result_id:
                result = audit_result_id.id
            record.audit_result_id = result

    audit_result_id = fields.Many2one(
        string="WR.170.1",
        comodel_name="general_audit_ws_ff42fdc",
        compute_sudo=True,
        compute="_compute_audit_result_id",
        store=True,
        help=(
            "Link to the Audit Result (ff42fdc) worksheet of the same "
            "General Audit. Automatically computed and stored."
        ),
    )
    audit_result_state = fields.Selection(
        string="State (WR.170.1)",
        related="audit_result_id.state",
        help=(
            "Workflow state of the linked Audit Result worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    audit_result_conclusion = fields.Text(
        string="Conclusion (WR.170.1)",
        related="audit_result_id.conclusion",
        help=(
            "Conclusion on the linked Audit Result worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Management Letter
    # LINK - 2 ae598e6 (WR.170.2)
    @api.depends(
        "general_audit_id",
    )
    def _compute_management_letter_id(self):
        """Compute the linked Management Letter worksheet.

        :return: None; sets ``management_letter_id`` on every record in
            ``self``.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ae598e6"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            management_letter_id = obj.search(criteria)
            if management_letter_id:
                result = management_letter_id.id
            record.management_letter_id = result

    management_letter_id = fields.Many2one(
        string="WR.170.2",
        comodel_name="general_audit_ws_ae598e6",
        compute_sudo=True,
        compute="_compute_management_letter_id",
        store=True,
        help=(
            "Link to the Management Letter (ae598e6) worksheet of the "
            "same General Audit. Automatically computed and stored."
        ),
    )
    management_letter_state = fields.Selection(
        string="State (WR.170.2)",
        related="management_letter_id.state",
        help=(
            "Workflow state of the linked Management Letter worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    management_letter_conclusion = fields.Text(
        string="Conclusion (WR.170.2)",
        related="management_letter_id.conclusion",
        help=(
            "Conclusion on the linked Management Letter worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Management Representation
    # LINK - 3 bbbdfe7 (WR.170.3)
    @api.depends(
        "general_audit_id",
    )
    def _compute_management_representation_id(self):
        """Compute the linked Management Representation worksheet.

        :return: None; sets ``management_representation_id`` on every
            record in ``self``.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_bbbdfe7"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            management_representation_id = obj.search(criteria)
            if management_representation_id:
                result = management_representation_id.id
            record.management_representation_id = result

    management_representation_id = fields.Many2one(
        string="WR.170.3",
        comodel_name="general_audit_ws_bbbdfe7",
        compute_sudo=True,
        compute="_compute_management_representation_id",
        store=True,
        help=(
            "Link to the Management Representation (bbbdfe7) worksheet "
            "of the same General Audit. Automatically computed and "
            "stored."
        ),
    )
    management_representation_state = fields.Selection(
        string="State (WR.170.3)",
        related="management_representation_id.state",
        help=(
            "Workflow state of the linked Management Representation "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    management_representation_conclusion = fields.Text(
        string="Conclusion (WR.170.3)",
        related="management_representation_id.conclusion",
        help=(
            "Conclusion on the linked Management Representation "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )

    def action_reload_links(self):
        """Refresh every linked KKA reference on the Links tab.

        :return: None; calls ``_reload_links`` on every record in
            ``self``, run with ``sudo()`` so users without direct write
            access on the linked worksheets can still trigger the
            reload from the button.
        """
        for record in self.sudo():
            record._reload_links()

    def _reload_links(self):
        """Recompute all three Links tab references.

        :return: None; re-runs ``_compute_audit_result_id``,
            ``_compute_management_letter_id``, and
            ``_compute_management_representation_id`` on this record.
        """
        self.ensure_one()
        self._compute_audit_result_id()
        self._compute_management_letter_id()
        self._compute_management_representation_id()
