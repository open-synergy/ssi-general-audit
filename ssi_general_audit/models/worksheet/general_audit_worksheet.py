# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWorksheet(models.Model):
    """
    Record Bersama untuk Seluruh Worksheet Audit (Shadow Record).

    Model konkret yang menjadi dasar bagi setiap worksheet audit melalui
    mekanisme *delegated inheritance* (``_inherits``). Satu record
    ``general_audit_worksheet`` dibuat otomatis ketika worksheet konkret
    dibuat, dan dihapus otomatis ketika worksheet konkretnya dihapus.

    Menyimpan field-field umum yang dimiliki oleh semua tipe worksheet:
    tanggal persiapan, tanggal review, penanggungjawab, kesimpulan, dan
    catatan review. Alur status: draft → open → confirm → done.

    Semua worksheet konkret (mis. acceptance & continuance, assignment letter,
    audit program) mewarisi field ini melalui ``GeneralAuditWorksheetMixin``.
    """

    _name = "general_audit_worksheet"
    _description = "General Audit Worksheet"
    _inherit = [
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.single_operating_unit",
    ]
    _order = "general_audit_id, parent_type_id, id"

    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"
    _create_sequence_state = "open"

    @api.model
    def _get_policy_field(self):
        res = super(GeneralAuditWorksheet, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "open_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def _compute_policy(self):
        _super = super(GeneralAuditWorksheet, self)
        _super._compute_policy()

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        readonly=True,
        required=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="General Audit to which this worksheet belongs.",
    )
    # Fields related from general audit
    date_start = fields.Date(
        string="Start Date",
        related="general_audit_id.date_start",
        readonly=True,
        store=True,
        help="Audit period start date.",
        compute_sudo=True,
    )
    date_end = fields.Date(
        string="End Date",
        related="general_audit_id.date_end",
        readonly=True,
        store=True,
        help="Audit period end date.",
        compute_sudo=True,
    )
    interim_date_start = fields.Date(
        string="Interim Start Date",
        related="general_audit_id.interim_date_start",
        readonly=True,
        store=True,
        help="Start date for the interim period.",
        compute_sudo=True,
    )
    interim_date_end = fields.Date(
        string="Interim End Date",
        related="general_audit_id.interim_date_end",
        readonly=True,
        store=True,
        help="End date for the interim period.",
        compute_sudo=True,
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        related="general_audit_id.previous_date_start",
        readonly=True,
        store=True,
        help="Start date of the previous period.",
        compute_sudo=True,
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        related="general_audit_id.previous_date_end",
        readonly=True,
        store=True,
        help="End date of the previous period.",
        compute_sudo=True,
    )
    preparation_date = fields.Date(
        string="Preparation Date",
        help="Date when the worksheet was prepared.",
    )
    preparation_time = fields.Integer(
        string="Preparation Time",
        help="Effort spent preparing the worksheet (in hours or minutes).",
    )
    review_date = fields.Date(
        string="Review Date",
        help="Date when the worksheet was reviewed.",
    )
    review_time = fields.Integer(
        string="Review Time",
        help="Effort spent reviewing the worksheet (in hours or minutes).",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        readonly=True,
        store=True,
        help="Currency used for amounts in this worksheet.",
        compute_sudo=True,
    )
    account_type_set_id = fields.Many2one(
        string="Accoount Type Set",
        comodel_name="client_account_type_set",
        related="general_audit_id.account_type_set_id",
        readonly=True,
        store=True,
        help="Account type set used by the linked General Audit.",
        compute_sudo=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        related="general_audit_id.partner_id",
        store=True,
        help="Audited client company.",
        compute_sudo=True,
    )
    accountant_id = fields.Many2one(
        string="Accountant",
        related="general_audit_id.accountant_id",
        store=True,
        help="Accountant responsible for the audit.",
        compute_sudo=True,
    )
    title = fields.Char(
        string="Title",
        related="general_audit_id.title",
        store=True,
        help="Title of the General Audit engagement.",
        compute_sudo=True,
    )
    parent_type_id = fields.Many2one(
        string="Parent Type",
        comodel_name="general_audit_worksheet_type",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        ondelete="restrict",
        help="Worksheet type category/group for this specific worksheet.",
    )
    conclusion_id = fields.Many2one(
        string="Conclusion",
        comodel_name="general_audit_worksheet_conclusion",
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        ondelete="restrict",
        help="Selected conclusion summarizing the worksheet's assessment.",
    )
    conclusion = fields.Text(
        string="Conclusion Additional Explanation",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Narrative explanation to support the selected conclusion.",
    )
    review = fields.Text(
        string="Review Notes",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
            "confirm": [
                ("readonly", False),
            ],
        },
        help="Notes and observations from the review of the worksheet.",
    )
