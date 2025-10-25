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
        help=(
            "The Audit Working Plan (cbbbaf4) this competency analysis belongs to. "
            "Deleting the worksheet will remove its competency lines."
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
            "Employee whose competency is being analyzed for this worksheet. "
            "Editable while the worksheet is in Open state."
        ),
    )
    competency_upgrade_ids = fields.Many2many(
        string="Competency Upgrade Needed",
        comodel_name="general_audit_competency_upgrade",
        relation="rel_general_audit_ws_cbbbaf4_team_competency_upgrade",
        column1="team_competency_id",
        column2="competency_upgrade_id",
        readonly=True,
        help=(
            "Recommended competency upgrades needed for the team member. "
            "Populated based on gaps between required competencies and current "
            "competency analysis (from PE.110.3)."
        ),
    )
    upgrade_attachment_ids = fields.Many2many(
        string="Attachments",
        comodel_name="ir.attachment",
        relation="rel_general_audit_ws_cbbbaf4_2_attachment",
        column1="ga_cbbbaf4_id",
        column2="attachment_id",
        domain="[('res_model', '=', 'general_audit_ws_cbbbaf4'),"
        "('res_id', '=', worksheet_id)]",
        help=(
            "Supporting documents for the competency upgrade plan (e.g., training "
            "materials, certificates). Only attachments of this worksheet are shown."
        ),
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help=(
            "Status of the parent worksheet. The state controls whether fields "
            "on this line are editable."
        ),
    )
