# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ClientAdjustmentEntryDetail(models.Model):
    _name = "client_adjustment_entry.detail"
    _description = "Accountant Client Adjustment Entry Detail"

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
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="entry_id.currency_id",
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
