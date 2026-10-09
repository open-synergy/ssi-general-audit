# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsB555eddCashflowLine(models.Model):
    """Report Formatting Control (b555edd) - Cash Flow Line.

    One cash flow item for one period on the Statement of Cash Flows.
    Reload fills the computed amounts and the summary rows; only the
    manual rows can be typed in, and editing one refreshes the summary
    rows of the same period, so the cash difference always reflects the
    current figures.
    """

    _name = "general_audit_ws_b555edd.cashflow_line"
    _description = "Report Formatting Control (b555edd) - Cash Flow Line"
    _order = "period, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_b555edd",
        string="# Worksheet",
        required=True,
        ondelete="cascade",
        help="Report Formatting Control worksheet this line belongs to.",
    )
    state = fields.Selection(
        related="worksheet_id.state",
        string="Status",
        help="Status of the parent worksheet; decides what can be edited.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="worksheet_id.general_audit_id.currency_id",
        store=True,
        help="Currency of the amounts; taken from the General Audit.",
    )
    item_id = fields.Many2one(
        comodel_name="general_audit_ws_b555edd.cashflow_item",
        string="Item",
        required=True,
        ondelete="restrict",
        help="Cash flow item this line reports.",
    )
    section = fields.Selection(
        related="item_id.section",
        string="Section",
        store=True,
        help="Part of the statement the line belongs to.",
    )
    calc_type = fields.Selection(
        related="item_id.calc_type",
        string="Calculation",
        store=True,
        help="How the amount is obtained.",
    )
    period = fields.Selection(
        selection=[
            ("current", "Current Period"),
            ("previous", "Previous Period"),
        ],
        string="Period",
        required=True,
        default="current",
        help="Period the amount belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        help="Display order, copied from the item.",
    )
    amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
        help="Cash inflow (positive) or outflow (negative).",
    )

    def write(self, vals):
        """Refresh the summary rows after a manual amount is typed in.

        :param dict vals: values to write
        :return: result of the parent ``write``
        :rtype: bool
        """
        result = super().write(vals)
        if "amount" in vals:
            manual = self.filtered(lambda r: r.calc_type == "manual")
            for worksheet in manual.mapped("worksheet_id"):
                worksheet._refresh_cashflow_totals()
        return result
