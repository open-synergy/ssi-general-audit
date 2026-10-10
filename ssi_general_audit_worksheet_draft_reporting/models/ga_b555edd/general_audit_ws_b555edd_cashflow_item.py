# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsB555eddCashflowItem(models.Model):
    """Report Formatting Control (b555edd) - Cash Flow Item.

    Master data of one row of the Statement of Cash Flows (indirect
    method). ``calc_type`` says how Reload computes the amount from the
    balances of the mapped standard account types; ``section`` says
    where the row belongs. Seeded by ``data/master``; one global set
    serves every General Audit.
    """

    _name = "general_audit_ws_b555edd.cashflow_item"
    _description = "Report Formatting Control (b555edd) - Cash Flow Item"
    _order = "sequence, id"

    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the row shown on the statement.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        help="Display and calculation order of the row.",
    )
    section = fields.Selection(
        selection=[
            ("operating_adjustment", "Operating - Adjustments"),
            ("working_capital", "Operating - Working Capital"),
            ("operating_other", "Operating - Interest and Tax"),
            ("investing", "Investing"),
            ("financing", "Financing"),
            ("summary", "Summary"),
        ],
        string="Section",
        required=True,
        help="Part of the statement the row belongs to.",
    )
    calc_type = fields.Selection(
        selection=[
            ("profit_before_tax", "Profit Before Tax"),
            ("pl_amount", "Profit or Loss Amount"),
            ("balance_change", "Balance Change"),
            ("capex", "Fixed Asset Acquisition"),
            ("manual", "Manual Entry"),
            ("operating_total", "Total Operating Cash Flow"),
            ("investing_total", "Total Investing Cash Flow"),
            ("financing_total", "Total Financing Cash Flow"),
            ("net_change", "Net Change in Cash"),
            ("cash_opening", "Opening Cash"),
            ("cash_closing_computed", "Closing Cash (Computed)"),
            ("cash_closing_tb", "Closing Cash (Trial Balance)"),
            ("cash_difference", "Cash Difference"),
        ],
        string="Calculation",
        required=True,
        help=(
            "How the amount is obtained. Profit or Loss Amount takes the "
            "period balance of the mapped types. Balance Change takes the "
            "change of their balance: an increase of an asset is a cash "
            "outflow, an increase of a liability or equity is a cash "
            "inflow. Fixed Asset Acquisition is the change of the mapped "
            "asset types plus the period expense of the reference types. "
            "Manual rows are typed in by the auditor."
        ),
    )
    sign = fields.Selection(
        selection=[("add", "+"), ("subtract", "-")],
        string="Sign",
        required=True,
        default="add",
        help="Whether the computed amount is added or subtracted.",
    )
    type_ids = fields.Many2many(
        comodel_name="client_account_type",
        relation="ga_b555edd_cashflow_item_type_rel",
        column1="item_id",
        column2="type_id",
        string="Account Types",
        help="Standard account types the row is computed from.",
    )
    reference_type_ids = fields.Many2many(
        comodel_name="client_account_type",
        relation="ga_b555edd_cashflow_item_reftype_rel",
        column1="item_id",
        column2="type_id",
        string="Reference Account Types",
        help=(
            "Account types whose period balance is added to the change of "
            "the mapped types, for example depreciation for asset "
            "acquisitions."
        ),
    )
