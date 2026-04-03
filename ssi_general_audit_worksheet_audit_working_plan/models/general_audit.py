# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAudit(models.Model):
    """Extension of the General Audit model for Audit Working Plan data.

    Adds aggregated team-allocation data to the General Audit engagement record:
    * ``detail_team_allocation_ids`` — all team allocation lines from the
      Audit Working Plan worksheets (WS-CBBBAF4) within this engagement,
      providing a consolidated view of staffing across phase worksheets.
    * ``team_allocation_user_ids`` — the Odoo users linked to the allocated
      employees, used for access control and notification purposes.
    """

    _name = "general_audit"
    _description = "General Audit"
    _inherit = [
        "general_audit",
    ]

    detail_team_allocation_ids = fields.One2many(
        string="Detail Team Allocations",
        comodel_name="general_audit_ws_cbbbaf4.team_allocation",
        inverse_name="general_audit_id",
        help=(
            "Team allocation details for this General Audit engagement. "
            "Managed through the Audit Working Plan (cbbbaf4) worksheets."
        ),
    )
    team_allocation_user_ids = fields.Many2many(
        string="Teams",
        comodel_name="res.users",
        compute="_compute_team_allocation_user_ids",
        help=(
            "Users linked to employees assigned as team members "
            "in the team allocations for this General Audit engagement."
        ),
        store=True,
        relation="general_audit_team_allocation_user_rel",
        column1="general_audit_id",
        column2="user_id",
    )

    @api.depends(
        "detail_team_allocation_ids",
        "detail_team_allocation_ids.team_id",
        "detail_team_allocation_ids.team_id.user_id",
    )
    def _compute_team_allocation_user_ids(self):
        for record in self:
            user_ids = record.detail_team_allocation_ids.mapped("team_id.user_id.id")
            record.team_allocation_user_ids = [(6, 0, user_ids)]
