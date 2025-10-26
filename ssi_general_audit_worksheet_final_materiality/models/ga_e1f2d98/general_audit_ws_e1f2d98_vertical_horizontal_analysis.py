# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WSE1F2D98VerticalHorizontalAnalysis(models.Model):
    _name = "general_audit_ws_e1f2d98.vertical_horizontal_analysis"
    _description = (
        "Final Analytic Procedure - "
        "Vertical and Horizontal Analysis (e1f2d98) - Detail"
    )

    worksheet_id = fields.Many2one(
        string="# WS-E1F2D98",
        comodel_name="general_audit_ws_e1f2d98",
        required=True,
        ondelete="cascade",
        help=(
            "Link to the related WS-E1F2D98 worksheet. Deleting the worksheet "
            "will also delete this analysis line."
        ),
    )
    prelim_analysis_id = fields.Many2one(
        string="Preliminary Detail Analysis",
        comodel_name="general_audit_ws_b32655a.vertical_horizontal_analysis",
        required=True,
        ondelete="restrict",
        help=(
            "Link to the related preliminary detail analysis. Deleting the "
            "analysis will also delete this line."
        ),
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        related="prelim_analysis_id.standard_detail_id",
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
    # Base Figure
    previous_base_figure = fields.Float(
        string="Previous Base Figure",
        related="general_audit_computation_item_id.previous_amount",
        store=True,
        help=(
            "Previous period total used as the denominator for previous "
            "vertical analysis."
        ),
    )
    end_period_base_figure = fields.Float(
        string="End Period Base Figure",
        related="general_audit_computation_item_id.home_amount",
        store=True,
        help=(
            "End period total used as the denominator for current vertical " "analysis."
        ),
    )
    audited_base_figure = fields.Float(
        string="Audited Base Figure",
        related="general_audit_computation_item_id.audited_amount",
        store=True,
        help=(
            "Audited total used as the denominator for audited vertical " "analysis."
        ),
    )
    # Balance
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="standard_detail_id.previous_balance",
        store=True,
        help="Previous period balance of the account from the standard detail.",
    )
    end_period_balance = fields.Monetary(
        string="End Period Balance",
        related="standard_detail_id.home_statement_balance",
        store=True,
        help="End period balance of the account from the standard detail.",
    )
    audited_balance = fields.Monetary(
        string="Audited Balance",
        related="standard_detail_id.audited_balance",
        store=True,
        help="Audited balance of the account from the standard detail.",
    )

    @api.depends(
        "previous_base_figure",
        "end_period_base_figure",
        "audited_base_figure",
        "previous_balance",
        "end_period_balance",
        "audited_balance",
    )
    def _compute_vertical(self):
        for record in self:
            previous = end_period = audited = 0.0

            if record.previous_base_figure != 0.0:
                previous = (
                    record.previous_balance / record.previous_base_figure
                ) * 100.0

            if record.end_period_base_figure != 0.0:
                end_period = (
                    record.end_period_balance / record.end_period_base_figure
                ) * 100.0

            if record.audited_base_figure != 0.0:
                audited = (record.audited_balance / record.audited_base_figure) * 100.0

            record.previous_vertical_analysis = previous
            record.end_period_vertical_analysis = end_period
            record.audited_vertical_analysis = audited

    previous_vertical_analysis = fields.Float(
        string="Previous Vertical Analysis",
        compute="_compute_vertical",
        compute_sudo=True,
        store=True,
        help=(
            "Previous year vertical analysis in percent: Previous Balance / "
            "Previous Base Figure × 100."
        ),
    )
    end_period_vertical_analysis = fields.Float(
        string="End Period Vertical Analysis",
        compute="_compute_vertical",
        compute_sudo=True,
        store=True,
        help=(
            "Current year vertical analysis in percent: End Period Balance / "
            "End Period Base Figure × 100."
        ),
    )
    audited_vertical_analysis = fields.Float(
        string="Audited Vertical Analysis",
        compute="_compute_vertical",
        compute_sudo=True,
        store=True,
        help=(
            "Audited vertical analysis in percent: Audited Balance / "
            "Audited Base Figure × 100."
        ),
    )

    @api.depends(
        "previous_balance",
        "end_period_balance",
        "audited_balance",
    )
    def _compute_horizontal(self):
        for record in self:
            end_period_change = audited_change = 0.0
            end_period_change_percent = audited_change_percent = 0.0
            if record.standard_detail_id:
                end_period_change = record.end_period_balance - record.previous_balance
                audited_change = record.audited_balance - record.previous_balance

            if record.previous_balance != 0.0:
                end_period_change_percent = (
                    end_period_change / record.previous_balance
                ) * 100.0
                audited_change_percent = (
                    audited_change / record.previous_balance
                ) * 100.0

            record.end_period_change = end_period_change
            record.audited_change = audited_change
            record.end_period_change_percent = end_period_change_percent
            record.audited_change_percent = audited_change_percent

    end_period_change = fields.Monetary(
        string="End Period Change",
        compute="_compute_horizontal",
        compute_sudo=True,
        store=True,
        help=(
            "Absolute change between Current Balance (end period) and "
            "Previous Balance."
        ),
    )
    end_period_change_percent = fields.Float(
        string="End Period Change (%)",
        compute="_compute_horizontal",
        store=True,
        help=(
            "Percentage change between Current Balance (end period) and "
            "Previous Balance."
        ),
    )
    audited_change = fields.Monetary(
        string="Audited Change",
        compute="_compute_horizontal",
        compute_sudo=True,
        store=True,
        help=("Absolute change between Audited Balance and Previous Balance."),
    )
    audited_change_percent = fields.Float(
        string="Audited Change (%)",
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
