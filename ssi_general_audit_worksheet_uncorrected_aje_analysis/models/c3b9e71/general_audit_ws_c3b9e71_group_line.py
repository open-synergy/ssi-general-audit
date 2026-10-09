# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWsC3b9e71GroupLine(models.Model):
    """Account group line of the Uncorrected AJE Analysis worksheet.

    One line per account group of the audit. It holds the audited balance
    of the group, the amount of uncorrected misstatement posted to it, and
    the share of that amount over the balance and over Performance
    Materiality.
    """

    _name = "general_audit_ws_c3b9e71.group_line"
    _description = "Uncorrected AJE Analysis (c3b9e71) - Group Line"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_c3b9e71",
        required=True,
        ondelete="cascade",
        help="Uncorrected AJE Analysis worksheet that owns this line.",
    )
    group_id = fields.Many2one(
        string="Account Group",
        comodel_name="client_account_group",
        required=True,
        ondelete="restrict",
        help="Account group analysed by this line.",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="group_id.sequence",
        store=True,
        help="Display order inherited from the account group.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="worksheet_id.currency_id",
        store=True,
        help="Currency of the amounts, inherited from the worksheet.",
    )
    balance = fields.Monetary(
        string="Audited Balance",
        currency_field="currency_id",
        help="Sum of the balance of the Specific Materiality mapping lines "
        "that belong to this account group.",
    )
    uncorrected_amount = fields.Monetary(
        string="Uncorrected Misstatement",
        currency_field="currency_id",
        help="Net amount of the uncorrected adjustment entries posted to "
        "this group, in the direction of its normal balance.",
    )
    pct_of_balance = fields.Float(
        string="% of Group Balance",
        compute="_compute_pct",
        store=True,
        compute_sudo=True,
        help="Uncorrected misstatement divided by the audited balance. "
        "Zero when the balance is zero.",
    )
    pct_of_pm = fields.Float(
        string="% of Performance Materiality",
        compute="_compute_pct",
        store=True,
        compute_sudo=True,
        help="Uncorrected misstatement divided by Performance Materiality. "
        "Zero when Performance Materiality is zero.",
    )

    @api.depends(
        "balance",
        "uncorrected_amount",
        "worksheet_id.performance_materiality",
    )
    def _compute_pct(self):
        """Compute both percentages, using zero when the divisor is zero.

        :return: ``None``
        """
        for record in self:
            pct_of_balance = pct_of_pm = 0.0
            if record.balance:
                pct_of_balance = record.uncorrected_amount / record.balance
            pm = record.worksheet_id.performance_materiality
            if pm:
                pct_of_pm = record.uncorrected_amount / pm
            record.pct_of_balance = pct_of_balance
            record.pct_of_pm = pct_of_pm
