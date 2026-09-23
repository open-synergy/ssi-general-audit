# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models


class GeneralAuditWSa8c54f3(models.Model):
    """Extends ``general_audit_ws_a8c54f3`` with ``link_42_id``..``link_47_id``.

    Defined in THIS module (``ssi_general_audit_worksheet_review``, the
    owner of the six KKA models targeted below) rather than in
    ``ssi_general_audit_worksheet_final_report`` itself, because that
    module cannot ``depend`` on this one without creating a circular
    dependency: this module already ``depends`` on
    ``ssi_general_audit_worksheet_final_report`` (see ``models/b66777d/``
    for the same pattern applied to ``general_audit_ws_b66777d``).
    """

    _inherit = "general_audit_ws_a8c54f3"

    # Financial Statement Disclosure Review
    # LINK - 42 be62e79
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_42_id(self):
        """Populate ``link_42_id`` from open/done Financial Statement
        Disclosure Review worksheets.

        Searches ``general_audit_ws_be62e79`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_be62e79"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_42_id = obj.search(criteria, limit=1)
            if link_42_id:
                result = link_42_id.id
            record.link_42_id = result

    link_42_id = fields.Many2one(
        string="Financial Statement Disclosure Review",
        comodel_name="general_audit_ws_be62e79",
        compute_sudo=True,
        compute="_compute_link_42_id",
        store=True,
        help=(
            "Link to worksheet (Financial Statement Disclosure Review) for "
            "this General Audit. Automatically computed and stored."
        ),
    )
    link_42_state = fields.Selection(
        string="State",
        related="link_42_id.state",
        help=(
            "Workflow state of the linked Financial Statement Disclosure "
            "Review worksheet. Read-only and follows the linked record."
        ),
    )
    link_42_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_42_id.conclusion_id",
        help=(
            "Conclusion from the Financial Statement Disclosure Review "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_42_conclusion = fields.Text(
        string="Conclusion",
        related="link_42_id.conclusion",
        help=(
            "Conclusion on the Financial Statement Disclosure Review "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )

    # Financial Statement Disclosure
    # LINK - 43 a025441
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_43_id(self):
        """Populate ``link_43_id`` from open/done Financial Statement
        Disclosure worksheets.

        Searches ``general_audit_ws_a025441`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a025441"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_43_id = obj.search(criteria, limit=1)
            if link_43_id:
                result = link_43_id.id
            record.link_43_id = result

    link_43_id = fields.Many2one(
        string="Financial Statement Disclosure",
        comodel_name="general_audit_ws_a025441",
        compute_sudo=True,
        compute="_compute_link_43_id",
        store=True,
        help=(
            "Link to worksheet (Financial Statement Disclosure) for this "
            "General Audit. Automatically computed and stored."
        ),
    )
    link_43_state = fields.Selection(
        string="State",
        related="link_43_id.state",
        help=(
            "Workflow state of the linked Financial Statement Disclosure "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_43_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_43_id.conclusion_id",
        help=(
            "Conclusion from the Financial Statement Disclosure worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_43_conclusion = fields.Text(
        string="Conclusion",
        related="link_43_id.conclusion",
        help=(
            "Conclusion on the Financial Statement Disclosure worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Audit Quality
    # LINK - 44 bcc0d76
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_44_id(self):
        """Populate ``link_44_id`` from open/done Audit Quality worksheets.

        Searches ``general_audit_ws_bcc0d76`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_bcc0d76"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_44_id = obj.search(criteria, limit=1)
            if link_44_id:
                result = link_44_id.id
            record.link_44_id = result

    link_44_id = fields.Many2one(
        string="Audit Quality",
        comodel_name="general_audit_ws_bcc0d76",
        compute_sudo=True,
        compute="_compute_link_44_id",
        store=True,
        help=(
            "Link to worksheet (Audit Quality) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_44_state = fields.Selection(
        string="State",
        related="link_44_id.state",
        help=(
            "Workflow state of the linked Audit Quality worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_44_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_44_id.conclusion_id",
        help=(
            "Conclusion from the Audit Quality worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )
    link_44_conclusion = fields.Text(
        string="Conclusion",
        related="link_44_id.conclusion",
        help=(
            "Conclusion on the Audit Quality worksheet. Read-only, mirrors "
            "the linked record."
        ),
    )

    # Audit Evidence Evaluation
    # LINK - 45 dae9f3c
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_45_id(self):
        """Populate ``link_45_id`` from open/done Audit Evidence Evaluation
        worksheets.

        Searches ``general_audit_ws_dae9f3c`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_dae9f3c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_45_id = obj.search(criteria, limit=1)
            if link_45_id:
                result = link_45_id.id
            record.link_45_id = result

    link_45_id = fields.Many2one(
        string="Audit Evidence Evaluation",
        comodel_name="general_audit_ws_dae9f3c",
        compute_sudo=True,
        compute="_compute_link_45_id",
        store=True,
        help=(
            "Link to worksheet (Audit Evidence Evaluation) for this "
            "General Audit. Automatically computed and stored."
        ),
    )
    link_45_state = fields.Selection(
        string="State",
        related="link_45_id.state",
        help=(
            "Workflow state of the linked Audit Evidence Evaluation "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_45_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_45_id.conclusion_id",
        help=(
            "Conclusion from the Audit Evidence Evaluation worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_45_conclusion = fields.Text(
        string="Conclusion",
        related="link_45_id.conclusion",
        help=(
            "Conclusion on the Audit Evidence Evaluation worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Audit Evidence Evaluation Detail
    # LINK - 46 cae598e
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_46_id(self):
        """Populate ``link_46_id`` from open/done Audit Evidence Evaluation
        Detail worksheets.

        Searches ``general_audit_ws_cae598e`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_cae598e"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_46_id = obj.search(criteria, limit=1)
            if link_46_id:
                result = link_46_id.id
            record.link_46_id = result

    link_46_id = fields.Many2one(
        string="Audit Evidence Evaluation Detail",
        comodel_name="general_audit_ws_cae598e",
        compute_sudo=True,
        compute="_compute_link_46_id",
        store=True,
        help=(
            "Link to worksheet (Audit Evidence Evaluation Detail) for this "
            "General Audit. Automatically computed and stored."
        ),
    )
    link_46_state = fields.Selection(
        string="State",
        related="link_46_id.state",
        help=(
            "Workflow state of the linked Audit Evidence Evaluation Detail "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_46_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_46_id.conclusion_id",
        help=(
            "Conclusion from the Audit Evidence Evaluation Detail "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_46_conclusion = fields.Text(
        string="Conclusion",
        related="link_46_id.conclusion",
        help=(
            "Conclusion on the Audit Evidence Evaluation Detail worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Proposed Audit Opinion
    # LINK - 47 fc75636
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_47_id(self):
        """Populate ``link_47_id`` from open/done Proposed Audit Opinion
        worksheets.

        Searches ``general_audit_ws_fc75636`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_fc75636"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_47_id = obj.search(criteria, limit=1)
            if link_47_id:
                result = link_47_id.id
            record.link_47_id = result

    link_47_id = fields.Many2one(
        string="Proposed Audit Opinion",
        comodel_name="general_audit_ws_fc75636",
        compute_sudo=True,
        compute="_compute_link_47_id",
        store=True,
        help=(
            "Link to worksheet (Proposed Audit Opinion) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_47_state = fields.Selection(
        string="State",
        related="link_47_id.state",
        help=(
            "Workflow state of the linked Proposed Audit Opinion "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_47_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_47_id.conclusion_id",
        help=(
            "Conclusion from the Proposed Audit Opinion worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_47_conclusion = fields.Text(
        string="Conclusion",
        related="link_47_id.conclusion",
        help=(
            "Conclusion on the Proposed Audit Opinion worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    def _reload_links(self):
        """Also recompute ``link_42_id``..``link_47_id`` on ``self``.

        Extends the base ``_reload_links`` (which recomputes
        ``link_1_id``..``link_41_id`` and ``link_48_id``) with the six KKA
        links owned by this module, so ``action_reload_links`` on the base
        model refreshes all 48 in one call regardless of which module
        defines each one.

        :return: ``None``.
        """
        super()._reload_links()
        self._compute_link_42_id()
        self._compute_link_43_id()
        self._compute_link_44_id()
        self._compute_link_45_id()
        self._compute_link_46_id()
        self._compute_link_47_id()

    def _get_custom_field_labels(self):
        """Merge in the KKA labels for ``link_42_id``..``link_47_id``.

        :return: dict of ``{field_name: label}``, base mapping from
            ``super()`` merged with the six labels owned by this module.
        """
        result = super()._get_custom_field_labels()
        result.update(
            {
                "link_42_id": _("Financial Statement Disclosure Review"),
                "link_43_id": _("Financial Statement Disclosure"),
                "link_44_id": _("Audit Quality"),
                "link_45_id": _("Audit Evidence Evaluation"),
                "link_46_id": _("Audit Evidence Evaluation Detail"),
                "link_47_id": _("Proposed Audit Opinion"),
            }
        )
        return result
