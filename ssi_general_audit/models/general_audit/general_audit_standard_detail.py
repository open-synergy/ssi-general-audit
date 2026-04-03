# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval as eval  # pylint: disable=redefined-builtin


class GeneralAuditStandardDetail(models.Model):
    """
    Baris Tipe Akun Standar dalam General Audit.

    Menyimpan referensi ke tipe akun standar (``client_account_type``) yang
    dianalisis dalam satu engagement audit, beserta saldo komparatif tiga
    periode yang diambil dari baris standar neraca saldo
    (``client_trial_balance.standard_detail``). Digunakan sebagai dasar
    prosedur analitis substansi (ISA 520 / SA 520) dan penetapan
    signifikansi material per tipe akun.
    """

    _name = "general_audit.standard_detail"
    _description = "Accountant General Audit Standard Detail"
    _order = "general_audit_id, type_id, id"
    _rec_name = "type_id"

    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        required=True,
        ondelete="restrict",
        help="Standard account type being analyzed.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Ordering number for the standard detail line.",
    )
    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        required=True,
        ondelete="cascade",
        help="General Audit that owns this standard detail line.",
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
    def _compute_standard_line(self):
        StandardDetail = self.env["client_trial_balance.standard_detail"]
        for record in self:
            home_result = interim_result = previous_result = False
            criteria = [
                ("type_id", "=", record.type_id.id),
            ]
            if record.general_audit_id.home_trial_balance_id:
                criteria_home = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.home_trial_balance_id.id,
                    )
                ]
                home_results = StandardDetail.search(criteria_home)
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
                interim_results = StandardDetail.search(criteria_interim)
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
                previous_results = StandardDetail.search(criteria_previous)
                if len(previous_results) > 0:
                    previous_result = previous_results[0]

            record.home_standard_line_id = home_result
            record.interim_standard_line_id = interim_result
            record.previous_standard_line_id = previous_result

    @api.depends(
        "general_audit_id.adjustment_entry_ids",
        "general_audit_id.adjustment_entry_ids.state",
        "general_audit_id.adjustment_entry_ids.detail_ids.account_id",
        "general_audit_id.adjustment_entry_ids.detail_ids.debit",
        "general_audit_id.adjustment_entry_ids.detail_ids.credit",
    )
    def _compute_standard_adjustment_id(self):
        StandardAdjustment = self.env["general_audit.adjustment"]
        for record in self:
            result = False
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("type_id", "=", record.type_id.id),
            ]
            standard_adjustments = StandardAdjustment.search(criteria)
            if len(standard_adjustments) > 0:
                result = standard_adjustments[0]
            record.standard_adjustment_id = result

    standard_adjustment_id = fields.Many2one(
        string="Standard Adjustment",
        comodel_name="general_audit.adjustment",
        readonly=True,
        compute="_compute_standard_adjustment_id",
        compute_sudo=True,
        store=True,
    )

    home_standard_line_id = fields.Many2one(
        string="End Period TB Standard Line",
        comodel_name="client_trial_balance.standard_detail",
        readonly=True,
        compute="_compute_standard_line",
        compute_sudo=True,
        store=True,
        help="Linked standard detail for the end period trial balance.",
    )
    interim_standard_line_id = fields.Many2one(
        string="Interim TB Standard Line",
        comodel_name="client_trial_balance.standard_detail",
        readonly=True,
        compute="_compute_standard_line",
        compute_sudo=True,
        store=True,
        help="Linked standard detail for the interim trial balance.",
    )
    previous_standard_line_id = fields.Many2one(
        string="Previous TB Standard Line",
        comodel_name="client_trial_balance.standard_detail",
        readonly=True,
        compute="_compute_standard_line",
        compute_sudo=True,
        store=True,
        help="Linked standard detail for the previous period trial balance.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        compute_sudo=True,
        store=True,
        help="Currency used for amounts; inherited from the General Audit.",
    )
    home_statement_opening_balance = fields.Monetary(
        string="End Period Opening Balance",
        related="home_standard_line_id.opening_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Opening balance from the end period trial balance.",
    )
    home_statement_balance = fields.Monetary(
        string="End Period Balance",
        related="home_standard_line_id.balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Net balance from the end period trial balance.",
    )
    interim_opening_balance = fields.Monetary(
        string="Interim Opening Balance",
        related="interim_standard_line_id.opening_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Opening balance from the interim trial balance.",
    )
    interim_balance = fields.Monetary(
        string="Interim Balance",
        related="interim_standard_line_id.balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Net balance from the interim trial balance.",
    )

    @api.depends(
        "interim_balance",
        "previous_balance",
        "type_id",
    )
    def _compute_extrapolation_balance(self):
        for record in self:
            balance = 0.0
            if record.type_id:
                python_code = record.type_id.python_code
                localdict = record._get_localdict()
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    balance = localdict["result"]
                except Exception as e:
                    err_msg = """
                    Type: %s
                    Error: %s
                    """ % (
                        record.type_id.name,
                        e,
                    )
                    raise ValidationError(err_msg)
            record.extrapolation_balance = balance

    extrapolation_balance = fields.Monetary(
        string="Extrapolation Balance",
        related=False,
        compute="_compute_extrapolation_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Extrapolated balance computed using the type's Python code.",
    )

    extrapolation_adjustment = fields.Monetary(
        string="Extrapolation Adjustment",
        currency_field="currency_id",
        help="Manual or calculated adjustment applied to the extrapolation.",
    )

    @api.depends(
        "extrapolation_balance",
        "extrapolation_adjustment",
    )
    def _compute_adjusted_extrapolation_balance(self):
        for record in self:
            result = record.extrapolation_balance + record.extrapolation_adjustment
            record.adjusted_extrapolation_balance = result

    adjusted_extrapolation_balance = fields.Monetary(
        string="Adjusted Extrapolation Balance",
        currency_field="currency_id",
        store=True,
        compute="_compute_adjusted_extrapolation_balance",
        compute_sudo=True,
        help="Extrapolation balance after applying the adjustment.",
    )

    previous_opening_balance = fields.Monetary(
        string="Previous Opening Balance",
        related="previous_standard_line_id.opening_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Opening balance from the previous period trial balance.",
    )
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="previous_standard_line_id.balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Net balance from the previous period trial balance.",
    )

    adjustment_debit = fields.Monetary(
        string="Adjustment Debit",
        related="standard_adjustment_id.debit",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Total debit adjustments affecting this type.",
    )
    adjustment_credit = fields.Monetary(
        string="Adjustment Credit",
        related="standard_adjustment_id.credit",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="Total credit adjustments affecting this type.",
    )

    @api.depends(
        "type_id",
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
        help="Net effect of adjustments based on the normal balance.",
    )
    audited_balance = fields.Monetary(
        string="Audited Balance",
        compute="_compute_adjustment_audited_balance",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
        help="End period balance after applying adjustments.",
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
                record.adjusted_extrapolation_balance + record.previous_balance
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
        help="Average of adjusted extrapolation and previous balances.",
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

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
            "standard_detail": self,
            "ga": self.general_audit_id,
        }
