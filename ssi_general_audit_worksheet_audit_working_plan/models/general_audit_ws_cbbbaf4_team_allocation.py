# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSCBBBAF4TeamAllocation(models.Model):
    _name = "general_audit_ws_cbbbaf4.team_allocation"
    _description = "Audit Working Plan (cbbbaf4) - Team Allocation"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_cbbbaf4",
        required=True,
        ondelete="cascade",
        help=(
            "The Audit Working Plan (cbbbaf4) this allocation line belongs to. "
            "Deleting the worksheet will remove its allocation lines."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help=("Line ordering for this team member. Lower values are shown first."),
    )
    team_id = fields.Many2one(
        string="Team Member",
        comodel_name="hr.employee",
        required=True,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Employee assigned to the engagement for this worksheet. "
            "Editable while the worksheet is in Open state."
        ),
    )
    role_id = fields.Many2one(
        string="Role",
        comodel_name="team_role",
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Engagement role of the team member (e.g., Partner, Manager, Senior). "
            "Editable while the worksheet is in Open state."
        ),
    )
    pe_allocation = fields.Float(
        string="Pre-Engagement Allocation",
        required=False,
        default=0.0,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Hours allocated to Pre-Engagement activities for this team member. "
            "Contributes to Total Allocation."
        ),
    )
    ra_allocation = fields.Float(
        string="Risk Assesment Allocation",
        required=False,
        default=0.0,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Hours allocated to Risk Assessment activities for this team member. "
            "Contributes to Total Allocation."
        ),
    )
    rr_allocation = fields.Float(
        string="Risk Response Allocation",
        required=False,
        default=0.0,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Hours allocated to Risk Response activities for this team member. "
            "Contributes to Total Allocation."
        ),
    )
    reporting_allocation = fields.Float(
        string="Reporting Allocation",
        required=False,
        default=0.0,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Hours allocated to Reporting activities for this team member. "
            "Contributes to Total Allocation."
        ),
    )

    @api.depends(
        "pe_allocation",
        "ra_allocation",
        "rr_allocation",
        "reporting_allocation",
    )
    def _compute_total_allocation(self):
        for record in self:
            record.total_allocation = (
                record.pe_allocation
                + record.ra_allocation
                + record.rr_allocation
                + record.reporting_allocation
            )

    total_allocation = fields.Float(
        string="Total Allocation",
        compute="_compute_total_allocation",
        store=True,
        compute_sudo=True,
        help=(
            "Computed total hours allocated to this team member across all phases "
            "(Pre-Engagement + Risk Assessment + Risk Response + Reporting)."
        ),
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help=(
            "Status of the parent worksheet. The state controls whether fields "
            "on this line are editable."
        ),
    )
