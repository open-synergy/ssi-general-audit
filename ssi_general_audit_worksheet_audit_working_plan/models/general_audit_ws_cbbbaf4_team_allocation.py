# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSCBBBAF4TeamAllocation(models.Model):
    _name = "general_audit_ws_cbbbaf4.team_allocation"
    _description = "Audit Working Plan (cbbbaf4) - Team Allocation"
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
        comodel_name="hr.employee",
        required=True,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
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
    )
    state = fields.Selection(
        related="worksheet_id.state",
    )
