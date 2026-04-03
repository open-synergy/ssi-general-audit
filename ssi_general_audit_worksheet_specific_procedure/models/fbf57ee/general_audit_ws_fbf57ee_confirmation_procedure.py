# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSfbf57eeConfirmationProcedure(models.Model):
    """Confirmation procedure line for the Going Concern worksheet (fbf57ee).

    Each line represents one going concern confirmation procedure from the
    master list, recording whether the procedure was performed and documenting
    any relevant observations. Supports evidence gathering for the going concern
    assessment under ISA 570.
    """

    _name = "general_audit_ws_fbf57ee.confirmation_procedure"
    _description = "Going Concern (fbf57ee) - Confirmation Procedure"
    _order = "worksheet_id, confirmation_procedure_id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_fbf57ee",
        string="Worksheet",
        required=True,
        ondelete="cascade",
        index=True,
        help="Parent Going Concern worksheet for this confirmation line.",
    )

    confirmation_procedure_id = fields.Many2one(
        comodel_name="general_audit_going_concern_confirmation_procedure",
        string="Confirmation Procedure",
        required=True,
        ondelete="restrict",
        index=True,
        help="The specific going concern confirmation procedure to be performed.",
    )
    performed = fields.Selection(
        selection=[
            ("performed", "Performed"),
            ("not_performed", "Not Performed"),
            ("na", "Not Applicable"),
        ],
        string="Performed",
        default="not_performed",
        required=True,
        help="Indicates whether the procedure has been performed.",
    )
    risk_assessment = fields.Selection(
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        string="Risk Assessment",
        default="medium",
        required=True,
        help="Indicates the risk assessment level for this procedure.",
    )
    explanation = fields.Text(
        string="Explanation",
        help="Provide additional details or explanations regarding the procedure.",
    )
    reference = fields.Char(
        string="Reference",
        help="Reference document or note related to this procedure.",
    )
