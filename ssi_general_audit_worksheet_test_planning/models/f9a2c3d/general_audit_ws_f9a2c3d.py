# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class GeneralAuditWSf9a2c3d(models.Model):
    """Test Planning Worksheet (f9a2c3d).

    Documents the auditor's planned and actual responses to assessed Risks of
    Material Misstatement (RMM) per significant account type, in accordance with
    ISA 330 — The Auditor's Responses to Assessed Risks.

    One worksheet covers the entire General Audit engagement.  The audit
    approach decision (nature, timing, and extent of procedures) is captured
    per account type via ``detail_ids`` (``general_audit_ws_f9a2c3d.detail``).

    For each significant account type the auditor specifies:
    - Whether an Analytical Procedure (AP) and/or Test of Detail (ToD) is needed
    - Timing: Interim or Year-End
    - Sampling parameters: Confidence Factor, Sampling Interval, and Sample Count

    Sampling formula (ISA 530 MUS):
      Sampling Interval = Tolerable Misstatement ÷ Confidence Factor
      Sample Count      = Sampling Pool ÷ Sampling Interval

    ``Tolerable Misstatement`` is sourced from the linked Preliminary Materiality
    worksheet (``general_audit_ws_d9d2b44``), field ``tolerable_misstatement``.
    ``Confidence Factor`` is determined per account type based on ROMM level and
    AP assurance availability (ISA GUIDE VOL 2, page 231).
    ``Sampling Pool`` is the aggregate monetary amount for the account type after
    excluding individually significant (100%% examined) items.

    Reference standards: ISA 300, ISA 315, ISA 330, ISA 530.
    """

    _name = "general_audit_ws_f9a2c3d"
    _description = "Test Planning (f9a2c3d)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_test_planning.worksheet_type_f9a2c3d"

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
            "Tolerable Misstatement value is used as the basis for "
            "computing Sampling Interval across all detail lines."
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
            "Preliminary Materiality worksheet."
        ),
    )

    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_f9a2c3d.detail",
        inverse_name="worksheet_id",
        string="Test Planning Details",
        readonly=True,
        states={"open": [("readonly", False)]},
        help=(
            "One line per significant account type. Captures the planned audit "
            "approach (nature, timing, extent) and actual test results."
        ),
    )

    def action_load_detail(self):
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        self.ensure_one()
        if not self.general_audit_id:
            raise UserError(_("Cannot load details: General Audit is not set."))
        Detail = self.env["general_audit_ws_f9a2c3d.detail"]
        StandardDetail = self.env["general_audit.standard_detail"]

        all_standard_details = StandardDetail.search(
            [("general_audit_id", "=", self.general_audit_id.id)]
        )
        existing_ids = self.detail_ids.mapped("standard_detail_id").ids

        for sd in all_standard_details:
            if sd.id not in existing_ids:
                Detail.create(
                    {
                        "worksheet_id": self.id,
                        "standard_detail_id": sd.id,
                    }
                )

        # Remove lines whose standard_detail no longer exists in the audit
        valid_ids = all_standard_details.ids
        stale = self.detail_ids.filtered(
            lambda d: d.standard_detail_id.id not in valid_ids
        )
        stale.unlink()
