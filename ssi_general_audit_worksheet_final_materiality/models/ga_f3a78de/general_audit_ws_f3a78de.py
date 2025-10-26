# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSf3a78de(models.Model):
    _name = "general_audit_ws_f3a78de"
    _description = "Final Analytical Procedures (f3a78de) - " "Ratio Analysis"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_final_materiality." "worksheet_type_f3a78de"
    )

    ws_d4289e4_id = fields.Many2one(
        string="# Preliminary Analytic Procedure - Ratio Analysis",
        comodel_name="general_audit_ws_d4289e4",
        help=(
            "Link to the Preliminary Analytic Procedure - Ratio Analysis "
            "worksheet used as basis for this Final Analytical Procedures "
            "worksheet."
        ),
        readonly=True,
        required=False,
        ondelete="restrict",
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    ratio_ids = fields.One2many(
        string="Ratios",
        comodel_name="general_audit_ws_f3a78de.ratio",
        inverse_name="worksheet_id",
        help="All ratio lines computed for this worksheet.",
    )

    def action_reload_ratio(self):
        for record in self:
            record._reload_ratio()
            record._recompute_computation()

    def action_compute_ratio(self):
        for record in self:
            record._recompute_computation()

    def _reload_ratio(self):
        self.ensure_one()
        all_ratios = self.env["client_financial_ratio"].search([])
        existing_ratios = self.ratio_ids.mapped("financial_ratio_id")

        to_be_added = all_ratios - existing_ratios
        to_be_removed = existing_ratios - all_ratios

        for ratio in to_be_removed:
            line = self.ratio_ids.filtered(lambda r: r.financial_ratio_id == ratio)
            line.unlink()

        for ratio in to_be_added:
            criteria = [
                ("worksheet_id", "=", self.ws_d4289e4_id.id),
                ("financial_ratio_id", "=", ratio.id),
            ]
            prelim_detail = False
            prelim_details = self.env["general_audit_ws_d4289e4.ratio"].search(criteria)
            if len(prelim_details) > 0:
                prelim_detail = prelim_details[0]

            self.env["general_audit_ws_f3a78de.ratio"].create(
                {
                    "worksheet_id": self.id,
                    "financial_ratio_id": ratio.id,
                    "industry_average": prelim_detail
                    and prelim_detail.industry_average
                    or 0.0,
                    "analysis": prelim_detail and prelim_detail.analysis or False,
                }
            )

    @ssi_decorator.post_confirm_action()
    def _recompute_computation(self):
        self.ensure_one()
        additional_dict = self._get_additional_dict()
        for computation in self.ratio_ids:
            additionaldict = computation._recompute(additional_dict)
            additional_dict = additionaldict

        self.general_audit_id._recompute_computation()
        self.general_audit_id._recompute_extrapolation_computation()
        self.general_audit_id._recompute_audited_computation()

    def _get_additional_dict(self):
        self.ensure_one()
        result = {"account_type": {}, "account_group": {}, "computation": {}}
        # Load general audit's standard detail to dict
        for data in self.general_audit_id.standard_detail_ids:
            result["account_type"].update(
                {
                    data.type_id.code: {
                        "extrapolation": data.extrapolation_balance,
                        "extrapolation_avg": data.extrapolation_avg,
                        "end_period": data.home_statement_balance,
                        "end_period_avg": data.home_statement_avg,
                        "interim": data.interim_balance,
                        "interim_avg": data.interim_avg,
                        "previous": data.previous_balance,
                        "audited": data.audited_balance,
                        "audited_avg": data.audited_avg,
                    },
                }
            )

        # Load general audit's group summary to dict
        for data in self.general_audit_id.group_detail_ids:
            result["account_group"].update(
                {
                    data.group_id.code: {
                        "extrapolation": data.extrapolation_balance,
                        "extrapolation_avg": data.extrapolation_avg,
                        "end_period": data.home_statement_balance,
                        "end_period_avg": data.home_statement_avg,
                        "interim": data.interim_balance,
                        "previous": data.previous_balance,
                        "interim_avg": data.interim_avg,
                        "audited": data.audited_balance,
                        "audited_avg": data.audited_avg,
                    },
                }
            )

        # Load general audit's computation to dict
        for data in self.general_audit_id.computation_ids:
            result["computation"].update(
                {
                    data.computation_item_id.code: {
                        "extrapolation": data.extrapolation_amount,
                        "extrapolation_avg": data.extrapolation_avg_amount,
                        "end_period": data.home_amount,
                        "end_period_avg": data.home_avg_amount,
                        "interim": data.interim_amount,
                        "interim_avg": data.interim_avg_amount,
                        "previous": data.previous_amount,
                        "audited": data.audited_amount,
                        "audited_avg": data.audited_avg_amount,
                    },
                }
            )
        return result
