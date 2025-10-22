# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa0319a2Detail(models.Model):
    _name = "general_audit_ws_a0319a2.detail"
    _description = "Findings That Influence Opinion (a0319a2) - Detail"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_a0319a2",
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
    risk = fields.Selection(
        selection=[
            ("major", "Major"),
            ("minor", "Minor"),
        ],
    )
    condition = fields.Text()
    criteria = fields.Text()
    cause = fields.Text()
    effect = fields.Text()
    proposed_adjustment = fields.Text()
