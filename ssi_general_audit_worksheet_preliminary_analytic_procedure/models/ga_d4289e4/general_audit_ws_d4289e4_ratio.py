# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models
from odoo.tools.safe_eval import safe_eval as eval  # pylint: disable=redefined-builtin


class GeneralAuditWSd4289e4Ratio(models.Model):
    _name = "general_audit_ws_d4289e4.ratio"
    _description = "Preliminary Analytic Procedure - Ratio Analysis (d4289e4) - Ratio"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_d4289e4",
        required=True,
        ondelete="cascade",
    )
    financial_ratio_id = fields.Many2one(
        string="Ratio",
        comodel_name="client_financial_ratio",
        required=True,
    )
    category = fields.Selection(
        string="Category",
        related="financial_ratio_id.category",
    )
    current_amount = fields.Float(
        string="Curr. Amount",
        related=False,
        store=True,
    )
    end_period_amount = fields.Float(
        string="End Period Amount",
        related=False,
        store=True,
    )
    extrapolation_amount = fields.Float(
        string="Extrapolation Amount",
        related=False,
        store=True,
    )
    interim_amount = fields.Float(
        string="Interim Amount",
        related=False,
        store=True,
    )
    previous_amount = fields.Float(
        string="Previous Amount",
        related=False,
        store=True,
    )
    industry_average = fields.Float(
        string="Industry Average",
    )
    analysis = fields.Char(
        string="Analysis",
    )

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _prepare_ratio_data(self, **kwargs):
        extrapolation_amount = kwargs.get("extrapolation", 0.0)
        interim_amount = kwargs.get("interim", 0.0)
        previous_amount = kwargs.get("previous", 0.0)
        end_period_amount = kwargs.get("end_period", 0.0)
        data = {
            "extrapolation_amount": extrapolation_amount,
            "interim_amount": interim_amount,
            "previous_amount": previous_amount,
            "end_period_amount": end_period_amount,
        }
        return data

    def _recompute(self, additional_dict):
        self.ensure_one()
        python_code = self.financial_ratio_id.python_code

        localdict = self._get_localdict()
        localdict.update(additional_dict)
        try:
            eval(
                python_code,
                localdict,
                mode="exec",
                nocopy=True,
            )
            extrapolation_amount = localdict["result_extrapolation"]
            interim_amount = localdict["result_interim"]
            previous_amount = localdict["result_previous"]
            end_period_amount = localdict["result_end_period"]
            additional_dict.update(
                {
                    self.financial_ratio_id.code: {
                        "extrapolation": extrapolation_amount,
                        "interim": interim_amount,
                        "previous": previous_amount,
                        "end_period": end_period_amount,
                    }
                }
            )
        except Exception:
            extrapolation_amount = interim_amount = previous_amount = 0.0
            end_period_amount = 0.0

        data = self._prepare_ratio_data(
            extrapolation=extrapolation_amount,
            interim=interim_amount,
            previous=previous_amount,
            end_period=end_period_amount,
        )
        if self.worksheet_id.base_amount_source == "extrapolation":
            data["current_amount"] = extrapolation_amount
        else:
            data["current_amount"] = end_period_amount
        self.write(data)
        return additional_dict
