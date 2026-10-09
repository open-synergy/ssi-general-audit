# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ClientAdjustmentEntryDetail(models.Model):
    """
    Baris Debit/Kredit Jurnal Penyesuaian Audit.

    Satu baris debit atau kredit dalam ``client_adjustment_entry``. Setiap
    baris mengidentifikasi akun klien yang terdampak penyesuaian beserta
    jumlah debit atau kreditnya. Baris ini juga terhubung ke baris detail
    general audit (``general_audit.detail``) untuk memudahkan penelusuran
    dampak penyesuaian terhadap saldo akun yang sedang diaudit.
    """

    _name = "client_adjustment_entry.detail"
    _description = "Accountant Client Adjustment Entry Detail"
    _order = "entry_id, id"

    aje_code = fields.Char(
        string="AJE Code",
        help="Original AJE/CAJE code from the client's source document, "
        "for traceability only. Free text, not validated against any "
        "record.",
    )
    name = fields.Char(
        string="Description",
        required=True,
        help="Free-text description of the adjustment line.",
    )
    entry_id = fields.Many2one(
        string="# Adjustment Entry",
        comodel_name="client_adjustment_entry",
        required=True,
        ondelete="cascade",
        help="Parent adjustment entry this line belongs to.",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="client_account",
        required=True,
        ondelete="restrict",
        help="Client account to debit or credit.",
    )
    detail_id = fields.Many2one(
        string="# General Audit Detail",
        comodel_name="general_audit.detail",
        help="Link to the related general audit detail, if applicable.",
        compute="_compute_detail_id",
        compute_sudo=True,
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="entry_id.currency_id",
        compute_sudo=True,
        store=True,
        help="Currency of amounts; inherited from the parent entry.",
    )
    debit = fields.Monetary(
        string="Debit",
        required=True,
        default=0.0,
        currency_field="currency_id",
        help="Amount to debit. Use 0 if none.",
    )
    credit = fields.Monetary(
        string="Credit",
        required=True,
        default=0.0,
        currency_field="currency_id",
        help="Amount to credit. Use 0 if none.",
    )
    corrected = fields.Boolean(
        string="Corrected",
        related="entry_id.corrected",
        store=False,
        readonly=True,
        help="Whether the parent adjustment entry is corrected by the client.",
    )
    impact_asset = fields.Monetary(
        string="Asset",
        compute="_compute_impact",
        store=False,
        compute_sudo=True,
        currency_field="currency_id",
        help="Impact on assets: debit minus credit, for accounts whose "
        "group has the Asset report category.",
    )
    impact_liability = fields.Monetary(
        string="Liabilities",
        compute="_compute_impact",
        store=False,
        compute_sudo=True,
        currency_field="currency_id",
        help="Impact on liabilities: credit minus debit, for accounts whose "
        "group has the Liability report category.",
    )
    impact_equity = fields.Monetary(
        string="Equities",
        compute="_compute_impact",
        store=False,
        compute_sudo=True,
        currency_field="currency_id",
        help="Impact on equity: credit minus debit, for accounts whose "
        "group has the Equity report category.",
    )
    impact_profit_loss = fields.Monetary(
        string="Profit & Loss",
        compute="_compute_impact",
        store=False,
        compute_sudo=True,
        currency_field="currency_id",
        help="Impact on profit and loss: credit minus debit, for accounts "
        "whose group has the Profit & Loss report category.",
    )

    @api.depends(
        "debit",
        "credit",
        "account_id.type_id.group_id.report_category",
    )
    def _compute_impact(self):
        """Split the line amount into the four report category impacts.

        Assets take debit minus credit; liabilities, equity and profit
        and loss take credit minus debit. A line whose account group has
        no report category contributes zero to every impact column.

        :return: ``None``
        """
        for record in self:
            category = record.account_id.type_id.group_id.report_category
            result = {
                "asset": 0.0,
                "liability": 0.0,
                "equity": 0.0,
                "profit_loss": 0.0,
            }
            if category == "asset":
                result["asset"] = record.debit - record.credit
            elif category:
                result[category] = record.credit - record.debit
            record.impact_asset = result["asset"]
            record.impact_liability = result["liability"]
            record.impact_equity = result["equity"]
            record.impact_profit_loss = result["profit_loss"]

    @api.depends(
        "account_id",
        "entry_id.general_audit_id",
    )
    def _compute_detail_id(self):
        for record in self:
            if record.account_id and record.entry_id.general_audit_id:
                Detail = self.env["general_audit.detail"]
                criteria = [
                    ("general_audit_id", "=", record.entry_id.general_audit_id.id),
                    ("account_id", "=", record.account_id.id),
                ]
                details = Detail.search(criteria, limit=1)
                if details:
                    record.detail_id = details[0]
                else:
                    record.detail_id = False

    @api.constrains(
        "credit",
    )
    def constrains_credit(self):
        for record in self:
            if record.credit:
                if record.credit < 0:
                    msg = _("Credit has to be greater or equal than 0")
                    raise UserError(msg)

    @api.constrains(
        "debit",
    )
    def constrains_debit(self):
        for record in self:
            if record.debit:
                if record.debit < 0:
                    msg = _("Debit has to be greater or equal than 0")
                    raise UserError(msg)
