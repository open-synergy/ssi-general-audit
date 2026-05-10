# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

# ---------------------------------------------------------------------------
# Confidence Factor Reference Table
# Source: ISA GUIDE VOL 2 hal. 231
# Rows: ROMM level  |  Cols: With SAP / Without SAP
# ---------------------------------------------------------------------------
_CF_TABLE = {
    "high": {"no": 2.1, "yes": 2.65},
    "moderate": {"no": 2.65, "yes": 2.65},
    "no": {"no": 1.75, "yes": 1.75},
    "low": {"no": 0.86, "yes": 1.31},
}


class GeneralAuditWSf9a2c3d(models.Model):
    """Test Planning Worksheet (f9a2c3d).

    One worksheet per standard account type within a General Audit engagement.
    Documents the auditor's planned and actual responses to assessed Risks of
    Material Misstatement (RMM) for a specific account type, in accordance with
    ISA 330 — The Auditor's Responses to Assessed Risks.

    Each worksheet is linked to one ``general_audit.standard_detail`` (standard
    account type). The audit approach decision (nature, timing, and extent of
    procedures) is captured at the worksheet (header) level.

    Test of Detail (ToD) can be performed at two levels:
    - ``standard_account``: sampling is computed once at the header level using
      the aggregate population for the entire account type.
    - ``account``: sampling is computed per individual account. The auditor loads
      account lines via ``action_load_detail`` and allocates a Tolerable
      Misstatement per account manually.

    Sampling formula (ISA 530 MUS):
      Sampling Interval = Tolerable Misstatement ÷ Confidence Factor
      Sample Count      = Sampling Pool ÷ Sampling Interval

    ``Confidence Factor`` is determined by ROMM level and AP assurance
    availability (ISA GUIDE VOL 2, page 231).

    Reference standards: ISA 300, ISA 315, ISA 330, ISA 530.
    """

    _name = "general_audit_ws_f9a2c3d"
    _description = "Test Planning (f9a2c3d)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_test_planning.worksheet_type_f9a2c3d"

    # --- Standard Account linkage ---

    @api.depends("general_audit_id")
    def _compute_allowed_standard_detail_ids(self):
        SD = self.env["general_audit.standard_detail"]
        for record in self:
            record.allowed_standard_detail_ids = SD
            if record.general_audit_id:
                record.allowed_standard_detail_ids = SD.search(
                    [("general_audit_id", "=", record.general_audit_id.id)]
                )

    allowed_standard_detail_ids = fields.Many2many(
        comodel_name="general_audit.standard_detail",
        string="Allowed Standard Details",
        compute="_compute_allowed_standard_detail_ids",
        store=False,
        compute_sudo=True,
        help="Standard detail lines belonging to the parent General Audit.",
    )
    standard_detail_id = fields.Many2one(
        comodel_name="general_audit.standard_detail",
        string="Standard Account",
        ondelete="restrict",
        readonly=True,
        states={"open": [("readonly", False)]},
        help=(
            "Standard account type this worksheet covers. "
            "One worksheet per standard account per General Audit."
        ),
    )
    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Account Type",
        related="standard_detail_id.type_id",
        store=True,
        compute_sudo=True,
        help="Account type derived from the selected standard detail.",
    )

    # --- Risk & Materiality classification ---

    @api.depends("standard_detail_id", "general_audit_id")
    def _compute_materiality(self):
        Mapping = self.env["general_audit_ws_6dcda0e_materiality_mapping"]
        for record in self:
            if not record.standard_detail_id or not record.general_audit_id:
                record.materiality = "tm"
                continue
            mapping = Mapping.search(
                [
                    ("standard_detail_id", "=", record.standard_detail_id.id),
                    (
                        "worksheet_id.general_audit_id",
                        "=",
                        record.general_audit_id.id,
                    ),
                ],
                limit=1,
            )
            if mapping and mapping.final_materiality == "m":
                record.materiality = "m"
            else:
                record.materiality = "tm"

    materiality = fields.Selection(
        string="Materiality",
        selection=[
            ("m", "Material (M)"),
            ("tm", "Not Material (TM)"),
        ],
        compute="_compute_materiality",
        store=True,
        compute_sudo=True,
        help=(
            "Auto-populated from the Specific Materiality worksheet (6dcda0e). "
            "Material if the account balance exceeds the Performance Materiality threshold."
        ),
    )
    romm = fields.Selection(
        string="ROMM",
        related="standard_detail_id.romm",
        store=True,
        compute_sudo=True,
        help=(
            "Combined Risk of Material Misstatement for this account type. "
            "Auto-populated from the Account Level ROMM worksheet (d66d87a)."
        ),
    )
    significant_account = fields.Boolean(
        string="Significant Account",
        related="standard_detail_id.significant_risk",
        store=True,
        compute_sudo=True,
        help=(
            "Auto-populated from the Inherent Risk worksheet (a418d89). "
            "True if this account type is classified as a significant risk."
        ),
    )

    @api.depends("risk_factor_adjustment", "tolerable_misstatement")
    def _compute_specific_materiality(self):
        for record in self:
            record.specific_materiality = (
                record.risk_factor_adjustment / 100.0 * record.tolerable_misstatement
            )

    specific_materiality = fields.Monetary(
        string="Specific Materiality",
        currency_field="currency_id",
        compute="_compute_specific_materiality",
        store=True,
        compute_sudo=True,
        help=(
            "Specific Materiality = Risk Factor Adjustment (%) × Tolerable Misstatement."
        ),
    )
    risk_factor_adjustment = fields.Float(
        string="Risk Factor Adjustment (%)",
        digits=(12, 2),
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Risk Factor Adjustment percentage applied to Tolerable "
        "Misstatement to derive Specific Materiality.",
    )

    # --- Preliminary Materiality linkage ---

    @api.depends("general_audit_id")
    def _compute_allowed_preliminary_materiality_ids(self):
        WS = self.env["general_audit_ws_d9d2b44"]
        for record in self:
            record.allowed_preliminary_materiality_ids = WS
            if record.general_audit_id:
                record.allowed_preliminary_materiality_ids = WS.search(
                    [("general_audit_id", "=", record.general_audit_id.id)]
                )

    allowed_preliminary_materiality_ids = fields.Many2many(
        comodel_name="general_audit_ws_d9d2b44",
        string="Allowed Preliminary Materiality Worksheets",
        compute="_compute_allowed_preliminary_materiality_ids",
        store=False,
        compute_sudo=True,
        help="Preliminary Materiality worksheets linked to the same General Audit.",
    )
    preliminary_materiality_id = fields.Many2one(
        comodel_name="general_audit_ws_d9d2b44",
        string="Preliminary Materiality",
        ondelete="restrict",
        readonly=True,
        states={"open": [("readonly", False)]},
        help=(
            "Materiality Computation worksheet (d9d2b44) whose "
            "Tolerable Misstatement value is used when sampling at "
            "the standard account level (tod_level = 'standard_account')."
        ),
    )
    tolerable_misstatement = fields.Monetary(
        string="Tolerable Misstatement",
        related="preliminary_materiality_id.tolerable_misstatement",
        store=True,
        compute_sudo=True,
        currency_field="currency_id",
        help=(
            "Tolerable Misstatement sourced from the linked "
            "Preliminary Materiality worksheet. "
            "Used when tod_level = 'standard_account'."
        ),
    )

    # --- Audit approach (nature & timing) ---

    need_ap = fields.Boolean(
        string="Analytical Procedure",
        related="standard_detail_id.planned_response_analytic_procedure",
        store=True,
        compute_sudo=True,
        help=(
            "Auto-populated from the ROMM worksheet planned response. "
            "Whether a Substantive Analytical Procedure is planned."
        ),
    )
    ap_result = fields.Selection(
        string="AP Result",
        selection=[
            ("h", "High (H)"),
            ("m", "Moderate (M)"),
            ("n", "None (N)"),
        ],
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Result level of the Analytical Procedure.",
    )
    need_tod = fields.Boolean(
        string="Test of Detail",
        related="standard_detail_id.planned_response_tod",
        store=True,
        compute_sudo=True,
        help=(
            "Auto-populated from the ROMM worksheet planned response. "
            "Whether a Test of Detail (substantive sampling) is planned."
        ),
    )

    @api.depends(
        "standard_detail_id.planned_response_interim",
        "standard_detail_id.planned_response_ye",
    )
    def _compute_timing(self):
        for record in self:
            if record.standard_detail_id.planned_response_interim:
                record.timing = "interim"
            elif record.standard_detail_id.planned_response_ye:
                record.timing = "ye"
            else:
                record.timing = False

    timing = fields.Selection(
        string="Timing",
        selection=[
            ("interim", "Interim (I)"),
            ("ye", "Year-End (YE)"),
        ],
        compute="_compute_timing",
        store=True,
        compute_sudo=True,
        help=(
            "Auto-populated from the ROMM worksheet planned response timing "
            "(Interim / Year-End). Can be overridden."
        ),
    )
    direct_examination = fields.Boolean(
        string="Direct Examination",
        default=True,
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Whether 100%% direct examination (no sampling) is applied.",
    )
    need_sampling = fields.Boolean(
        string="Sampling",
        default=False,
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Whether statistical sampling is planned for this account.",
    )

    # --- ToD sampling level ---

    tod_level = fields.Selection(
        string="ToD Level",
        selection=[
            ("standard_account", "Per Standard Account"),
            ("account", "Per Individual Account"),
        ],
        default="standard_account",
        readonly=True,
        states={"open": [("readonly", False)]},
        help=(
            "Determines the granularity of Test of Detail:\n"
            "- Per Standard Account: sampling is computed once at the header level "
            "for the entire account type population.\n"
            "- Per Individual Account: sampling is computed per individual account. "
            "Use the 'Load / Sync Accounts' button to populate the detail lines."
        ),
    )

    # --- Population & sampling amounts (used when tod_level = 'standard_account') ---

    audited_balance = fields.Monetary(
        string="Audited Balance (Rp)",
        currency_field="currency_id",
        related="standard_detail_id.audited_balance",
        store=True,
        compute_sudo=True,
        help="Audited balance of the account type from the trial balance.",
    )
    key_item_amount = fields.Monetary(
        string="Direct Examination (Rp)",
        currency_field="currency_id",
        readonly=True,
        states={"open": [("readonly", False)]},
        help=(
            "Total amount of key items and directly examined items "
            "(100%% examination). Manually entered by the auditor. "
            "Key items are individual items whose balance exceeds the "
            "Sampling Interval and are examined in full (ISA 530 MUS)."
        ),
    )

    @api.onchange(
        "standard_detail_id",
        "direct_examination",
        "need_sampling",
    )
    def _onchange_examination_sampling(self):
        if self.direct_examination and not self.need_sampling:
            self.key_item_amount = self.audited_balance
        elif not self.direct_examination and self.need_sampling:
            self.key_item_amount = 0.0

    @api.depends(
        "standard_detail_id",
        "audited_balance",
        "key_item_amount",
    )
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
        help=(
            "Sampling Pool = Audited Balance - Key Items. "
            "Auto-computed as the portion of the population remaining after "
            "removing key items and directly examined items (ISA 530 MUS)."
        ),
    )
    confidence_factor = fields.Float(
        string="Confidence Factor",
        digits=(12, 2),
        readonly=True,
        states={"open": [("readonly", False)]},
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

    # --- Individual account detail lines (used when tod_level = 'account') ---

    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_f9a2c3d.detail",
        inverse_name="worksheet_id",
        string="Account Details",
        readonly=True,
        states={"open": [("readonly", False)]},
        help=(
            "Individual account lines for this standard account type. "
            "Populated via 'Load / Sync Accounts' when tod_level = 'account'. "
            "Each line carries its own sampling calculation with a manually "
            "allocated Tolerable Misstatement."
        ),
    )

    def action_load_detail(self):
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        self.ensure_one()
        if not self.general_audit_id:
            raise UserError(_("Cannot load details: General Audit is not set."))
        if not self.standard_detail_id:
            raise UserError(_("Cannot load details: Standard Account is not set."))
        Detail = self.env["general_audit_ws_f9a2c3d.detail"]
        AuditDetail = self.env["general_audit.detail"]

        type_id = self.standard_detail_id.type_id.id
        all_audit_details = AuditDetail.search(
            [
                ("general_audit_id", "=", self.general_audit_id.id),
                ("type_id", "=", type_id),
            ]
        )
        existing_ids = self.detail_ids.mapped("audit_detail_id").ids

        for ad in all_audit_details:
            if ad.id not in existing_ids:
                Detail.create(
                    {
                        "worksheet_id": self.id,
                        "audit_detail_id": ad.id,
                    }
                )

        # Remove stale lines whose audit_detail no longer belongs to this type
        valid_ids = all_audit_details.ids
        stale = self.detail_ids.filtered(
            lambda d: d.audit_detail_id.id not in valid_ids
        )
        stale.unlink()
