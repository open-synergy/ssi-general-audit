# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSf9a2c3dDetail(models.Model):
    """Test Planning Account Detail (f9a2c3d.detail).

    One record per individual client account within a Test Planning worksheet
    where Test of Detail is performed at the account level
    (``tod_level = 'account'`` on the parent worksheet).

    Each line is linked to a ``general_audit.detail`` record (an individual
    client account within the General Audit). The auditor manually allocates
    a Tolerable Misstatement per account and enters Key Items to compute
    the sampling parameters.

    Sampling formula (ISA 530 MUS):
      Sampling Pool     = Account Balance - Key Items
      Sampling Interval = Tolerable Misstatement ÷ Confidence Factor
      Sample Count      = Sampling Pool ÷ Sampling Interval
    """

    _name = "general_audit_ws_f9a2c3d.detail"
    _description = "Test Planning Account Detail (f9a2c3d)"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_f9a2c3d",
        string="# Worksheet",
        required=True,
        ondelete="cascade",
        help="Parent Test Planning worksheet.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        help="Display order within the worksheet.",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="worksheet_id.currency_id",
        store=True,
        compute_sudo=True,
        help="Currency inherited from the parent worksheet.",
    )

    # --- Account linkage ---

    @api.depends(
        "worksheet_id",
        "worksheet_id.general_audit_id",
        "worksheet_id.standard_detail_id",
    )
    def _compute_allowed_audit_detail_ids(self):
        AuditDetail = self.env["general_audit.detail"]
        for record in self:
            record.allowed_audit_detail_ids = AuditDetail
            ws = record.worksheet_id
            if ws.general_audit_id and ws.standard_detail_id:
                record.allowed_audit_detail_ids = AuditDetail.search(
                    [
                        ("general_audit_id", "=", ws.general_audit_id.id),
                        ("type_id", "=", ws.standard_detail_id.type_id.id),
                    ]
                )

    allowed_audit_detail_ids = fields.Many2many(
        comodel_name="general_audit.detail",
        string="Allowed Audit Details",
        compute="_compute_allowed_audit_detail_ids",
        store=False,
        compute_sudo=True,
        help="Individual account detail lines available for this account type.",
    )
    audit_detail_id = fields.Many2one(
        comodel_name="general_audit.detail",
        string="Account",
        required=True,
        ondelete="restrict",
        help="Individual client account detail from the General Audit.",
    )
    account_id = fields.Many2one(
        comodel_name="client_account",
        string="Client Account",
        related="audit_detail_id.account_id",
        store=True,
        compute_sudo=True,
        help="Client account from the linked audit detail.",
    )
    audited_balance = fields.Monetary(
        string="Account Balance (Rp)",
        currency_field="currency_id",
        related="audit_detail_id.audited_balance",
        store=True,
        compute_sudo=True,
        help="Audited balance for this individual account.",
    )

    # --- Sampling parameters ---

    specific_materiality = fields.Monetary(
        string="Specific Materiality (Rp)",
        currency_field="currency_id",
        help=(
            "Specific Materiality for this individual account. "
            "Manually entered by the auditor."
        ),
    )
    direct_examination = fields.Boolean(
        string="Direct Examination",
        default=True,
        help="Whether 100%% direct examination (no sampling) is applied.",
    )
    need_sampling = fields.Boolean(
        string="Sampling",
        default=False,
        help="Whether statistical sampling is planned for this account.",
    )

    @api.onchange("direct_examination", "need_sampling")
    def _onchange_examination_sampling(self):
        if self.direct_examination and not self.need_sampling:
            self.key_item_amount = self.audited_balance
        elif not self.direct_examination and self.need_sampling:
            self.key_item_amount = 0.0

    tolerable_misstatement = fields.Monetary(
        string="Tolerable Misstatement (Rp)",
        currency_field="currency_id",
        help=(
            "Tolerable Misstatement allocated to this individual account. "
            "Manually entered by the auditor (ISA 530 MUS)."
        ),
    )
    key_item_amount = fields.Monetary(
        string="Direct Examination (Rp)",
        currency_field="currency_id",
        help=(
            "Total amount of key items and directly examined items "
            "(100%% examination). Manually entered by the auditor."
        ),
    )

    @api.depends("audited_balance", "key_item_amount")
    def _compute_sampling_amount(self):
        for record in self:
            record.sampling_amount = record.audited_balance - record.key_item_amount

    sampling_amount = fields.Monetary(
        string="Sampling (Rp)",
        currency_field="currency_id",
        compute="_compute_sampling_amount",
        store=True,
        compute_sudo=True,
        readonly=False,
        help="Sampling Pool = Account Balance - Key Items (ISA 530 MUS).",
    )
    confidence_factor = fields.Float(
        string="Confidence Factor",
        digits=(12, 2),
        help=(
            "Confidence factor from ISA sampling table, determined by ROMM level "
            "and availability of Substantive Analytical Procedure assurance "
            "(ISA GUIDE VOL 2, page 231)."
        ),
    )

    @api.depends("tolerable_misstatement", "confidence_factor")
    def _compute_sampling_interval(self):
        for record in self:
            if record.confidence_factor > 0:
                record.sampling_interval = (
                    record.tolerable_misstatement / record.confidence_factor
                )
            else:
                record.sampling_interval = 0.0

    sampling_interval = fields.Monetary(
        string="Sampling Interval",
        currency_field="currency_id",
        compute="_compute_sampling_interval",
        store=True,
        compute_sudo=True,
        help="Sampling Interval = Tolerable Misstatement ÷ Confidence Factor (ISA 530 MUS).",
    )

    @api.depends("sampling_amount", "sampling_interval")
    def _compute_sample_count(self):
        for record in self:
            if record.sampling_interval > 0:
                record.sample_count = record.sampling_amount / record.sampling_interval
            else:
                record.sample_count = 0.0

    sample_count = fields.Float(
        string="Sample Count",
        digits=(12, 2),
        compute="_compute_sample_count",
        store=True,
        compute_sudo=True,
        help="Computed Sample Count = Sampling Pool ÷ Sampling Interval.",
    )
