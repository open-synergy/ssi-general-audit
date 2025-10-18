# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ClientAccountType(models.Model):
    _name = "client_account_type"
    _inherit = ["mixin.master_data"]
    _description = "Client Account Type"
    _order = "sequence, id"
    _show_code_on_display_name = True

    group_id = fields.Many2one(
        string="Client Account Group",
        comodel_name="client_account_group",
        required=True,
        help="Account group that this type belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Ordering of the account type.",
    )
    normal_balance = fields.Selection(
        string="Normal Balance",
        selection=[
            ("dr", "Debit"),
            ("cr", "Credit"),
        ],
        required=True,
        default="dr",
        help="Default normal balance for accounts of this type.",
    )
    analytic_procedure_computation_item_id = fields.Many2one(
        string="Computation Item for Analytic Procedure",
        comodel_name="trial_balance_computation_item",
        help="Computation item used to calculate analytic procedure for this type.",
    )
    python_code = fields.Text(
        string="Python Code",
        required=True,
        default="result = document.balance",
        help=(
            "Python code to compute the balance for this type. The variable "
            "'document' refers to the trial balance line."
        ),
    )
