# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import api, fields, models


class GeneralAuditGroupDetail(models.Model):
    _name = "general_audit.group_detail"
    _description = "Accountant General Audit Group Detail"
    _order = "general_audit_id, group_id, id"

    group_id = fields.Many2one(
        string="Account Group",
        comodel_name="client_account_group",
        required=True,
        ondelete="restrict",
        help="Client account group represented by this line.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Ordering number for this group line.",
    )
    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        required=True,
        ondelete="cascade",
        help="General Audit document that owns this group line.",
    )

    @api.depends(
        "general_audit_id",
        "general_audit_id.home_trial_balance_id",
        "general_audit_id.interim_trial_balance_id",
        "general_audit_id.previous_trial_balance_id",
        "general_audit_id.home_trial_balance_id.state",
        "general_audit_id.interim_trial_balance_id.state",
        "general_audit_id.previous_trial_balance_id.state",
    )
    def _compute_group_line(self):
        GroupDetail = self.env["client_trial_balance.group_detail"]
        for record in self:
            home_result = interim_result = previous_result = False
            criteria = [
                ("group_id", "=", record.group_id.id),
            ]
            if record.general_audit_id.home_trial_balance_id:
                criteria_home = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.home_trial_balance_id.id,
                    )
                ]
                home_results = GroupDetail.search(criteria_home)
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
                interim_results = GroupDetail.search(criteria_interim)
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
                previous_results = GroupDetail.search(criteria_previous)
                if len(previous_results) > 0:
                    previous_result = previous_results[0]

            record.home_group_line_id = home_result
            record.interim_group_line_id = interim_result
            record.previous_group_line_id = previous_result

    home_group_line_id = fields.Many2one(
        string="End Period TB Standard Line",
        comodel_name="client_trial_balance.group_detail",
        readonly=True,
        compute="_compute_group_line",
        store=True,
        help="Linked group detail for the end period trial balance.",
    )
    interim_group_line_id = fields.Many2one(
        string="Interim TB Standard Line",
        comodel_name="client_trial_balance.group_detail",
        readonly=True,
        compute="_compute_group_line",
        store=True,
        help="Linked group detail for the interim trial balance.",
    )
    previous_group_line_id = fields.Many2one(
        string="Previous TB Standard Line",
        comodel_name="client_trial_balance.group_detail",
        readonly=True,
        compute="_compute_group_line",
        store=True,
        help="Linked group detail for the previous period trial balance.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        store=True,
        help="Currency used for amounts; inherited from the General Audit.",
    )
    home_statement_balance = fields.Monetary(
        string="End Period Balance",
        related="home_group_line_id.balance",
        store=True,
        currency_field="currency_id",
        help="Net balance of the group from the end period trial balance.",
    )
    interim_balance = fields.Monetary(
        string="Interim Balance",
        related="interim_group_line_id.balance",
        store=True,
        currency_field="currency_id",
        help="Net balance of the group from the interim trial balance.",
    )

    @api.depends(
        "general_audit_id.standard_detail_ids",
        "general_audit_id.standard_detail_ids.extrapolation_balance",
        "general_audit_id.standard_detail_ids.adjusted_extrapolation_balance",
        "general_audit_id.standard_detail_ids.extrapolation_adjustment",
        "group_id",
    )
    def _compute_extrapolation_balance(self):
        for record in self:
            result = 0.0
            if record.group_id:
                ga = record.general_audit_id
                for standard in ga.standard_detail_ids.filtered(
                    lambda r: r.type_id.group_id.id == record.group_id.id
                ):
                    result += standard.adjusted_extrapolation_balance
            record.extrapolation_balance = result

    extrapolation_balance = fields.Monetary(
        string="Extrapolation Balance",
        related=False,
        compute="_compute_extrapolation_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Adjusted extrapolation balance aggregated for this group.",
    )
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="previous_group_line_id.balance",
        store=True,
        currency_field="currency_id",
        help="Net balance of the group from the previous period trial balance.",
    )

    @api.depends(
        "interim_balance",
        "extrapolation_balance",
        "previous_balance",
        "home_statement_balance",
        "audited_balance",
    )
    def _compute_average(self):
        for record in self:
            interim_avg = (record.interim_balance + record.previous_balance) / 2.0
            extrapolation_avg = (
                record.extrapolation_balance + record.previous_balance
            ) / 2.0
            home_statement_avg = (
                record.home_statement_balance + record.previous_balance
            ) / 2.0
            audited_avg = (record.audited_balance + record.previous_balance) / 2.0

            record.interim_avg = interim_avg
            record.extrapolation_avg = extrapolation_avg
            record.home_statement_avg = home_statement_avg
            record.audited_avg = audited_avg

    interim_avg = fields.Monetary(
        string="Interim Average",
        compute="_compute_average",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Average of interim and previous balances.",
    )
    extrapolation_avg = fields.Monetary(
        string="Extrapolation Average",
        compute="_compute_average",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Average of extrapolation and previous balances.",
    )
    home_statement_avg = fields.Monetary(
        string="End Period Average",
        compute="_compute_average",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Average of end period and previous balances.",
    )
    audited_avg = fields.Monetary(
        string="Audited Average",
        compute="_compute_average",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Average of audited and previous balances.",
    )

    @api.depends(
        "general_audit_id.adjustment_entry_ids",
        "general_audit_id.adjustment_entry_ids.state",
        "general_audit_id.adjustment_entry_ids.detail_ids.account_id",
        "general_audit_id.adjustment_entry_ids.detail_ids.debit",
        "general_audit_id.adjustment_entry_ids.detail_ids.credit",
    )
    def _compute_adjustment_id(self):
        StandardAdjustment = self.env["general_audit.group_adjustment"]
        for record in self:
            result = False
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("group_id", "=", record.group_id.id),
            ]
            standard_adjustments = StandardAdjustment.search(criteria)
            if len(standard_adjustments) > 0:
                result = standard_adjustments[0]
            record.adjustment_id = result

    adjustment_id = fields.Many2one(
        string="Adjustment",
        comodel_name="general_audit.group_adjustment",
        readonly=True,
        compute="_compute_adjustment_id",
        store=True,
        help="Aggregated adjustments affecting this group.",
    )
    adjustment_debit = fields.Monetary(
        string="Adjustment Debit",
        store=True,
        compute="_compute_adjustment",
        compute_sudo=True,
        currency_field="currency_id",
        help="Total debit adjustments for this group.",
    )
    adjustment_credit = fields.Monetary(
        string="Adjustment Credit",
        store=True,
        compute="_compute_adjustment",
        compute_sudo=True,
        currency_field="currency_id",
        help="Total credit adjustments for this group.",
    )

    @api.depends(
        "general_audit_id.adjustment_entry_ids",
        "general_audit_id.adjustment_entry_ids.state",
        "general_audit_id.adjustment_entry_ids.detail_ids.account_id",
        "general_audit_id.adjustment_entry_ids.detail_ids.debit",
        "general_audit_id.adjustment_entry_ids.detail_ids.credit",
        "group_id",
    )
    def _compute_adjustment(self):
        for record in self:
            debit = credit = 0.0
            ga = record.general_audit_id
            for adjustment in ga.adjustment_entry_ids.filtered(
                lambda r: r.state == "done"
            ):
                for detail in adjustment.detail_ids.filtered(
                    lambda r: r.account_id.group_id.id == record.group_id.id
                ):
                    debit += detail.debit
                    credit += detail.credit
            record.adjustment_debit = debit
            record.adjustment_credit = credit

    @api.depends(
        "adjustment_debit",
        "adjustment_credit",
        "group_id",
        "home_statement_balance",
    )
    def _compute_adjustment_audited_balance(self):
        for record in self:
            adjustment = audited = 0.0
            if record.group_id:
                if record.group_id.normal_balance == "dr":
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
        help="Net effect of adjustments on the group based on normal balance.",
    )
    audited_balance = fields.Monetary(
        string="Audited Balance",
        compute="_compute_adjustment_audited_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="End period balance after applying adjustments to the group.",
    )
