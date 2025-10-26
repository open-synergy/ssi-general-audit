# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSbb33b94(models.Model):
    _name = "general_audit_ws_bb33b94"
    _description = "Final Materiality (bb33b94)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_final_materiality." "worksheet_type_bb33b94"
    )

    # Planning
    planning_ws_d9d2b44_id = fields.Many2one(
        comodel_name="general_audit_ws_d9d2b44",
        string="# Preliminary Materiality (Planning)",
        ondelete="restrict",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    planning_base_amount = fields.Monetary(
        string="Planning Base Amount",
        compute="_compute_planning",
        store=True,
        compute_sudo=True,
    )
    planning_overall_materiality_percentage = fields.Float(
        string="Planning Overall Materiality Percentage (%)",
        compute="_compute_planning",
        store=True,
        compute_sudo=True,
    )
    planning_overall_materiality = fields.Monetary(
        string="Planning Overall Materiality",
        compute="_compute_planning",
        store=True,
        compute_sudo=True,
    )
    planning_performance_materiality_percentage = fields.Float(
        string="Planning Performance Materiality Percentage (%)",
        compute="_compute_planning",
        store=True,
        compute_sudo=True,
    )
    planning_performance_materiality = fields.Monetary(
        string="Planning Performance Materiality",
        compute="_compute_planning",
        store=True,
        compute_sudo=True,
    )
    planning_tolerable_misstatement_percentage = fields.Float(
        string="Planning Tolerable Misstatement Percentage (%)",
        compute="_compute_planning",
        store=True,
        compute_sudo=True,
    )
    planning_tolerable_misstatement = fields.Monetary(
        string="Planning Tolerable Misstatement",
        compute="_compute_planning",
        store=True,
        compute_sudo=True,
    )

    # Uniaudited
    end_period_ws_d9d2b44_id = fields.Many2one(
        comodel_name="general_audit_ws_d9d2b44",
        string="# Preliminary Materiality (End Period)",
        ondelete="restrict",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    end_period_base_amount = fields.Monetary(
        string="End Period Base Amount",
        compute="_compute_end_period",
        store=True,
        compute_sudo=True,
    )
    end_period_overall_materiality_percentage = fields.Float(
        string="End Period Overall Materiality Percentage (%)",
        compute="_compute_end_period",
        store=True,
        compute_sudo=True,
    )
    end_period_overall_materiality = fields.Monetary(
        string="End Period Overall Materiality",
        compute="_compute_end_period",
        store=True,
        compute_sudo=True,
    )
    end_period_performance_materiality_percentage = fields.Float(
        string="End Period Performance Materiality Percentage (%)",
        compute="_compute_end_period",
        store=True,
        compute_sudo=True,
    )
    end_period_performance_materiality = fields.Monetary(
        string="End Period Performance Materiality",
        compute="_compute_end_period",
        store=True,
        compute_sudo=True,
    )
    end_period_tolerable_misstatement_percentage = fields.Float(
        string="End Period Tolerable Misstatement Percentage (%)",
        compute="_compute_end_period",
        store=True,
        compute_sudo=True,
    )
    end_period_tolerable_misstatement = fields.Monetary(
        string="End Period Tolerable Misstatement",
        compute="_compute_end_period",
        store=True,
        compute_sudo=True,
    )

    computation_item_id = fields.Many2one(
        string="Computation Item",
        related="ws_d9d2b44_id.computation_item_id",
        readonly=True,
        store=True,
    )
    general_audit_computation_id = fields.Many2one(
        string="General Audit Computation",
        related="ws_d9d2b44_id.general_audit_computation_id",
        readonly=True,
        store=True,
    )
    other_amount_ok = fields.Boolean(
        string="Use Other Amount",
        related="ws_d9d2b44_id.other_amount_ok",
        readonly=True,
        store=True,
    )
    other_amount_source = fields.Char(
        string="Other Amount Source",
        related="ws_d9d2b44_id.other_amount_source",
        readonly=True,
        store=True,
    )
    other_base_amount = fields.Monetary(
        string="Other Base Amount",
        related="ws_d9d2b44_id.other_base_amount",
        readonly=True,
        store=True,
    )

    # Base Amount
    other_amount_ok = fields.Boolean(
        string="Use Other Amount",
        default=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Enable to override the computed base with a custom 'Other " "Base Amount'."
        ),
    )
    other_amount_source = fields.Char(
        string="Other Amount's Source",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Describe the source/rationale of the custom 'Other Base Amount'.",
    )
    other_base_amount = fields.Monetary(
        string="Other Base Amount",
        default=0.0,
        required=True,
        readonly=True,
        currency_field="currency_id",
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Custom base amount to use when 'Use Other Amount' is enabled.",
    )

    allowed_computation_item_ids = fields.Many2many(
        string="Allowed Computation Item To Use",
        comodel_name="trial_balance_computation_item",
        compute="_compute_allowed_computation_item_ids",
        store=False,
        help=("Computation items available based on the selected General " "Audit."),
    )

    computation_item_id = fields.Many2one(
        string="Computation Item To Use",
        comodel_name="trial_balance_computation_item",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        ondelete="restrict",
        help=(
            "Computation item from the General Audit whose value will be "
            "used to derive the base amount."
        ),
    )
    general_audit_computation_id = fields.Many2one(
        string="General Audit Computation",
        comodel_name="general_audit.computation",
        compute="_compute_base",
        store=True,
        help=(
            "Matched General Audit computation record for the selected "
            "computation item."
        ),
    )
    base_computation_amount = fields.Monetary(
        string="Base Amount for Materiality Computation",
        compute="_compute_base",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Calculated base amount used to compute materiality.",
    )

    # Materiality
    overall_materiality_percentage = fields.Float(
        string="Overall Materiality Percentage",
        default=0.0,
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help=(
            "Percentage applied to the base amount to compute Overall " "Materiality."
        ),
    )
    overall_materiality = fields.Monetary(
        string="Overall Materiality",
        compute="_compute_materiality",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Computed Overall Materiality amount.",
    )
    overall_materiality_consideration = fields.Text(
        string="Overall Materiality Consideration",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Considerations and professional judgement supporting the "
            "selected overall materiality percentage."
        ),
    )
    performance_materiality_percentage = fields.Float(
        string="Performance Materiality Percentage",
        default=0.0,
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help=(
            "Percentage of Overall Materiality used to compute Performance "
            "Materiality."
        ),
    )
    performance_materiality = fields.Monetary(
        string="Performance Materiality",
        compute="_compute_materiality",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Computed Performance Materiality amount.",
    )
    performance_materiality_consideration = fields.Text(
        string="Performence Materiality Consideration",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Considerations and professional judgement supporting the "
            "selected performance materiality percentage."
        ),
    )
    tolerable_misstatement_percentage = fields.Float(
        string="Tolerable Misstatement Percentage",
        default=0.0,
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help=(
            "Percentage of Performance Materiality used to compute the "
            "Tolerable Misstatement."
        ),
    )
    tolerable_misstatement = fields.Monetary(
        string="Tolerable Misstatement",
        compute="_compute_materiality",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Computed Tolerable Misstatement amount.",
    )
    tolerable_misstatement_consideration = fields.Text(
        string="Tolerable Misstatement Consideration",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Considerations and professional judgement supporting the "
            "selected tolerable misstatement percentage."
        ),
    )

    # Overall Materiality Diff
    audited_unaudited_overall_materiality_diff = fields.Monetary(
        string="Audited vs Uniaudited Overall Materiality Difference",
        compute="_compute_diff",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help=(
            "Difference between the Overall Materiality calculated based "
            "on Audited and Uniaudited Financial Statements."
        ),
    )
    audited_unaudited_overall_materiality_diff_percentage = fields.Float(
        string="Audited vs Uniaudited Overall Materiality Difference (%)",
        compute="_compute_diff",
        compute_sudo=True,
        store=True,
        help=(
            "Percentage difference between the Overall Materiality "
            "calculated based on Audited and Uniaudited Financial "
            "Statements."
        ),
    )
    audited_planning_overall_materiality_diff = fields.Monetary(
        string="Audited vs Planning Overall Materiality Difference",
        compute="_compute_diff",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help=(
            "Difference between the Overall Materiality calculated based "
            "on Audited Financial Statements and the Planning "
            "Overall Materiality."
        ),
    )
    audited_planning_overall_materiality_diff_percentage = fields.Float(
        string="Audited vs Planning Overall Materiality Difference (%)",
        compute="_compute_diff",
        compute_sudo=True,
        store=True,
        help=(
            "Percentage difference between the Overall Materiality "
            "calculated based on Audited Financial Statements and the "
            "Planning Overall Materiality."
        ),
    )

    # Performance Materiality Diff
    audited_unaudited_performance_materiality_diff = fields.Monetary(
        string="Audited vs Uniaudited Performance Materiality Difference",
        compute="_compute_diff",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help=(
            "Difference between the Performance Materiality calculated "
            "based on Audited and Uniaudited Financial Statements."
        ),
    )
    audited_unaudited_performance_materiality_diff_percentage = fields.Float(
        string="Audited vs Uniaudited Performance Materiality Difference (%)",
        compute="_compute_diff",
        compute_sudo=True,
        store=True,
        help=(
            "Percentage difference between the Performance Materiality "
            "calculated based on Audited and Uniaudited Financial "
            "Statements."
        ),
    )
    audited_planning_performance_materiality_diff = fields.Monetary(
        string="Audited vs Planning Performance Materiality Difference",
        compute="_compute_diff",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help=(
            "Difference between the Performance Materiality calculated "
            "based on Audited Financial Statements and the Planning "
            "Performance Materiality."
        ),
    )
    audited_planning_performance_materiality_diff_percentage = fields.Float(
        string="Audited vs Planning Performance Materiality Difference (%)",
        compute="_compute_diff",
        compute_sudo=True,
        store=True,
        help=(
            "Percentage difference between the Performance Materiality "
            "calculated based on Audited Financial Statements and the "
            "Planning Performance Materiality."
        ),
    )

    # Tolerable Misstatement Diff
    audited_unaudited_tolerable_misstatement_diff = fields.Monetary(
        string="Audited vs Uniaudited Tolerable Misstatement Difference",
        compute="_compute_diff",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help=(
            "Difference between the Tolerable Misstatement calculated "
            "based on Audited and Uniaudited Financial Statements."
        ),
    )
    audited_unaudited_tolerable_misstatement_diff_percentage = fields.Float(
        string="Audited vs Uniaudited Tolerable Misstatement Difference (%)",
        compute="_compute_diff",
        compute_sudo=True,
        store=True,
        help=(
            "Percentage difference between the Tolerable Misstatement "
            "calculated based on Audited and Uniaudited Financial "
            "Statements."
        ),
    )
    audited_planning_tolerable_misstatement_diff = fields.Monetary(
        string="Audited vs Planning Tolerable Misstatement Difference",
        compute="_compute_diff",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help=(
            "Difference between the Tolerable Misstatement calculated "
            "based on Audited Financial Statements and the Planning "
            "Tolerable Misstatement."
        ),
    )
    audited_planning_tolerable_misstatement_diff_percentage = fields.Float(
        string="Audited vs Planning Tolerable Misstatement Difference (%)",
        compute="_compute_diff",
        compute_sudo=True,
        store=True,
        help=(
            "Percentage difference between the Tolerable Misstatement "
            "calculated based on Audited Financial Statements and the "
            "Planning Tolerable Misstatement."
        ),
    )

    @api.depends(
        "planning_ws_d9d2b44_id",
        "end_period_ws_d9d2b44_id",
    )
    def _compute_planning(self):
        for record in self:
            if record.planning_ws_d9d2b44_id:
                record.planning_base_amount = (
                    record.planning_ws_d9d2b44_id.base_computation_amount
                )
                record.planning_overall_materiality_percentage = (
                    record.planning_ws_d9d2b44_id.overall_materiality_percentage
                )
                record.planning_overall_materiality = (
                    record.planning_ws_d9d2b44_id.overall_materiality
                )
                record.planning_performance_materiality_percentage = (
                    record.planning_ws_d9d2b44_id.performance_materiality_percentage
                )
                record.planning_performance_materiality = (
                    record.planning_ws_d9d2b44_id.performance_materiality
                )
                record.planning_tolerable_misstatement_percentage = (
                    record.planning_ws_d9d2b44_id.tolerable_misstatement_percentage
                )
                record.planning_tolerable_misstatement = (
                    record.planning_ws_d9d2b44_id.tolerable_misstatement
                )
            elif record.end_period_ws_d9d2b44_id:
                record.planning_base_amount = (
                    record.end_period_ws_d9d2b44_id.base_computation_amount
                )
                record.planning_overall_materiality_percentage = (
                    record.end_period_ws_d9d2b44_id.overall_materiality_percentage
                )
                record.planning_overall_materiality = (
                    record.end_period_ws_d9d2b44_id.overall_materiality
                )
                record.planning_performance_materiality_percentage = (
                    record.end_period_ws_d9d2b44_id.performance_materiality_percentage
                )
                record.planning_performance_materiality = (
                    record.end_period_ws_d9d2b44_id.performance_materiality
                )
                record.planning_tolerable_misstatement_percentage = (
                    record.end_period_ws_d9d2b44_id.tolerable_misstatement_percentage
                )
                record.planning_tolerable_misstatement = (
                    record.end_period_ws_d9d2b44_id.tolerable_misstatement
                )
            else:
                record.planning_base_amount = 0.0
                record.planning_overall_materiality_percentage = 0.0
                record.planning_overall_materiality = 0.0
                record.planning_performance_materiality_percentage = 0.0
                record.planning_performance_materiality = 0.0
                record.planning_tolerable_misstatement_percentage = 0.0
                record.planning_tolerable_misstatement = 0.0

    @api.depends(
        "end_period_ws_d9d2b44_id",
    )
    def _compute_end_period(self):
        for record in self:
            if record.end_period_ws_d9d2b44_id:
                record.end_period_base_amount = (
                    record.end_period_ws_d9d2b44_id.base_computation_amount
                )
                record.end_period_overall_materiality_percentage = (
                    record.end_period_ws_d9d2b44_id.overall_materiality_percentage
                )
                record.end_period_overall_materiality = (
                    record.end_period_ws_d9d2b44_id.overall_materiality
                )
                record.end_period_performance_materiality_percentage = (
                    record.end_period_ws_d9d2b44_id.performance_materiality_percentage
                )
                record.end_period_performance_materiality = (
                    record.end_period_ws_d9d2b44_id.performance_materiality
                )
                record.end_period_tolerable_misstatement_percentage = (
                    record.end_period_ws_d9d2b44_id.tolerable_misstatement_percentage
                )
                record.end_period_tolerable_misstatement = (
                    record.end_period_ws_d9d2b44_id.tolerable_misstatement
                )
            else:
                record.end_period_base_amount = 0.0
                record.end_period_overall_materiality_percentage = 0.0
                record.end_period_overall_materiality = 0.0
                record.end_period_performance_materiality_percentage = 0.0
                record.end_period_performance_materiality = 0.0
                record.end_period_tolerable_misstatement_percentage = 0.0
                record.end_period_tolerable_misstatement = 0.0

    @api.depends(
        "overall_materiality",
        "performance_materiality",
        "tolerable_misstatement",
        "end_period_overall_materiality",
        "end_period_performance_materiality",
        "end_period_tolerable_misstatement",
        "planning_overall_materiality",
        "planning_performance_materiality",
        "planning_tolerable_misstatement",
    )
    def _compute_diff(self):
        for record in self:
            # Overall Materiality Diff
            record.audited_unaudited_overall_materiality_diff = (
                record.overall_materiality - record.end_period_overall_materiality
            )
            if record.end_period_overall_materiality != 0.0:
                record.audited_unaudited_overall_materiality_diff_percentage = (
                    record.audited_unaudited_overall_materiality_diff
                    / record.end_period_overall_materiality
                ) * 100.0
            else:
                record.audited_unaudited_overall_materiality_diff_percentage = 0.0

            record.audited_planning_overall_materiality_diff = (
                record.overall_materiality - record.planning_overall_materiality
            )
            if record.planning_overall_materiality != 0.0:
                record.audited_planning_overall_materiality_diff_percentage = (
                    record.audited_planning_overall_materiality_diff
                    / record.planning_overall_materiality
                ) * 100.0
            else:
                record.audited_planning_overall_materiality_diff_percentage = 0.0

            # Performance Materiality Diff
            record.audited_unaudited_performance_materiality_diff = (
                record.performance_materiality
                - record.end_period_performance_materiality
            )
            if record.end_period_performance_materiality != 0.0:
                record.audited_unaudited_performance_materiality_diff_percentage = (
                    record.audited_unaudited_performance_materiality_diff
                    / record.end_period_performance_materiality
                ) * 100.0
            else:
                record.audited_unaudited_performance_materiality_diff_percentage = 0.0

            record.audited_planning_performance_materiality_diff = (
                record.performance_materiality - record.planning_performance_materiality
            )
            if record.planning_performance_materiality != 0.0:
                record.audited_planning_performance_materiality_diff_percentage = (
                    record.audited_planning_performance_materiality_diff
                    / record.planning_performance_materiality
                ) * 100.0
            else:
                record.audited_planning_performance_materiality_diff_percentage = 0.0

            # Tolerable Misstatement Diff
            record.audited_unaudited_tolerable_misstatement_diff = (
                record.tolerable_misstatement - record.end_period_tolerable_misstatement
            )
            if record.end_period_tolerable_misstatement != 0.0:
                record.audited_unaudited_tolerable_misstatement_diff_percentage = (
                    record.audited_unaudited_tolerable_misstatement_diff
                    / record.end_period_tolerable_misstatement
                ) * 100.0
            else:
                record.audited_unaudited_tolerable_misstatement_diff_percentage = 0.0

    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_computation_item_ids(self):
        for record in self:
            record.allowed_computation_item_ids = [(5, 0, 0)]
            if record.general_audit_id:
                record.allowed_computation_item_ids = [
                    (
                        6,
                        0,
                        record.general_audit_id.computation_ids.mapped(
                            "computation_item_id"
                        ).ids,
                    )
                ]

    @api.depends(
        "general_audit_id",
        "computation_item_id",
        "other_amount_ok",
        "other_base_amount",
    )
    def _compute_base(self):
        Computation = self.env["general_audit.computation"]
        for document in self:
            general_audit_computation_id = False
            base_computation_amount = 0.0
            if document.general_audit_id and document.computation_item_id:
                criteria = [
                    ("general_audit_id.id", "=", document.general_audit_id.id),
                    ("computation_item_id.id", "=", document.computation_item_id.id),
                ]
                computations = Computation.search(criteria)
                if len(computations) > 0:
                    general_audit_computation_id = computations[0]
                    base_computation_amount = (
                        general_audit_computation_id.audited_amount
                    )

            if document.other_amount_ok:
                base_computation_amount = document.other_base_amount

            document.general_audit_computation_id = general_audit_computation_id
            document.base_computation_amount = base_computation_amount

    @api.depends(
        "base_computation_amount",
        "other_base_amount",
        "performance_materiality_percentage",
        "overall_materiality_percentage",
        "tolerable_misstatement_percentage",
    )
    def _compute_materiality(self):
        for document in self:
            document.overall_materiality = (
                document.overall_materiality_percentage / 100.00
            ) * document.base_computation_amount
            document.performance_materiality = (
                document.performance_materiality_percentage / 100.00
            ) * document.overall_materiality
            document.tolerable_misstatement = (
                document.tolerable_misstatement_percentage / 100.00
            ) * document.performance_materiality
