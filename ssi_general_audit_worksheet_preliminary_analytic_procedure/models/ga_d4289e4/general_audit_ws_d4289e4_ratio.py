# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval as eval  # pylint: disable=redefined-builtin


class GeneralAuditWSd4289e4Ratio(models.Model):
    _name = "general_audit_ws_d4289e4.ratio"
    _description = "Preliminary Analytic Procedure - Ratio Analysis (d4289e4) - Ratio"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_d4289e4",
        required=True,
        ondelete="cascade",
        help="Worksheet document that this ratio line belongs to.",
    )
    financial_ratio_id = fields.Many2one(
        string="Ratio",
        comodel_name="client_financial_ratio",
        required=True,
        help=(
            "Client financial ratio definition used to compute results. "
            "Its Python code is executed to derive values."
        ),
        ondelete="restrict",
    )
    category = fields.Selection(
        string="Category",
        related="financial_ratio_id.category",
        help="Ratio category derived from the selected ratio definition.",
    )
    current_amount = fields.Float(
        string="Current",
        related=False,
        store=True,
        help=(
            "Displayed current ratio result based on the worksheet Balance "
            "Type (Extrapolation or End Period)."
        ),
    )
    end_period_amount = fields.Float(
        string="End Period Amount",
        related=False,
        store=True,
        help="Ratio computed using End Period (actual) figures.",
    )
    extrapolation_amount = fields.Float(
        string="Extrapolation Amount",
        related=False,
        store=True,
        help="Ratio computed using Extrapolation (forecasted) figures.",
    )
    interim_amount = fields.Float(
        string="Interim Amount",
        related=False,
        store=True,
        help="Ratio computed using Interim figures.",
    )
    previous_amount = fields.Float(
        string="Previous Amount",
        related=False,
        store=True,
        help="Ratio computed using Previous period figures.",
    )
    audited_amount = fields.Float(
        string="Audited Amount",
        related=False,
        store=True,
        help="Audited Amount.",
    )
    industry_average = fields.Float(
        string="Industry Average",
        help="Industry benchmark for this ratio, for comparison purposes.",
    )
    analysis = fields.Char(
        string="Analysis",
        help=(
            "Short commentary or interpretation of the ratio movement or " "variance."
        ),
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
        audited_amount = kwargs.get("audited", 0.0)
        data = {
            "extrapolation_amount": extrapolation_amount,
            "interim_amount": interim_amount,
            "previous_amount": previous_amount,
            "end_period_amount": end_period_amount,
            "audited_amount": audited_amount,
        }
        return data

    def _recompute(self, additional_dict):
        self.ensure_one()
        extrapolation_amount = interim_amount = previous_amount = 0.0
        end_period_amount = audited_amount = 0.0
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
            audited_amount = localdict["result_audited"]
            additional_dict.update(
                {
                    self.financial_ratio_id.code: {
                        "extrapolation": extrapolation_amount,
                        "interim": interim_amount,
                        "previous": previous_amount,
                        "end_period": end_period_amount,
                        "audited": audited_amount,
                    }
                }
            )
        except Exception as e:
            msg_err = _(e)
            raise ValidationError(msg_err)

        data = self._prepare_ratio_data(
            extrapolation=extrapolation_amount,
            interim=interim_amount,
            previous=previous_amount,
            end_period=end_period_amount,
            audited=audited_amount,
        )
        if self.worksheet_id.base_amount_source == "extrapolation":
            data["current_amount"] = extrapolation_amount
        else:
            data["current_amount"] = end_period_amount
        self.write(data)
        return additional_dict
