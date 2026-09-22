# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWsB66777dTeamAllocation(models.Model):
    """One row of the "Final Team Allocations" table on WS.090.2 (b66777d).

    Stores, per ``hr.employee``, the REALIZED effort (``preparation_time``
    + ``review_time``, summed across every ``general_audit_worksheet`` of
    this engagement) broken down by the same four audit phases used by
    the Audit Working Plan (``general_audit_ws_cbbbaf4.team_allocation``):
    Pre-Engagement (PE), Risk Assessment (RA), Risk Responses (RR) and
    Windup & Reporting (Reporting). The phase of a contributing worksheet
    is read from ``general_audit_worksheet.parent_type_id.category_id``
    (``general_audit_worksheet_type_category``, four fixed records --
    ``ssi_general_audit``'s ``general_audit_worksheet_type_category_
    data.xml``), NOT from a flat single number per worksheet -- see
    ``general_audit_ws_b66777d._compute_team_allocation_totals()``.

    Each realized phase column is paired with a best-effort PLANNED
    column copied from this engagement's AWP row for the same Team
    Member (``awp_pe_allocation``, etc.), so ``diff_allocation`` compares
    realized against planned totals apples-to-apples.

    (Re)populated by ``general_audit_ws_b66777d.action_populate_team_
    allocation()`` -- a full unlink-then-recreate snapshot, not a
    live-reactive summary (see that method's docstring). This IS the
    "Reload" behaviour requested for stale/late-filled historical data
    (issue #383, open question #1): clicking Populate again always
    re-reads every worksheet's current preparation_time/review_time, so
    values filled in after the fact are picked up on the next click --
    no separate Reload button/field is needed. Only available while the
    worksheet is Open (``state == 'open'``), matching the Populate
    button's ``invisible`` attrs in the form view.

    Not exposed for manual editing: every group's create/write/unlink
    permission on this model is 0 in ``security/ir.model.access.csv``,
    so only the ``sudo()``-wrapped populate logic inside
    ``general_audit_ws_b66777d._populate_team_allocation()`` can write
    to it -- same pattern as ``general_audit_ws_b66777d.detail``.
    """

    _name = "general_audit_ws_b66777d.team_allocation"
    _description = "Independent Auditor Report (b66777d) - Team Allocation"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="Worksheet",
        comodel_name="general_audit_ws_b66777d",
        required=True,
        ondelete="cascade",
        help=(
            "Independent Auditor's Report worksheet this Final Team "
            "Allocations row belongs to."
        ),
    )
    team_id = fields.Many2one(
        string="Team Member",
        comodel_name="hr.employee",
        required=True,
        readonly=True,
        ondelete="restrict",
        help=(
            "Employee this row aggregates. Always readonly -- this row "
            "is a system-populated aggregation, never manually entered "
            "(see general_audit_ws_cbbbaf4.team_allocation.team_id for "
            "the equivalent PLANNED row, which stays user-editable)."
        ),
    )
    pe_allocation = fields.Integer(
        string="Pre-Engagement Allocation",
        readonly=True,
        help=(
            "Sum of preparation_time + review_time across every "
            "general_audit_worksheet of this engagement, attributed to "
            "this Team Member, whose parent_type_id.category_id is "
            "Pre-Engagement (ssi_general_audit.worksheet_type_"
            "category_pe). Contributes to Total Allocation."
        ),
    )
    ra_allocation = fields.Integer(
        string="Risk Assessment Allocation",
        readonly=True,
        help=(
            "Sum of preparation_time + review_time across every "
            "general_audit_worksheet of this engagement, attributed to "
            "this Team Member, whose parent_type_id.category_id is "
            "Risk Assessment (ssi_general_audit.worksheet_type_"
            "category_ra). Contributes to Total Allocation."
        ),
    )
    rr_allocation = fields.Integer(
        string="Risk Responses Allocation",
        readonly=True,
        help=(
            "Sum of preparation_time + review_time across every "
            "general_audit_worksheet of this engagement, attributed to "
            "this Team Member, whose parent_type_id.category_id is "
            "Risk Responses (ssi_general_audit.worksheet_type_"
            "category_rr, code RE). Contributes to Total Allocation."
        ),
    )
    reporting_allocation = fields.Integer(
        string="Windup & Reporting Allocation",
        readonly=True,
        help=(
            "Sum of preparation_time + review_time across every "
            "general_audit_worksheet of this engagement, attributed to "
            "this Team Member, whose parent_type_id.category_id is "
            "Windup & Reporting (ssi_general_audit.worksheet_type_"
            "category_wr). Contributes to Total Allocation."
        ),
    )

    @api.depends(
        "pe_allocation",
        "ra_allocation",
        "rr_allocation",
        "reporting_allocation",
    )
    def _compute_total_allocation(self):
        """Sum this row's four realized phase allocations.

        :return: None
        """
        for record in self:
            record.total_allocation = (
                record.pe_allocation
                + record.ra_allocation
                + record.rr_allocation
                + record.reporting_allocation
            )

    total_allocation = fields.Integer(
        string="Total Allocation",
        compute="_compute_total_allocation",
        store=True,
        help=(
            "Computed total realized hours for this Team Member "
            "(Pre-Engagement + Risk Assessment + Risk Responses + "
            "Windup & Reporting Allocation)."
        ),
    )
    awp_pe_allocation = fields.Integer(
        string="AWP Pre-Engagement Allocation",
        readonly=True,
        help=(
            "Best-effort copy of this Team Member's planned "
            "pe_allocation from the same engagement's Audit Working "
            "Plan (general_audit_ws_cbbbaf4.team_allocation) -- 0 when "
            "the Audit Working Plan module is not installed, no such "
            "worksheet exists yet for this engagement, or it has no "
            "allocation row for this Team Member. See "
            "general_audit_ws_b66777d._get_awp_team_allocation_line()."
        ),
    )
    awp_ra_allocation = fields.Integer(
        string="AWP Risk Assessment Allocation",
        readonly=True,
        help=(
            "Best-effort copy of this Team Member's planned "
            "ra_allocation from the same engagement's Audit Working "
            "Plan (general_audit_ws_cbbbaf4.team_allocation) -- 0 on "
            "the same best-effort conditions as awp_pe_allocation."
        ),
    )
    awp_rr_allocation = fields.Integer(
        string="AWP Risk Responses Allocation",
        readonly=True,
        help=(
            "Best-effort copy of this Team Member's planned "
            "rr_allocation from the same engagement's Audit Working "
            "Plan (general_audit_ws_cbbbaf4.team_allocation) -- 0 on "
            "the same best-effort conditions as awp_pe_allocation."
        ),
    )
    awp_reporting_allocation = fields.Integer(
        string="AWP Windup & Reporting Allocation",
        readonly=True,
        help=(
            "Best-effort copy of this Team Member's planned "
            "reporting_allocation from the same engagement's Audit "
            "Working Plan (general_audit_ws_cbbbaf4.team_allocation) -- "
            "0 on the same best-effort conditions as awp_pe_allocation."
        ),
    )

    @api.depends(
        "awp_pe_allocation",
        "awp_ra_allocation",
        "awp_rr_allocation",
        "awp_reporting_allocation",
    )
    def _compute_awp_total_allocation(self):
        """Sum this row's four planned (AWP) phase allocations.

        :return: None
        """
        for record in self:
            record.awp_total_allocation = (
                record.awp_pe_allocation
                + record.awp_ra_allocation
                + record.awp_rr_allocation
                + record.awp_reporting_allocation
            )

    awp_total_allocation = fields.Integer(
        string="AWP Total Allocation",
        compute="_compute_awp_total_allocation",
        store=True,
        help=(
            "Computed total planned hours for this Team Member, from "
            "the same engagement's Audit Working Plan (AWP Pre-"
            "Engagement + AWP Risk Assessment + AWP Risk Responses + "
            "AWP Windup & Reporting Allocation). 0 when the AWP is not "
            "available -- see awp_pe_allocation's help."
        ),
    )

    @api.depends(
        "total_allocation",
        "awp_total_allocation",
    )
    def _compute_diff_allocation(self):
        """Compute the realized-vs-planned difference for this row.

        :return: None
        """
        for record in self:
            record.diff_allocation = (
                record.total_allocation - record.awp_total_allocation
            )

    diff_allocation = fields.Integer(
        string="Difference vs AWP",
        compute="_compute_diff_allocation",
        store=True,
        help=(
            "Total Allocation minus AWP Total Allocation. Positive "
            "means this Team Member worked more than planned; "
            "negative means less."
        ),
    )
