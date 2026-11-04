# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWsB555eddDetail(models.Model):
    """Report Formatting Control (b555edd) - one standard account type line.

    Mirrors one ``general_audit.standard_detail`` of the parent General
    Audit: the account type, its group and the audited balances of the
    current and the previous period. Lines are created by the parent
    worksheet's ``action_reload_account`` and are never typed in.
    """

    _name = "general_audit_ws_b555edd.detail"
    _description = "Report Formatting Control (b555edd) - Detail"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_b555edd",
        string="# Worksheet",
        required=True,
        ondelete="cascade",
        help="Report Formatting Control worksheet this line belongs to.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="worksheet_id.general_audit_id.currency_id",
        store=True,
        help="Currency of the amounts; taken from the General Audit.",
    )
    standard_detail_id = fields.Many2one(
        string="# Standard Detail",
        comodel_name="general_audit.standard_detail",
        required=True,
        ondelete="restrict",
        help="Standard account type line of the General Audit.",
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        related="standard_detail_id.type_id",
        store=True,
        readonly=True,
        help="Standard account type reported on this line.",
    )
    group_id = fields.Many2one(
        string="Account Group",
        comodel_name="client_account_group",
        related="standard_detail_id.type_id.group_id",
        store=True,
        readonly=True,
        help="Account group; decides which statement tab shows this line.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        help="Display order: account group sequence, then type sequence.",
    )
    current_balance = fields.Monetary(
        string="Current Balance",
        compute="_compute_balance",
        store=True,
        readonly=True,
        compute_sudo=True,
        currency_field="currency_id",
        help="Audited balance of the current period. The unappropriated "
        "retained earnings line also carries the profit of the period.",
    )
    previous_balance = fields.Monetary(
        string="Previous Balance",
        compute="_compute_balance",
        store=True,
        readonly=True,
        compute_sudo=True,
        currency_field="currency_id",
        help="Balance of the previous period. The unappropriated retained "
        "earnings line also carries the profit of that period.",
    )

    @api.depends(
        "standard_detail_id.audited_balance",
        "standard_detail_id.previous_balance",
        "standard_detail_id.type_id",
        "worksheet_id.general_audit_id.standard_detail_ids.audited_balance",
        "worksheet_id.general_audit_id.standard_detail_ids.previous_balance",
        "worksheet_id.general_audit_id.standard_detail_ids.type_id",
        "worksheet_id.general_audit_id.closing_line_ids.account_id",
        "worksheet_id.general_audit_id.closing_line_ids.account_type_id",
        "worksheet_id.general_audit_id.closing_line_ids.debit",
        "worksheet_id.general_audit_id.closing_line_ids.credit",
        "worksheet_id.general_audit_id.previous_closing_line_ids.account_id",
        "worksheet_id.general_audit_id.previous_closing_line_ids.account_type_id",
        "worksheet_id.general_audit_id.previous_closing_line_ids.debit",
        "worksheet_id.general_audit_id.previous_closing_line_ids.credit",
    )
    def _compute_balance(self):
        """Fill the balances of both periods from the standard detail.

        Lines of other account types show the audited balance as is. The
        unappropriated retained earnings line adds the
        ``profit_after_tax`` total of the same period, because the profit
        is not closed into equity in the trial balance.

        Once the closing lines of the General Audit are generated, the
        closing is the only source: the current balance of each
        destination account type adds its closing amount and the profit
        is no longer added, so it is not counted twice. The previous
        period follows the same rule with the previous closing lines
        of the General Audit.

        :return: None
        """
        receiver = self._get_profit_receiver_type()
        for record in self:
            detail = record.standard_detail_id
            current = detail.audited_balance
            previous = detail.previous_balance
            closing_lines = (
                record.worksheet_id.general_audit_id.closing_line_ids.filtered(
                    lambda line: not line.account_id
                )
            )
            previous_closing_lines = (
                record.worksheet_id.general_audit_id.previous_closing_line_ids.filtered(
                    lambda line: not line.account_id
                )
            )
            if closing_lines:
                current += record._get_closing_amount(closing_lines, detail.type_id)
            if previous_closing_lines:
                previous += record._get_closing_amount(
                    previous_closing_lines, detail.type_id
                )
            if receiver and detail.type_id == receiver:
                worksheet = record.worksheet_id
                details = worksheet.general_audit_id.standard_detail_ids
                if not closing_lines:
                    current += worksheet._get_formula_total(
                        "profit_after_tax", "audited_balance", details
                    )
                if not previous_closing_lines:
                    previous += worksheet._get_formula_total(
                        "profit_after_tax", "previous_balance", details
                    )
            record.current_balance = current
            record.previous_balance = previous

    @api.model
    def _get_closing_amount(self, closing_lines, account_type):
        """Get the closing amount that lands in an account type.

        Each destination line of the type is signed on the normal
        balance side of the type, like ``audited_balance``.

        :param closing_lines: destination ``general_audit.closing_line``
            records of the General Audit (lines without an account)
        :param account_type: ``client_account_type`` record of the line
        :return: closing amount of the type, zero when no closing line
            targets it
        :rtype: float
        """
        result = 0.0
        for line in closing_lines.filtered(
            lambda line: line.account_type_id == account_type
        ):
            if account_type.normal_balance == "cr":
                result += line.credit - line.debit
            else:
                result += line.debit - line.credit
        return result

    @api.model
    def _get_profit_receiver_type(self):
        """Return the account type that receives the profit of the period.

        Extension point: override to widen the account types that carry
        the profit.

        :return: the unappropriated retained earnings account type, or an
            empty recordset when the master data is missing
        :rtype: recordset
        """
        return (
            self.env.ref(
                "ssi_general_audit.client_account_type_44_a5c4f192",
                raise_if_not_found=False,
            )
            or self.env["client_account_type"]
        )
