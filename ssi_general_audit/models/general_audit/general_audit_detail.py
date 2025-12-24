# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import api, fields, models


class GeneralAuditDetail(models.Model):
    _name = "general_audit.detail"
    _description = "Accountant General Audit Detail"
    _order = "general_audit_id, type_id, account_id, id"
    _rec_name = "account_id"

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        required=True,
        ondelete="cascade",
        help="General Audit document that owns this detail line.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        compute_sudo=True,
        store=True,
        help="Currency used for amounts; inherited from the General Audit.",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="client_account",
        required=True,
        ondelete="restrict",
        help="Client account being tracked in the audit.",
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        related="account_id.type_id",
        compute_sudo=True,
        store=True,
        readonly=False,
        help="Account type derived from the selected client account.",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="account_id.sequence",
        compute_sudo=True,
        store=True,
        help="Ordering number inherited from the client account.",
    )

    # Link to Trial Balance Detail
    home_line_id = fields.Many2one(
        string="End Period TB Standard Line",
        comodel_name="client_trial_balance.detail",
        readonly=True,
        compute="_compute_detail",
        compute_sudo=True,
        store=True,
        help="Linked trial balance detail for the end period.",
    )
    interim_line_id = fields.Many2one(
        string="Interim TB Standard Line",
        comodel_name="client_trial_balance.detail",
        readonly=True,
        compute="_compute_detail",
        compute_sudo=True,
        store=True,
        help="Linked trial balance detail for the interim period.",
    )
    previous_line_id = fields.Many2one(
        string="Previous TB Standard Line",
        comodel_name="client_trial_balance.detail",
        readonly=True,
        compute="_compute_detail",
        compute_sudo=True,
        store=True,
        help="Linked trial balance detail for the previous period.",
    )

    # Balance
    home_statement_opening_balance = fields.Monetary(
        string="End Period Opening Balance",
        related="home_line_id.opening_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Opening balance from the end period trial balance.",
    )
    home_statement_balance = fields.Monetary(
        string="End Period Balance",
        related="home_line_id.balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Net balance from the end period trial balance.",
    )
    interim_opening_balance = fields.Monetary(
        string="Interim Opening Balance",
        related="interim_line_id.opening_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Opening balance from the interim trial balance.",
    )
    interim_balance = fields.Monetary(
        string="Interim Balance",
        related="interim_line_id.balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Net balance from the interim trial balance.",
    )
    previous_opening_balance = fields.Monetary(
        string="Previous Opening Balance",
        related="previous_line_id.opening_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Opening balance from the previous period trial balance.",
    )
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="previous_line_id.balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Net balance from the previous period trial balance.",
    )

    @api.depends(
        "general_audit_id",
        "account_id",
        "general_audit_id.home_trial_balance_id",
        "general_audit_id.interim_trial_balance_id",
        "general_audit_id.previous_trial_balance_id",
        "general_audit_id.home_trial_balance_id.state",
        "general_audit_id.interim_trial_balance_id.state",
        "general_audit_id.previous_trial_balance_id.state",
    )
    def _compute_detail(self):
        Detail = self.env["client_trial_balance.detail"]
        for record in self:
            home_result = interim_result = previous_result = False
            criteria = [
                ("account_id", "=", record.account_id.id),
            ]
            if record.general_audit_id.home_trial_balance_id:
                criteria_home = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.home_trial_balance_id.id,
                    )
                ]
                home_results = Detail.search(criteria_home)
                if len(home_results) > 0:
                    home_result = home_results[0]

            if record.general_audit_id.interim_trial_balance_id:
                criteria_interim = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.interim_trial_balance_id.id,
                    )
                ]
                interim_results = Detail.search(criteria_interim)
                if len(interim_results) > 0:
                    interim_result = interim_results[0]

            if record.general_audit_id.previous_trial_balance_id:
                criteria_previous = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.previous_trial_balance_id.id,
                    )
                ]
                previous_results = Detail.search(criteria_previous)
                if len(previous_results) > 0:
                    previous_result = previous_results[0]

            record.home_line_id = home_result
            record.interim_line_id = interim_result
            record.previous_line_id = previous_result

    @api.depends(
        "general_audit_id.adjustment_entry_ids",
        "general_audit_id.adjustment_entry_ids.state",
        "general_audit_id.adjustment_entry_ids.detail_ids.account_id",
        "general_audit_id.adjustment_entry_ids.detail_ids.debit",
        "general_audit_id.adjustment_entry_ids.detail_ids.credit",
    )
    def _compute_adjustment_id(self):
        StandardAdjustment = self.env["general_audit.account_adjustment"]
        for record in self:
            result = False
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("account_id", "=", record.account_id.id),
            ]
            standard_adjustments = StandardAdjustment.search(criteria)
            if len(standard_adjustments) > 0:
                result = standard_adjustments[0]
            record.adjustment_id = result

    adjustment_id = fields.Many2one(
        string="Adjustment",
        comodel_name="general_audit.account_adjustment",
        readonly=True,
        compute="_compute_adjustment_id",
        compute_sudo=True,
        store=True,
        help="Aggregated adjustments affecting this account.",
    )

    adjustment_debit = fields.Monetary(
        string="Adjustment Debit",
        related="adjustment_id.debit",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Total debit adjustments for this account.",
    )
    adjustment_credit = fields.Monetary(
        string="Adjustment Credit",
        related="adjustment_id.credit",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Total credit adjustments for this account.",
    )

    adjustment_line_ids = fields.One2many(
        string="Adjustment Lines",
        comodel_name="client_adjustment_entry.detail",
        inverse_name="detail_id",
        help="Detailed adjustment entries linked to this audit detail.",
    )
    adjustment_ids = fields.Many2many(
        string="Adjustments",
        comodel_name="client_adjustment_entry",
        relation="rel_general_audit_detail_2_client_adjustment_entry",
        column1="detail_id",
        column2="client_adjustment_entry_id",
        compute="_compute_adjustment_ids",
        compute_sudo=True,
        store=True,
        help="Adjustment entries associated with this audit detail.",
    )
    adjustment_dr = fields.Monetary(
        string="Total Adjustment Debit",
        compute="_compute_adjustment_ids",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Sum of debit amounts from all linked adjustment entries.",
    )
    adjustment_cr = fields.Monetary(
        string="Total Adjustment Credit",
        compute="_compute_adjustment_ids",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Sum of credit amounts from all linked adjustment entries.",
    )

    @api.depends(
        "adjustment_line_ids",
        "adjustment_line_ids.entry_id",
        "adjustment_line_ids.entry_id.state",
    )
    def _compute_adjustment_ids(self):
        for record in self:
            adjustment_entries = record.adjustment_line_ids.mapped("entry_id").filtered(
                lambda entry: entry.state == "done"
            )
            record.adjustment_ids = adjustment_entries
            record.adjustment_dr = sum(
                record.adjustment_line_ids.filtered(
                    lambda line: line.entry_id.state == "done"
                ).mapped("debit")
            )
            record.adjustment_cr = sum(
                record.adjustment_line_ids.filtered(
                    lambda line: line.entry_id.state == "done"
                ).mapped("credit")
            )

    @api.depends(
        "adjustment_id",
        "account_id",
        "adjustment_debit",
        "adjustment_credit",
        "home_statement_balance",
    )
    def _compute_adjustment_audited_balance(self):
        for record in self:
            adjustment = audited = 0.0
            if record.type_id:
                if record.type_id.normal_balance == "dr":
                    adjustment = record.adjustment_debit - record.adjustment_credit
                else:
                    adjustment = record.adjustment_credit - record.adjustment_debit
            audited = record.home_statement_balance + adjustment
            record.audited_balance = audited
            record.adjustment_balance = adjustment

    adjustment_balance = fields.Monetary(
        string="Adjustment Balance",
        compute="_compute_adjustment_audited_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Net effect of adjustments based on the account's normal balance.",
    )
    audited_balance = fields.Monetary(
        string="Audited Balance",
        compute="_compute_adjustment_audited_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="End period balance after applying adjustments.",
    )
