# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


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

    Total, AWP Total and Difference are deliberately NOT columns on
    this row: they are not meaningful per employee, only in aggregate
    across the whole engagement -- matching how the Audit Working
    Plan's own KKA shows its "Total"/"Difference" figures once for the
    whole worksheet, not once per Team Member. Those fifteen fields
    (``total_pe_allocation`` etc., ``awp_total_pe_allocation`` etc.,
    ``diff_pe_allocation`` etc.) live on the parent
    ``general_audit_ws_b66777d`` worksheet instead -- see that model's
    ``_compute_team_allocation_total()``,
    ``_populate_awp_total_allocation()`` and
    ``_compute_team_allocation_diff()``.

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
            "category_pe). Contributes to the parent worksheet's "
            "total_pe_allocation."
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
            "category_ra). Contributes to the parent worksheet's "
            "total_ra_allocation."
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
            "category_rr, code RE). Contributes to the parent "
            "worksheet's total_rr_allocation."
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
            "category_wr). Contributes to the parent worksheet's "
            "total_reporting_allocation."
        ),
    )
