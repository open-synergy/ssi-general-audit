# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSab19fd4(models.Model):
    """Worksheet WR.110.3 — Audit Result Formulation.

    Consolidates all findings from WR.110.1 (Findings That Influence Opinion)
    and control deficiencies from WR.110.2 (Control Deficiencies) onto a
    single engagement-partner view to support the formulation of the final
    audit opinion.

    The ``link_1_ids`` field aggregates the detail lines of all WR.110.1
    worksheets within the same general audit, and ``link_2_ids`` aggregates
    the detail lines of all WR.110.2 worksheets.  Both fields are recomputed
    via ``action_recompute``, which should be called after upstream worksheets
    have been confirmed.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 700/SA 700 (Forming an Opinion);
    ISA 450/SA 450 (Evaluation of Misstatements);
    ISA 265/SA 265 (Communicating Deficiencies).
    """

    _name = "general_audit_ws_ab19fd4"
    _description = "Audit Result Formulation (ab19fd4)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_audit_result." "worksheet_type_ab19fd4"

    # Findings That Influence Opinion
    # LINK - 1 a0319a2 (WR. 110.1) - source worksheet header reference
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_1_id(self):
        """Derive the source 'Findings That Influence Opinion' worksheet.

        :return: nothing; assigns ``link_1_id`` to the first
            ``general_audit_ws_a0319a2`` record belonging to the same
            general audit, or an empty recordset when none is found.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a0319a2"]
            if record.general_audit_id:
                result = obj.search(
                    [("general_audit_id", "=", record.general_audit_id.id)],
                    limit=1,
                )
            record.link_1_id = result

    link_1_id = fields.Many2one(
        string="# WR.110.1",
        comodel_name="general_audit_ws_a0319a2",
        compute_sudo=True,
        compute="_compute_link_1_id",
        store=True,
        help=(
            "Source 'Findings That Influence Opinion' worksheet whose detail "
            "lines are aggregated into link_1_ids."
        ),
    )

    # Findings That Influence Opinion
    # LINK - 1 a0319a2 (WR. 110.1)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_1_ids(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a0319a2"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_1_ids = obj.search(criteria)
            if link_1_ids:
                result = link_1_ids.detail_ids.ids
            record.link_1_ids = result

    link_1_ids = fields.Many2many(
        string="WR. 110.1",
        comodel_name="general_audit_ws_a0319a2.detail",
        compute_sudo=True,
        compute="_compute_link_1_ids",
        store=True,
        help=(
            "Auto-populated link to 'Findings That Influence Opinion'. "
            "Computed from worksheet a0319a2 belonging to the same general audit."
        ),
    )

    # Control Deficiencies
    # LINK - 2 d33420f (WR. 110.2) - source worksheet header reference
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_2_id(self):
        """Derive the source 'Control Deficiencies' worksheet.

        :return: nothing; assigns ``link_2_id`` to the first
            ``general_audit_ws_d33420f`` record belonging to the same
            general audit, or an empty recordset when none is found.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d33420f"]
            if record.general_audit_id:
                result = obj.search(
                    [("general_audit_id", "=", record.general_audit_id.id)],
                    limit=1,
                )
            record.link_2_id = result

    link_2_id = fields.Many2one(
        string="# WR.110.2",
        comodel_name="general_audit_ws_d33420f",
        compute_sudo=True,
        compute="_compute_link_2_id",
        store=True,
        help=(
            "Source 'Control Deficiencies' worksheet whose detail lines are "
            "aggregated into link_2_ids."
        ),
    )

    # Control Deficiencies
    # LINK - 2 d33420f (WR. 110.2)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_2_ids(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d33420f"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_2_ids = obj.search(criteria)
            if link_2_ids:
                result = link_2_ids.detail_ids.ids
            record.link_2_ids = result

    link_2_ids = fields.Many2many(
        string="WR. 110.2",
        comodel_name="general_audit_ws_d33420f.detail",
        compute_sudo=True,
        compute="_compute_link_2_ids",
        store=True,
        help=(
            "Auto-populated link to 'Control Deficiencies'. "
            "Computed from worksheet d33420f belonging to the same general audit."
        ),
    )

    def action_recompute(self):
        """Refresh both source worksheet references and their detail links.

        :return: ``None``.
        """
        for record in self:
            record._compute_link_1_id()
            record._compute_link_1_ids()
            record._compute_link_2_id()
            record._compute_link_2_ids()
