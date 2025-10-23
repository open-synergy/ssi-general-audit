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
        help=(
            "Parent discussion worksheet for control deficiencies. "
            "Used to group control-related discussion items."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help="Display order of this line within the discussion worksheet.",
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help="Current state of the parent worksheet (related).",
    )
    detail_id = fields.Many2one(
        comodel_name="general_audit_ws_d33420f.detail",
        ondelete="restrict",
        help=(
            "Linked control deficiency detail record (from worksheet d33420f) "
            "being discussed or followed up."
        ),
    )
    condition = fields.Text(
        related="detail_id.condition",
        help="Condition text pulled from the linked control deficiency detail.",
    )
    risk = fields.Selection(
        related="detail_id.risk",
        help="Risk severity pulled from the linked control deficiency detail.",
    )
    result = fields.Selection(
        selection=[
            ("resolved", "Resolved"),
            ("escalated", "Escalated"),
        ],
        help=(
            "Outcome of the discussion/follow-up for this control deficiency: "
            "resolved or escalated."
        ),
    )
    follow_up = fields.Text(
        help=(
            "Planned or completed follow-up actions to address the control "
            "deficiency."
        ),
    )
