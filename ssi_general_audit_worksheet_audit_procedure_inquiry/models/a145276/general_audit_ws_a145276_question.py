# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa145276Question(models.Model):
    _name = "general_audit_ws_a145276.question"
    _description = "Inquiry Audit Procedure - Question (a145276)"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_a145276",
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
    question = fields.Text(
        string="Question",
        required=True,
        help="The audit question related to the inquiry procedure.",
    )
    answer = fields.Text(
        string="Answer",
        required=True,
        help="The answer provided for the audit question.",
    )
