# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSd4289e4(models.Model):
    _name = "general_audit_ws_d4289e4"
    _description = "Preliminary Analytic Procedure - Ratio Analysis (d4289e4)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_preliminary_analytic_procedure."
        "worksheet_type_d4289e4"
    )

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
    )
    ratio_ids = fields.One2many(
        string="Ratio Ratio",
        comodel_name="general_audit_ws_d4289e4.ratio",
        inverse_name="worksheet_id",
    )
    liquidity_ratio_ids = fields.One2many(
        string="Liquidity Ratio",
        comodel_name="general_audit_ws_d4289e4.ratio",
        inverse_name="worksheet_id",
        domain=[
            ("financial_ratio_id.category", "=", "liquidity"),
        ],
    )
    activity_ratio_ids = fields.One2many(
        string="Activity Ratio",
        comodel_name="general_audit_ws_d4289e4.ratio",
        inverse_name="worksheet_id",
        domain=[
            ("financial_ratio_id.category", "=", "activity"),
        ],
    )
    solvency_ratio_ids = fields.One2many(
        string="Solvency Ratio",
        comodel_name="general_audit_ws_d4289e4.ratio",
        inverse_name="worksheet_id",
        domain=[
            ("financial_ratio_id.category", "=", "solvency"),
        ],
    )
    profitability_ratio_ids = fields.One2many(
        string="Profitability Ratio",
        comodel_name="general_audit_ws_d4289e4.ratio",
        inverse_name="worksheet_id",
        domain=[
            ("financial_ratio_id.category", "=", "profitability"),
        ],
    )

    @api.onchange("general_audit_id")
    def onchange_ratio_ids(self):
        self.update({"ratio_ids": [(5, 0, 0)]})
        FinancialRatio = self.env["client_financial_ratio"]
        if self.general_audit_id:
            result = []
            for ratio in FinancialRatio.search([]):
                result.append(
                    (
                        0,
                        0,
                        {
                            "financial_ratio_id": ratio.id,
                        },
                    )
                )
            self.update({"ratio_ids": result})

    def action_compute_ratio(self):
        for record in self:
            record._recompute_computation()

    @api.onchange(
        "base_amount_source",
    )
    def onchange_recompute_ratio_ids(self):
        self._recompute_computation()

    @ssi_decorator.post_confirm_action()
    def _recompute_computation(self):
        self.ensure_one()
        additional_dict = self._get_additional_dict()
        for computation in self.ratio_ids:
            additionaldict = computation._recompute(additional_dict)
            additional_dict = additionaldict

        self.general_audit_id._recompute_extrapolation_computation()

    def _get_additional_dict(self):
        self.ensure_one()
        result = {"account_type": {}, "account_group": {}, "computation": {}}
        # Load general audit's standard detail to dict
        for data in self.general_audit_id.standard_detail_ids:
            result["account_type"].update(
                {
                    data.type_id.code: {
                        "extrapolation": data.extrapolation_balance,
                        "interim": data.interim_balance,
                        "previous": data.previous_balance,
                        "end_period": data.home_statement_balance,
                        "extrapolation_avg": data.extrapolation_avg,
                        "interim_avg": data.interim_avg,
                        "end_period_avg": data.home_statement_avg,
                    },
                }
            )

        # Load general audit's group summary to dict
        for data in self.general_audit_id.group_detail_ids:
            result["account_group"].update(
                {
                    data.group_id.code: {
                        "extrapolation": data.extrapolation_balance,
                        "interim": data.interim_balance,
                        "previous": data.previous_balance,
                        "end_period": data.home_statement_balance,
                        "extrapolation_avg": data.extrapolation_avg,
                        "interim_avg": data.interim_avg,
                    },
                }
            )

        # Load general audit's computation to dict
        for data in self.general_audit_id.computation_ids:
            result["computation"].update(
                {
                    data.computation_item_id.code: {
                        "extrapolation": data.extrapolation_amount,
                        "interim": data.interim_amount,
                        "previous": data.previous_amount,
                        "end_period": data.home_amount,
                        "extrapolation_avg": data.extrapolation_avg_amount,
                        "interim_avg": data.interim_avg_amount,
                    },
                }
            )
        return result

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
