# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWS6dcda0e(models.Model):
    _name = "general_audit_ws_6dcda0e"
    _description = "Specific Materiality (6dcda0e)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_preliminary_materiality.worksheet_type_6dcda0e"
    )

    worksheet_d9d2b44_id = fields.Many2one(
        string="# WS D9D2B44",
        comodel_name="general_audit_ws_d9d2b44",
        required=False,
        readonly=True,
        ondelete="restrict",
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help=(
            "Link to the Materiality Computation (d9d2b44) worksheet that "
            "provides overall and performance materiality thresholds."
        ),
    )

    base_amount_source = fields.Selection(
        related="worksheet_d9d2b44_id.base_amount_source",
        help=(
            "Balance source used when deriving the base amount: "
            "Extrapolation or End Period."
        ),
    )

    @api.depends(
        "worksheet_d9d2b44_id",
        "materiality_type",
    )
    def _compute_base_amount(self):
        for record in self:
            base = 0.0
            if record.worksheet_d9d2b44_id:
                worksheet_d9d2b44 = record.worksheet_d9d2b44_id

                if record.materiality_type == "om":
                    base = worksheet_d9d2b44.overall_materiality
                else:
                    base = worksheet_d9d2b44.performance_materiality

            record.base = base

    base = fields.Monetary(
        string="Balance",
        compute="_compute_base_amount",
        store=True,
        currency_field="currency_id",
        help=(
            "Base threshold amount (Overall or Performance Materiality) "
            "derived from the linked computation worksheet."
        ),
    )

    materiality_type = fields.Selection(
        string="Materiality Type",
        selection=[
            ("om", "Overall Materiality"),
            ("pm", "Performance Materiality"),
        ],
        required=False,
        default="pm",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help=(
            "Choose which materiality threshold to use in this worksheet: "
            "Overall or Performance."
        ),
    )
    materiality_mapping_ids = fields.One2many(
        string="Materiality Mapping",
        comodel_name="general_audit_ws_6dcda0e_materiality_mapping",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Mapping lines of standard details with their materiality assessment.",
    )

    def action_reload_materiality_mapping(self):
        for record in self.sudo():
            record.onchange_materiality_mapping_ids()

    @api.onchange("general_audit_id")
    def onchange_materiality_mapping_ids(self):
        self.update({"materiality_mapping_ids": [(5, 0, 0)]})
        if self.general_audit_id:
            result = []
            for detail in self.general_audit_id.standard_detail_ids:
                result.append(
                    (
                        0,
                        0,
                        {
                            "standard_detail_id": detail.id,
                        },
                    )
                )
            self.update({"materiality_mapping_ids": result})

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
