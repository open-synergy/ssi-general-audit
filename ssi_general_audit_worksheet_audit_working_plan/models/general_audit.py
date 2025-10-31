# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAudit(models.Model):
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
