# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models

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


class GeneralAuditWSf9a2c3dDetail(models.Model):
    """Test Planning Detail (f9a2c3d.detail).

    One record per significant account type within a Test Planning worksheet.
    Captures the three ISA 330 dimensions of audit response — nature, timing,
    and extent — for each account type.

    **Planning fields** (set before fieldwork):
    - ``standard_detail_id``: links to ``general_audit.standard_detail`` which
      carries the account type, audited balance, and materiality context.
    - ``materiality``: M (Material) or TM (Not Material), driven by the audited
      balance vs. performance materiality.
    - ``romm``: combined Risk of Material Misstatement level (L/M/H/No).
    - ``significant_account``: whether this account is classified as significant.
    - ``need_ap``: analytical procedure planned.
    - ``need_tod``: test of detail (substantive sampling) planned.
    - ``timing``: Interim or Year-End.
    - ``direct_examination``: full 100% examination (not sampling).
    - ``need_sampling``: statistical sampling planned.
    - ``population_amount``: aggregate population value for the account type (Rp).
    - ``sampling_amount``: aggregate sampling pool for the account type after
      excluding individually significant (100%% examined) items.
    - ``confidence_factor``: factor from ISA 530 table based on ROMM level and
      AP assurance availability (ISA GUIDE VOL 2 hal. 231).
    - ``sampling_interval``: computed = Tolerable Misstatement ÷ confidence_factor.
      TM is sourced from ``worksheet_id.tolerable_misstatement`` (d9d2b44).
    - ``sample_count``: computed = sampling_amount ÷ sampling_interval.
    """

    _name = "general_audit_ws_f9a2c3d.detail"
    _description = "Test Planning Detail (f9a2c3d)"
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

    # --- Account Type linkage ---
    standard_detail_id = fields.Many2one(
        comodel_name="general_audit.standard_detail",
        string="Standard Account",
        required=True,
        ondelete="restrict",
        help=(
            "Link to the standard detail line in the General Audit. "
            "Provides access to the account type, audited balance, and "
            "materiality data."
        ),
    )
    allowed_standard_detail_ids = fields.Many2many(
        comodel_name="general_audit.standard_detail",
        string="Allowed Standard Details",
        compute="_compute_allowed_standard_detail_ids",
        store=False,
        compute_sudo=True,
        help="Standard detail lines belonging to the parent General Audit.",
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
            "Auto-populated from the Specific Materiality worksheet "
            "(6dcda0e). Material if the account balance exceeds the "
            "Performance Materiality threshold. Can be overridden."
        ),
    )
    romm = fields.Selection(
        string="ROMM",
        related="standard_detail_id.romm",
        store=True,
        compute_sudo=True,
        help=(
            "Combined Risk of Material Misstatement for this account type. "
            "Auto-populated from the Account Level ROMM worksheet (d66d87a). "
            "Can be overridden."
        ),
    )
    significant_account = fields.Boolean(
        string="Significant Account",
        related="standard_detail_id.significant_risk",
        store=True,
        compute_sudo=True,
        help=(
            "Auto-populated from the Inherent Risk worksheet (a418d89). "
            "True if this account type is classified as a significant risk. "
            "Can be overridden."
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
            "Whether a Substantive Analytical Procedure is planned. Can be overridden."
        ),
    )
    ap_result = fields.Selection(
        string="AP Result",
        selection=[
            ("h", "High (H)"),
            ("m", "Moderate (M)"),
            ("n", "None (N)"),
        ],
        help=(
            "Result level of the Analytical Procedure. "
            "Indicates how much assurance was obtained."
        ),
    )
    need_tod = fields.Boolean(
        string="Test of Detail",
        related="standard_detail_id.planned_response_tod",
        store=True,
        compute_sudo=True,
        help=(
            "Auto-populated from the ROMM worksheet planned response. "
            "Whether a Test of Detail (substantive sampling) is planned. Can be overridden."
        ),
    )
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
        default=False,
        help="Whether 100%% direct examination (no sampling) is applied.",
    )
    need_sampling = fields.Boolean(
        string="Statistical Sampling",
        default=False,
        help="Whether statistical sampling is planned for this account.",
    )

    # --- Population & sampling amounts ---
    audited_balance = fields.Monetary(
        string="Audited Balance (Rp)",
        currency_field="currency_id",
        related="standard_detail_id.audited_balance",
        store=True,
        compute_sudo=True,
        help="Audited balance of the account type from the trial balance.",
    )
    key_item_amount = fields.Monetary(
        string="Key Items (Rp)",
        currency_field="currency_id",
        help=(
            "Total amount of key items and directly examined items "
            "(100%% examination). Manually entered by the auditor. "
            "Key items are individual items whose balance exceeds the "
            "Sampling Interval and are examined in full (ISA 530 MUS)."
        ),
    )
    sampling_amount = fields.Monetary(
        string="Sampling Pool (Rp)",
        currency_field="currency_id",
        compute="_compute_sampling_amount",
        store=True,
        compute_sudo=True,
        readonly=False,
        help=(
            "Sampling Pool = Population - Key Items. "
            "Auto-computed as the portion of the population remaining after "
            "removing key items and directly examined items (ISA 530 MUS)."
        ),
    )

    # --- Sampling parameters ---
    confidence_factor = fields.Float(
        string="Confidence Factor",
        digits=(12, 2),
        help=(
            "Confidence factor from ISA sampling table, determined by ROMM level "
            "and availability of Substantive Analytical Procedure assurance."
        ),
    )
    sampling_interval = fields.Monetary(
        string="Sampling Interval",
        currency_field="currency_id",
        compute="_compute_sampling_interval",
        store=True,
        compute_sudo=True,
        help="Sampling Interval = Tolerable Misstatement ÷ Confidence Factor (ISA 530 MUS).",
    )
    sample_count = fields.Float(
        string="Sample Count",
        digits=(12, 2),
        compute="_compute_sample_count",
        store=True,
        compute_sudo=True,
        help="Computed Sample Count = Sampling Pool ÷ Sampling Interval.",
    )

    # --- Computed ---

    @api.depends("standard_detail_id", "worksheet_id.general_audit_id")
    def _compute_materiality(self):
        Mapping = self.env["general_audit_ws_6dcda0e_materiality_mapping"]
        for record in self:
            if (
                not record.standard_detail_id
                or not record.worksheet_id.general_audit_id
            ):
                record.materiality = "tm"
                continue
            mapping = Mapping.search(
                [
                    ("standard_detail_id", "=", record.standard_detail_id.id),
                    (
                        "worksheet_id.general_audit_id",
                        "=",
                        record.worksheet_id.general_audit_id.id,
                    ),
                ],
                limit=1,
            )
            if mapping and mapping.final_materiality == "m":
                record.materiality = "m"
            else:
                record.materiality = "tm"

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

    @api.depends("worksheet_id", "worksheet_id.general_audit_id")
    def _compute_allowed_standard_detail_ids(self):
        StandardDetail = self.env["general_audit.standard_detail"]
        for record in self:
            record.allowed_standard_detail_ids = StandardDetail
            if record.worksheet_id.general_audit_id:
                record.allowed_standard_detail_ids = StandardDetail.search(
                    [
                        (
                            "general_audit_id",
                            "=",
                            record.worksheet_id.general_audit_id.id,
                        )
                    ]
                )

    @api.depends("audited_balance", "key_item_amount")
    def _compute_sampling_amount(self):
        for record in self:
            record.sampling_amount = record.audited_balance - record.key_item_amount

    @api.depends("worksheet_id.tolerable_misstatement", "confidence_factor")
    def _compute_sampling_interval(self):
        for record in self:
            if record.confidence_factor > 0:
                record.sampling_interval = (
                    record.worksheet_id.tolerable_misstatement
                    / record.confidence_factor
                )
            else:
                record.sampling_interval = 0.0

    @api.depends("sampling_amount", "sampling_interval")
    def _compute_sample_count(self):
        for record in self:
            if record.sampling_interval > 0:
                record.sample_count = record.sampling_amount / record.sampling_interval
            else:
                record.sample_count = 0.0
