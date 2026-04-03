# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AnalyticProcedureConsulsionCategory(models.Model):
    """
    Master: Analytic Procedure Conclusion Category.

    Provides a **configurable hierarchy of categories** used to organise the
    auditor's conclusion narratives on the Preliminary Analytic Procedure
    summary worksheet (``general_audit_ws_c8740d4``).

    Examples of categories and their hierarchy:

    * Revenue and Cost of Sales
      * Net Revenue Trend
      * Gross Margin Analysis
    * Liquidity Position
    * Going Concern Indicators

    ``sequence`` and ``parent_id`` control the display order in the conclusion
    section of the form view.  Conclusion lines
    (``general_audit_ws_c8740d4.analytic_procedure_conclusion``) reference
    a category to determine their position in the structured narrative.
    """

    _name = "analytic_procedure_conclusion_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Analytic Procedure Consulsion Category"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Ordering number. Lower values appear first.",
    )
    parent_id = fields.Many2one(
        string="Parent",
        comodel_name="analytic_procedure_conclusion_category",
        help=("Parent category to build a hierarchy of conclusion categories."),
    )
