# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa145276Question(models.Model):
    """Individual question-and-answer record within an Inquiry worksheet (WS-A145276).

    Each record represents a single question posed to the inquiry source during
    the audit inquiry procedure, together with the answer received.

    Inquiry questions are used to gather audit evidence from knowledgeable
    persons inside or outside the entity (ISA 500 / SA 500). The structured
    Q&A format ensures that all relevant topics are covered and that responses
    are documented for audit trail purposes.

    Records are ordered by ``sequence`` within their parent worksheet, allowing
    the auditor to present questions in a logical, controlled order.
    """

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
