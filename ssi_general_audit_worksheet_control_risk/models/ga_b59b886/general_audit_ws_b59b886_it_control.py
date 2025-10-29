# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb59b886ItControl(models.Model):
    _name = "general_audit_ws_b59b886.it_control"
    _description = "Control Risk - Entity Level (b59b886) - " "IT Control"
    _order = "detail_id, category_id, control_id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_b59b886",
        required=True,
        ondelete="cascade",
        help="Parent worksheet to which this control deficiency line belongs.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help="Sequence used to order the lines in the report.",
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help="State of the parent worksheet.",
    )
    detail_id = fields.Many2one(
        comodel_name="general_audit_ws_f63f569.detail",
        ondelete="restrict",
    )
    control_id = fields.Many2one(
        related="detail_id.control_id",
        store=True,
    )
    category_id = fields.Many2one(
        related="detail_id.control_id",
        store=True,
        help="Category of the selected control (auto-filled).",
    )
    result = fields.Many2one(
        related="detail_id.result",
    )
    explanation = fields.Text(
        related="detail_id.explanation",
    )
