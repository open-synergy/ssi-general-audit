# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WS1401VerticalHorizontalAnalysis(models.Model):
    _name = "general_audit_ws_b32655a.vertical_horizontal_analysis"
    _description = (
        "Preliminary Analytic Procedure - "
        "Vertical and Horizontal Analysis (b32655a) - Detail"
    )

    worksheet_id = fields.Many2one(
        string="# WS-B32655A",
        comodel_name="general_audit_ws_b32655a",
        required=True,
        ondelete="cascade",
        help=(
            "Link to the related WS-B32655A worksheet. Deleting the worksheet "
            "will also delete this analysis line."
        ),
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="general_audit.standard_detail",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the mapped standard detail line (account/section) "
            "used to compute balances."
        ),
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        related="standard_detail_id.type_id",
        store=True,
        help=(
            "Client account type derived from the standard detail. Stored for "
            "filtering and grouping."
        ),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="standard_detail_id.currency_id",
        store=True,
        help=("Currency of the balances, inherited from the standard detail."),
    )
    sequence = fields.Integer(
        string="Sequence",
        related="standard_detail_id.sequence",
        store=True,
        help="Display sequence taken from the standard detail.",
    )

    computation_item_id = fields.Many2one(
        string="Base Figure Computation Item",
        comodel_name="trial_balance_computation_item",
        related="type_id.analytic_procedure_computation_item_id",
        store=True,
        help=(
            "Computation item used as the base figure (denominator) for the "
            "vertical analysis, derived from the account type."
        ),
    )

    @api.depends(
        "computation_item_id",
        "worksheet_id.general_audit_id",
    )
    def _compute_computation_item(self):
        Computation = self.env["general_audit.computation"]
        for record in self:
            result = False
            ws = record.worksheet_id
            if ws.general_audit_id and record.computation_item_id:
                criteria = [
                    ("general_audit_id", "=", ws.general_audit_id.id),
                    ("computation_item_id", "=", record.computation_item_id.id),
                ]
                computations = Computation.search(criteria)
                if len(computations) > 0:
                    result = computations[0]
            record.general_audit_computation_item_id = result

    general_audit_computation_item_id = fields.Many2one(
        string="General Audit Computation",
        comodel_name="general_audit.computation",
        compute="_compute_computation_item",
        store=True,
        help=(
            "Resolved General Audit computation record that matches the base "
            "figure item for this line."
        ),
    )
    interim_base_figure = fields.Float(
        string="Interim Base Figure",
        related="general_audit_computation_item_id.interim_amount",
        store=True,
        help=(
            "Interim total used as the denominator for interim vertical " "analysis."
        ),
    )
    extrapolation_base_figure = fields.Float(
        string="Extrapolation Base Figure",
        related="general_audit_computation_item_id.extrapolation_amount",
        store=True,
        help=(
            "Extrapolated total used as the denominator for current vertical "
            "analysis when Balance Type is Extrapolation."
        ),
    )
    previous_base_figure = fields.Float(
        string="Previous Base Figure",
        related="general_audit_computation_item_id.previous_amount",
        store=True,
        help=(
            "Previous period total used as the denominator for previous "
            "vertical analysis."
        ),
    )
    interim_balance = fields.Monetary(
        string="Interim Balance",
        related="standard_detail_id.interim_balance",
        store=True,
        help="Interim balance of the account from the standard detail.",
    )

    @api.depends(
        "worksheet_id.base_amount_source",
        "standard_detail_id",
    )
    def _compute_extrapolation_balance(self):
        for record in self:
            result = 0
            if record.worksheet_id.base_amount_source and record.standard_detail_id:
                if record.worksheet_id.base_amount_source == "extrapolation":
                    result = (
                        record.standard_detail_id.adjusted_extrapolation_balance
                    )  # TO DO
                else:
                    result = record.standard_detail_id.home_statement_balance
            record.extrapolation_balance = result

    extrapolation_balance = fields.Monetary(
        string="Current Balance",
        compute="_compute_extrapolation_balance",
        compute_sudo=True,
        store=True,
        help=(
            "Current period balance in home currency. If Balance Type is "
            "Extrapolation, uses adjusted extrapolation balance; otherwise "
            "uses end-period (home statement) balance."
        ),
    )
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="standard_detail_id.previous_balance",
        store=True,
        help="Previous period balance of the account from the standard detail.",
    )

    @api.depends(
        "interim_base_figure",
        "extrapolation_base_figure",
        "previous_base_figure",
        "interim_balance",
        "extrapolation_balance",
        "previous_balance",
    )
    def _compute_vertical(self):
        for record in self:
            interim = extrapolation = previous = 0.0

            if record.interim_base_figure != 0.0:
                interim = (record.interim_balance / record.interim_base_figure) * 100.0

            if record.extrapolation_base_figure != 0.0:
                extrapolation = (
                    record.extrapolation_balance / record.extrapolation_base_figure
                ) * 100.0

            if record.previous_base_figure != 0.0:
                previous = (
                    record.previous_balance / record.previous_base_figure
                ) * 100.0

            record.interim_vertical_analysis = interim
            record.extrapolation_vertical_analysis = extrapolation
            record.previous_vertical_analysis = previous

    interim_vertical_analysis = fields.Float(
        string="Interim Vertical Analysis",
        compute="_compute_vertical",
        store=True,
        help=(
            "Interim vertical analysis in percent: Interim Balance / Interim "
            "Base Figure × 100."
        ),
    )
    extrapolation_vertical_analysis = fields.Float(
        string="Extrapolation Vertical Analysis",
        compute="_compute_vertical",
        store=True,
        help=(
            "Current vertical analysis in percent: Current Balance / "
            "Extrapolation Base Figure × 100."
        ),
    )
    previous_vertical_analysis = fields.Float(
        string="Previous Vertical Analysis",
        compute="_compute_vertical",
        store=True,
        help=(
            "Previous year vertical analysis in percent: Previous Balance / "
            "Previous Base Figure × 100."
        ),
    )

    @api.depends(
        "interim_balance",
        "extrapolation_balance",
        "previous_balance",
    )
    def _compute_horizontal(self):
        for record in self:
            extrapolation_change = interim_change = 0.0
            extrapolation_change_percent = interim_change_percent = 0.0
            if record.standard_detail_id:
                extrapolation_change = (
                    record.extrapolation_balance - record.previous_balance
                )
                interim_change = record.interim_balance - record.previous_balance

            if record.previous_balance != 0.0:
                extrapolation_change_percent = (
                    extrapolation_change / record.previous_balance
                ) * 100.0
                interim_change_percent = (
                    interim_change / record.previous_balance
                ) * 100.0

            record.extrapolation_change = extrapolation_change
            record.interim_change = interim_change
            record.extrapolation_change_percent = extrapolation_change_percent
            record.interim_change_percent = interim_change_percent

    extrapolation_change = fields.Monetary(
        string="Extrapolation Change",
        compute="_compute_horizontal",
        store=True,
        help=(
            "Absolute change between Current Balance (extrapolation) and "
            "Previous Balance."
        ),
    )
    extrapolation_change_percent = fields.Float(
        string="Extrapolation Change (%)",
        compute="_compute_horizontal",
        store=True,
        help=(
            "Percentage change between Current Balance (extrapolation) and "
            "Previous Balance."
        ),
    )
    interim_change = fields.Monetary(
        string="Interim Change",
        compute="_compute_horizontal",
        store=True,
        help=("Absolute change between Interim Balance and Previous Balance."),
    )
    interim_change_percent = fields.Float(
        string="Interim Change (%)",
        compute="_compute_horizontal",
        store=True,
        help=("Percentage change between Interim Balance and Previous Balance."),
    )
    industry_average = fields.Float(
        string="Industry Average",
        help=(
            "Industry benchmark for this account or analysis, used as a "
            "reference for comparison."
        ),
    )
    vertical_need_attention = fields.Boolean(
        string="Vertical Need Attention",
        default=False,
        help=(
            "Enable to flag that vertical analysis results for this line "
            "require auditor attention."
        ),
    )
    horizontal_need_attention = fields.Boolean(
        string="Horizontal Need Attention",
        default=False,
        help=(
            "Enable to flag that horizontal analysis results for this line "
            "require auditor attention."
        ),
    )
    explanation = fields.Char(
        string="Explanation",
        help=(
            "Brief notes to explain significant variances or observations. "
            "Use to document the reason for attention flags."
        ),
    )
