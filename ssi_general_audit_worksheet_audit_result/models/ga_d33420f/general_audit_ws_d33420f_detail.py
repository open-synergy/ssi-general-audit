# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd33420fDetail(models.Model):
    _name = "general_audit_ws_d33420f.detail"
    _description = "Control Deficiencies (d33420f) - Detail"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_d33420f",
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
