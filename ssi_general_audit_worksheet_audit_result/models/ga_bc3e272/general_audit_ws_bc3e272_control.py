# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbc3e272Control(models.Model):
    _name = "general_audit_ws_bc3e272.control"
    _description = "Audit Result Discussion (bc3e272) - " "Control Deficiencies"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_bc3e272",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
    state = fields.Selection(
        related="worksheet_id.state",
    )
    detail_id = fields.Many2one(
        comodel_name="general_audit_ws_d33420f.detail",
        ondelete="restrict",
    )
    condition = fields.Text(
        related="detail_id.condition",
    )
    risk = fields.Selection(
        related="detail_id.risk",
    )
    result = fields.Selection(
        selection=[
            ("resolved", "Resolved"),
            ("escalated", "Escalated"),
        ],
    )
    follow_up = fields.Text()
