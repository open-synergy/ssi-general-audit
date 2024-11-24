# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSCBBBAF4TeamCompetency(models.Model):
    _name = "general_audit_ws_cbbbaf4.team_competency"
    _description = "Audit Working Plan (cbbbaf4) - Team Competency Analysis"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_cbbbaf4",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    team_id = fields.Many2one(
        string="Team Member",
        comodel_name="res.partner",
        required=True,
        domain=[
            ("is_company", "=", False),
        ],
    )
    comptency_upgrade_ids = fields.Many2many(
        string="Competency Upgrade Needed",
        comodel_name="general_audit_competency_upgrade",
        relation="rel_general_audit_ws_cbbbaf4_team_competency_upgrade",
        column1="team_competency_id",
        column2="competency_upgrade_id",
    )
