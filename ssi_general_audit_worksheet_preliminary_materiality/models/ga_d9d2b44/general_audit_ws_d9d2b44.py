# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSd9d2b44(models.Model):
    _name = "general_audit_ws_d9d2b44"
    _description = "Materiality Computation (d9d2b44)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_preliminary_materiality.worksheet_type_d9d2b44"
    )

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

    @api.depends(
        "general_audit_id",
        "computation_item_id",
        "other_amount_ok",
        "other_base_amount",
        "base_amount_source",
    )
    def _compute_base(self):
        Computation = self.env["general_audit.computation"]
        for document in self:
            general_audit_computation_id = False
            base_computation_amount = 0.0
            if (
                document.general_audit_id
                and document.computation_item_id
                and document.base_amount_source
            ):
                criteria = [
                    ("general_audit_id.id", "=", document.general_audit_id.id),
                    ("computation_item_id.id", "=", document.computation_item_id.id),
                ]
                computations = Computation.search(criteria)
                if len(computations) > 0:
                    general_audit_computation_id = computations[0]
                    if document.base_amount_source == "extrapolation":
                        base_computation_amount = (
                            general_audit_computation_id.extrapolation_amount
                        )
                    elif document.base_amount_source == "end_period":
                        base_computation_amount = (
                            general_audit_computation_id.home_amount
                        )

            if document.other_amount_ok:
                base_computation_amount = document.other_base_amount

            document.general_audit_computation_id = general_audit_computation_id
            document.base_computation_amount = base_computation_amount

    base_amount_source = fields.Selection(
        string="Balance Type",
        selection=[
            ("extrapolation", "Extrapolation"),
            ("end_period", "End Period"),
        ],
        required=False,
        default="extrapolation",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help=(
            "Source of the base amount used in materiality computation: "
            "Extrapolation or End Period."
        ),
    )

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
        store=True,
        currency_field="currency_id",
        help="Calculated base amount used to compute materiality.",
    )
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

    @ssi_decorator.pre_confirm_check()
    def _10_check_balance_type(self):
        self.ensure_one()
        criteria = [
            ("general_audit_id", "=", self.general_audit_id.id),
            ("type_id", "=", self.type_id.id),
            ("base_amount_source", "=", self.base_amount_source),
            ("id", "!=", self.id),
        ]
        check = self.search(criteria)
        if check:
            error_message = """
            Context: Confirmation for %s
            Database ID: %s
            Problem: Balance type %s is already used for General Audit %s.
            """ % (
                self.type_id.name,
                self.id,
                self.base_amount_source,
                self.name,
            )
            raise ValidationError(_(error_message))
