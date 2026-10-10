# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWsB555eddEquityLine(models.Model):
    """Report Formatting Control (b555edd) - Equity Line.

    One equity component for one period on the Statement of Changes in
    Equity. The opening balance, profit, other comprehensive income
    (OCI) and closing balance are filled by the parent worksheet's
    Reload; the four owner transactions are typed in by the auditor.
    Whatever movement they do not explain stays visible as
    ``other_movement``, so the row always adds up to the closing
    balance.
    """

    _name = "general_audit_ws_b555edd.equity_line"
    _description = "Report Formatting Control (b555edd) - Equity Line"
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
    component_id = fields.Many2one(
        comodel_name="general_audit_ws_b555edd.equity_component",
        string="Component",
        required=True,
        ondelete="restrict",
        help="Equity component this line reports.",
    )
    period = fields.Selection(
        selection=[
            ("current", "Current Period"),
            ("previous", "Previous Period"),
        ],
        string="Period",
        required=True,
        default="current",
        help="Period the amounts belong to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        help="Display order, copied from the component.",
    )
    opening_balance = fields.Monetary(
        string="Opening Balance",
        currency_field="currency_id",
        readonly=True,
        help="Balance of the component at the start of the period.",
    )
    profit = fields.Monetary(
        string="Profit",
        currency_field="currency_id",
        readonly=True,
        help="Profit after tax of the period, if the component receives it.",
    )
    oci = fields.Monetary(
        string="OCI",
        currency_field="currency_id",
        readonly=True,
        help="Other comprehensive income of the period, if received.",
    )
    issuance = fields.Monetary(
        string="Issuance of Shares",
        currency_field="currency_id",
        help="Shares issued to the owners; typed in by the auditor.",
    )
    treasury = fields.Monetary(
        string="Treasury Shares",
        currency_field="currency_id",
        help="Treasury share transactions; typed in by the auditor.",
    )
    reserve = fields.Monetary(
        string="Addition of Reserves",
        currency_field="currency_id",
        help="Appropriation to reserves; typed in by the auditor.",
    )
    dividend = fields.Monetary(
        string="Dividends",
        currency_field="currency_id",
        help="Dividends distributed; typed in by the auditor.",
    )
    closing_balance = fields.Monetary(
        string="Closing Balance",
        currency_field="currency_id",
        readonly=True,
        help="Balance of the component at the end of the period.",
    )
    other_movement = fields.Monetary(
        string="Other Movement",
        currency_field="currency_id",
        compute="_compute_other_movement",
        store=True,
        help=(
            "Movement the profit, OCI and owner transactions do not "
            "explain. Zero when the row adds up."
        ),
    )

    @api.depends(
        "opening_balance",
        "profit",
        "oci",
        "issuance",
        "treasury",
        "reserve",
        "dividend",
        "closing_balance",
    )
    def _compute_other_movement(self):
        """Compute the movement left unexplained on each line.

        :return: None
        """
        for record in self:
            record.other_movement = record.closing_balance - (
                record.opening_balance
                + record.profit
                + record.oci
                + record.issuance
                + record.treasury
                + record.reserve
                + record.dividend
            )
