# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSaa899bafRelation(models.Model):
    """Relation/Comparison for Plausible Relationship Audit Procedure (WS-AA899BAF).

    Each record defines a comparison between two variables defined in the
    same worksheet, implementing the plausible relationship analysis table
    per SA 520.  The auditor defines an expected (hypothesis) ratio between
    two variables and evaluates the deviation.
    """

    _name = "general_audit_ws_aa899baf.relation"
    _description = "Plausible Relationship Audit Procedure - Relation"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_aa899baf",
        string="Worksheet",
        required=True,
        ondelete="cascade",
        index=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    variable1_id = fields.Many2one(
        comodel_name="general_audit_ws_aa899baf.variable",
        string="Variable 1",
        help="First variable in the plausible relationship comparison.",
    )
    variable2_id = fields.Many2one(
        comodel_name="general_audit_ws_aa899baf.variable",
        string="Variable 2",
        help="Second variable in the plausible relationship comparison.",
    )
    amount1 = fields.Float(
        string="Amount 1",
        digits=(16, 2),
        related="variable1_id.value",
        store=False,
        compute_sudo=True,
        help="Value of Variable 1.",
    )
    amount2 = fields.Float(
        string="Amount 2",
        digits=(16, 2),
        related="variable2_id.value",
        store=False,
        compute_sudo=True,
        help="Value of Variable 2.",
    )
    realization = fields.Float(
        string="Realization",
        digits=(16, 4),
        compute="_compute_realization",
        store=True,
        compute_sudo=True,
        help="Ratio of Amount 1 to Amount 2 (Amount 1 / Amount 2). "
        "Zero when Amount 2 is zero.",
    )
    hypothesis = fields.Float(
        string="Hypothesis",
        digits=(16, 4),
        help="Expected ratio based on the auditor's hypothesis "
        "(plausible relationship).",
    )
    div = fields.Float(
        string="Div",
        digits=(16, 4),
        compute="_compute_div",
        store=True,
        compute_sudo=True,
        help="Deviation: Realization minus Hypothesis.",
    )
    result = fields.Text(
        string="Result",
        help="Auditor's conclusion or notes on this plausible relationship comparison.",
    )

    @api.depends(
        "variable1_id.value",
        "variable2_id.value",
    )
    def _compute_realization(self):
        for record in self:
            amt1 = record.variable1_id.value if record.variable1_id else 0.0
            amt2 = record.variable2_id.value if record.variable2_id else 0.0
            record.realization = amt1 / amt2 if amt2 else 0.0

    @api.depends(
        "realization",
        "hypothesis",
    )
    def _compute_div(self):
        for record in self:
            record.div = record.realization - record.hypothesis
