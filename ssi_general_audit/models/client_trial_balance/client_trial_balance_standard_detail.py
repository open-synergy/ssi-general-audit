# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import api, fields, models


class ClientTrialBalanceStandardDetail(models.Model):
    _name = "client_trial_balance.standard_detail"
    _description = "Accountant Client Trial Balance Standard Detail"
    _order = "sequence, trial_balance_id, id"

    @api.depends(
        "trial_balance_id",
        "trial_balance_id.date_start",
        "trial_balance_id.date_end",
        "trial_balance_id.previous_date_start",
        "trial_balance_id.previous_date_end",
        "trial_balance_id.interim_date_start",
        "trial_balance_id.interim_date_end",
        "type_id",
        "trial_balance_id.detail_ids",
        "trial_balance_id.detail_ids.type_id",
        "trial_balance_id.detail_ids.balance",
        "trial_balance_id.detail_ids.opening_balance",
        "trial_balance_id.detail_ids.debit",
        "trial_balance_id.detail_ids.credit",
    )
    def _compute_balance(self):
        obj_detail = self.env["client_trial_balance.detail"]
        for document in self:
            balance = opening_balance = debit = credit = 0.0
            criteria = [
                ("trial_balance_id", "=", document.trial_balance_id.id),
                ("type_id", "=", document.type_id.id),
            ]
            for detail in obj_detail.search(criteria):
                opening_balance += detail.opening_balance
                debit += detail.debit
                credit += detail.credit
                balance += detail.balance

            document.balance = balance
            document.opening_balance = opening_balance
            document.debit = debit
            document.credit = credit

    trial_balance_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="client_trial_balance",
        required=True,
        ondelete="cascade",
        help="Parent Trial Balance document.",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="general_audit.standard_detail",
        required=True,
        ondelete="restrict",
        help="Standard account type line defined in the General Audit.",
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        related="standard_detail_id.type_id",
        store=True,
        help="Account type derived from the linked standard detail.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="standard_detail_id.currency_id",
        store=True,
        help="Currency of amounts; inherited from the standard detail.",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="standard_detail_id.sequence",
        store=True,
        help="Ordering number from the standard detail.",
    )
    opening_balance = fields.Monetary(
        string="Opening Balance",
        compute="_compute_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Total opening balance for the type (sum of details).",
    )
    debit = fields.Monetary(
        string="Debit",
        compute="_compute_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Total debit during the period for this type.",
    )
    credit = fields.Monetary(
        string="Credit",
        compute="_compute_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Total credit during the period for this type.",
    )
    balance = fields.Monetary(
        string="Balance",
        compute="_compute_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Net balance for this standard account type.",
    )
