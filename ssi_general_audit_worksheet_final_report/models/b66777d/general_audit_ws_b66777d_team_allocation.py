# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWsB66777dTeamAllocation(models.Model):
    """One row of the "Final Team Allocations" table on WS.090.2 (b66777d).

    Stores, per ``hr.employee``, the realized effort (``preparation_time``
    + ``review_time``, summed across every ``general_audit_worksheet``
    of this engagement) against the planned effort from the Audit
    Working Plan (``general_audit_ws_cbbbaf4.team_allocation``).
    (Re)populated by ``general_audit_ws_b66777d.action_populate_team_
    allocation()`` -- a full unlink-then-recreate snapshot, not a
    live-reactive summary (see that method's docstring).

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
    total_preparation_time = fields.Integer(
        string="Total Preparation Time",
        readonly=True,
        help=(
            "Sum of preparation_time across every general_audit_"
            "worksheet of this engagement whose user_id (Responsible) "
            "maps to this Team Member's linked user, "
            "res.users.employee_id. Contributes to Total Allocation."
        ),
    )
    total_review_time = fields.Integer(
        string="Total Review Time",
        readonly=True,
        help=(
            "Sum of review_time across every general_audit_worksheet "
            "of this engagement whose reviewer_id maps to this Team "
            "Member's linked user, res.users.employee_id. Contributes "
            "to Total Allocation."
        ),
    )

    @api.depends(
        "total_preparation_time",
        "total_review_time",
    )
    def _compute_total_allocation(self):
        """Sum this row's realized preparation and review time.

        :return: None
        """
        for record in self:
            record.total_allocation = (
                record.total_preparation_time + record.total_review_time
            )

    total_allocation = fields.Integer(
        string="Total Allocation",
        compute="_compute_total_allocation",
        store=True,
        help=(
            "Computed total realized hours for this Team Member "
            "(Total Preparation Time + Total Review Time)."
        ),
    )
    awp_total_allocation = fields.Integer(
        string="AWP Total Allocation",
        readonly=True,
        help=(
            "Best-effort copy of this Team Member's planned "
            "total_allocation from the same engagement's Audit "
            "Working Plan (general_audit_ws_cbbbaf4.team_allocation) "
            "-- 0 when the Audit Working Plan module is not installed, "
            "no such worksheet exists yet for this engagement, or it "
            "has no allocation row for this Team Member. See "
            "general_audit_ws_b66777d._get_awp_total_allocation()."
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
