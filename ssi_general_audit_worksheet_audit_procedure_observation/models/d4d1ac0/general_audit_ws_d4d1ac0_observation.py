# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd4d1ac0Question(models.Model):
    _name = "general_audit_ws_d4d1ac0.observation"
    _description = "Inquiry Audit Procedure - Observation (d4d1ac0)"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_d4d1ac0",
        string="Worksheet",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help="The sequence order of the question in the inquiry procedure.",
    )
    subject = fields.Text(
        string="Subject",
        required=True,
        help="The subject of the observation made during the audit procedure.",
    )
    observation = fields.Text(
        string="Observation",
        required=True,
        help="The observation made during the audit procedure.",
    )
