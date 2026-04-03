# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSfbf57eeComputation(models.Model):
    """Z-Score computation line for the Going Concern worksheet (fbf57ee).

    Each line links one trial balance computation result to the Altman Z-Score
    formula. The auditor reviews the computed values and their contribution to
    the overall Z-Score, which is used to quantitatively assess the client's
    probability of financial distress under ISA 570.
    """

    _name = "general_audit_ws_fbf57ee.computation"
    _description = "Going Concern (fbf57ee) - Computation"
    _order = "worksheet_id, computation_item_id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_fbf57ee",
        string="Worksheet",
        required=True,
        ondelete="cascade",
        index=True,
        help="Parent Going Concern worksheet for this computation line.",
    )
    general_audit_computation_id = fields.Many2one(
        comodel_name="general_audit.computation",
        string="Computation",
        required=True,
        ondelete="restrict",
        help="General Audit computation source used to derive amounts and results.",
    )
    computation_item_id = fields.Many2one(
        related="general_audit_computation_id.computation_item_id",
        string="Computation Item",
        readonly=True,
        store=True,
        help="Computation Item associated with the Computation.",
    )
    current_amount = fields.Float(
        string="Current Amount",
        digits=(16, 2),
        compute="_compute_current_amount",
        store=True,
        help="Amount used for Z-Score computation based on the selected balance type.",
    )
    coefficient = fields.Float(
        string="Coefficient",
        digits=(16, 6),
        required=True,
        help="Weight/Coefficient applied to the computation item when calculating Z-Score.",
    )
    result = fields.Float(
        string="Result",
        digits=(16, 2),
        compute="_compute_result",
        store=True,
        help="Computed result = Current Amount × Coefficient.",
    )

    @api.depends(
        "worksheet_id.balance_type",
        "general_audit_computation_id",
    )
    def _compute_current_amount(self):
        for record in self:
            balance_type = record.worksheet_id.balance_type
            result = 0.0
            if record.general_audit_computation_id:
                if balance_type == "end_period":
                    result = record.general_audit_computation_id.home_balance
                else:
                    result = record.general_audit_computation_id.interim_balance

            record.current_amount = result

    @api.depends(
        "current_amount",
        "coefficient",
    )
    def _compute_result(self):
        for record in self:
            record.result = record.current_amount * record.coefficient
