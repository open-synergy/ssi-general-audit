# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc2375d8AnalyticProcedureConclusion(models.Model):
    """
    Conclusion narrative line for the Final Analytical Procedures (c2375d8).

    Each record stores the auditor's **written conclusion** for one
    conclusion category (e.g., "Revenue Trend", "Liquidity Position").
    The ``category_id`` determines the section heading and the display
    order (via ``parent_sequence`` and ``sequence``).

    The auditor uses this model to document the overall conclusion
    reached from the final analytical procedures performed at the end
    of fieldwork, mirroring the conclusion structure already used by
    the Preliminary Analytic Procedure worksheet (c8740d4).
    """

    _name = "general_audit_ws_c2375d8.analytic_procedure_conclusion"
    _description = "Final Analytical Procedures (c2375d8) - Conclusion"
    _order = "parent_sequence, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_c2375d8",
        required=True,
        ondelete="cascade",
        help="Worksheet document that this conclusion belongs to.",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="analytic_procedure_conclusion_category",
        required=True,
        ondelete="restrict",
        help=(
            "Conclusion category that defines the section and ordering of "
            "the conclusion."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        related="category_id.sequence",
        store=True,
        help="Order within the category (lower values appear first).",
    )
    parent_sequence = fields.Integer(
        string="Parent Sequence",
        related="category_id.parent_id.sequence",
        store=True,
        help=(
            "Order of the parent category used for hierarchical sorting of "
            "conclusions."
        ),
    )
    name = fields.Text(
        string="Conclusion",
        required=True,
        help=(
            "Auditor's conclusion text summarizing the results of the "
            "final analytical procedures."
        ),
    )
