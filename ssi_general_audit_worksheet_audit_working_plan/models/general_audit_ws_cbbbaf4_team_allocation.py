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
        comodel_name="res.partner",
        required=True,
        domain=[
            ("is_company", "=", False),
        ],
    )
    role = fields.Char(
        string="Role",
        required=True,
    )
    ra_allocation = fields.Float(
        string="Risk Assesment Allocation",
        required=True,
        default=0.0,
    )
    rr_allocation = fields.Float(
        string="Risk Response Allocation",
        required=True,
        default=0.0,
    )
    reporting_allocation = fields.Float(
        string="Reporting Allocation",
        required=True,
        default=0.0,
    )
