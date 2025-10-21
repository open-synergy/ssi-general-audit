# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class TrialBalanceComputationItem(models.Model):
    _name = "trial_balance_computation_item"
    _inherit = "trial_balance_computation_item"

    going_concern_ok = fields.Boolean(
        string="Use in Going Concern Indicator Computation",
        default=False,
        help="Indicates whether this item is used in the going concern indicator computation.",
    )
