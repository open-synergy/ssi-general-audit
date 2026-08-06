# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSd66d87aDetail(models.Model):
    """
    ROMM detail line for the Account Level ROMM worksheet (d66d87a).

    One record per standard detail (account/section).  The line carries
    risk assessment attributes from the linked ``general_audit.standard_detail``:

    * ``fraud_impacted``    — whether the account is affected by fraud risk.
    * ``inherent_risk``     — Low / Medium / High.
    * ``significant_risk``  — flagged as a significant risk account.
    * ``control_risk``      — looked up from the Significant Account (ba9b2f0)
      or Business Cycle Internal Control (eabdaad) worksheet.
    * ``romm_risk_initial``/``romm`` — computed from the above using the Risk
      Configuration **pinned on the parent worksheet**
      (``worksheet_id.romm_scoring_config_id``, not whatever is currently
      active in Settings — see that field's help for why) via ROMM Risk
      Initial (Inherent Risk x Control Risk) and ROMM Risk Further, stored
      as ``romm`` (Fraud Risk x Significant Risk x ROMM Risk Initial).
      ``romm`` is written back onto ``standard_detail_id`` explicitly
      inside the compute method.
    * P&D assertion types (``pr_assersion_type_ids``).
    * Planned response flags: analytical procedure, ToC, ToD, interim.

    The P&D assertion types and planned response fields are ``related``, with
    changes written back to the parent ``general_audit.standard_detail``
    record automatically.
    """

    _name = "general_audit_ws_d66d87a.detail"
    _description = "Worksheet d66d87a - Detail"
    _order = "worksheet_id, standard_detail_id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_d66d87a",
        required=True,
        ondelete="cascade",
        help=(
            "Worksheet this line belongs to. Deleting the worksheet will remove "
            "its related lines."
        ),
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="general_audit.standard_detail",
        required=True,
        ondelete="restrict",
        help=("Standard detail (account/assertion) referenced by this line."),
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        related="standard_detail_id.type_id",
        store=True,
        help=(
            "Account type derived from the standard detail; stored for filtering "
            "and reporting."
        ),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="standard_detail_id.currency_id",
        store=True,
        help=("Currency derived from the standard detail; stored for reporting."),
    )

    # Overall Risk Assesment
    fraud_impacted = fields.Boolean(
        string="Impacted By Fraud",
        related="standard_detail_id.fraud_impacted",
        store=True,
        help=("Indicates if the standard detail is impacted by fraud risk factors."),
    )
    inherent_risk = fields.Selection(
        string="Inherent Risk",
        related="standard_detail_id.inherent_risk",
        store=True,
        help=("Inherent risk level inherited from the standard detail."),
    )
    significant_risk = fields.Boolean(
        string="Significant Risk",
        related="standard_detail_id.significant_risk",
        store=True,
        help=(
            "Indicates if the standard detail is flagged as a significant risk "
            "account (set on the Account Level Inherent Risk worksheet)."
        ),
    )
    control_risk = fields.Selection(
        string="Control Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        compute="_compute_control_risk",
        store=True,
        compute_sudo=True,
        help=(
            "Control risk for this account, looked up from the Significant "
            "Account (ba9b2f0) worksheet's Risk field if available, "
            "otherwise from the Business Cycle Internal Control (eabdaad) "
            "worksheet covering this account's type."
        ),
    )

    pr_assersion_type_ids = fields.Many2many(
        string="Assersion Types on Presentation and Disclosure",
        related="standard_detail_id.pr_assersion_type_ids",
        readonly=False,
        help=(
            "Presentation & Disclosure (P&D) assertion types inherited from the "
            "standard detail. Changes here will be synchronized back to the standard detail."
        ),
    )
    romm_risk_initial = fields.Selection(
        string="ROMM Risk Initial",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        compute="_compute_romm",
        store=True,
        help=(
            "Intermediate result (Inherent Risk x Control Risk), classified "
            "using the weights/thresholds in the Risk Configuration. Shown "
            "for transparency; feeds into ROMM Risk Further (romm) below."
        ),
    )
    romm = fields.Selection(
        string="ROMM Risk Further",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        compute="_compute_romm",
        store=True,
        compute_sudo=True,
        help=(
            'Overall ROMM ("ROMM Risk Further"), computed from ROMM Risk '
            "Initial (Inherent Risk x Control Risk) and Fraud Risk x "
            "Significant Risk x ROMM Risk Initial using the Risk "
            "Configuration. Read-only; written back to the standard detail."
        ),
    )
    planned_response_toc = fields.Boolean(
        string="Planned Response TOC",
        related="standard_detail_id.planned_response_toc",
        readonly=False,
        store=True,
        help=(
            "Indicates that tests of controls (ToC) are planned based on the ROMM assessment."
        ),
    )
    planned_response_analytic_procedure = fields.Boolean(
        string="Planned Response Analytic Procedure",
        related="standard_detail_id.planned_response_analytic_procedure",
        readonly=False,
        store=True,
        help=(
            "Indicates that analytical procedures are planned based on the ROMM assessment."
        ),
    )
    planned_response_tod = fields.Boolean(
        string="Planned Response ToD",
        related="standard_detail_id.planned_response_tod",
        readonly=False,
        store=True,
        help=(
            "Indicates that tests of details (ToD) are planned based on the ROMM assessment."
        ),
    )
    planned_response_interim = fields.Boolean(
        string="Planned Response on Interim",
        related="standard_detail_id.planned_response_interim",
        readonly=False,
        store=True,
        help=("Planned timing includes the interim period."),
    )
    planned_response_ye = fields.Boolean(
        string="Planned Response on Year End",
        related="standard_detail_id.planned_response_ye",
        readonly=False,
        store=True,
        help=("Planned timing includes year-end procedures."),
    )

    @api.depends("standard_detail_id", "worksheet_id.general_audit_id")
    def _compute_control_risk(self):
        for record in self:
            record.control_risk = record._get_control_risk_level()

    @api.depends(
        "inherent_risk",
        "control_risk",
        "fraud_impacted",
        "significant_risk",
        "worksheet_id.romm_scoring_config_id",
    )
    def _compute_romm(self):
        # Fallback only - every worksheet gets romm_scoring_config_id pinned
        # at creation time (see general_audit_ws_d66d87a.py). This covers
        # worksheets created before that field existed.
        fallback_config = (
            self.env["general_audit_romm_scoring_config"].sudo()._get_config()
        )
        for record in self:
            config = record.worksheet_id.romm_scoring_config_id or fallback_config
            if not config:
                # No Risk Configuration exists at all (e.g. every record was
                # deleted) - leave ROMM blank rather than erroring out.
                record.romm_risk_initial = False
                record.romm = False
                record.standard_detail_id.write({"romm": False})
                continue
            romm_risk_initial = config.get_romm_risk_initial(
                record.inherent_risk, record.control_risk
            )
            record.romm_risk_initial = romm_risk_initial
            fraud_risk = "high" if record.fraud_impacted else "medium"
            significant_risk_level = "high" if record.significant_risk else "medium"
            record.romm = config.get_romm_risk_further(
                fraud_risk, significant_risk_level, romm_risk_initial
            )
            # Explicit write-back inside the compute (not inverse=) - mirrors
            # general_audit_ws_a418d89.detail._compute_risk(). inverse= only
            # fires when this field is written from OUTSIDE; it is never
            # called when the compute method assigns the value itself.
            record.standard_detail_id.write({"romm": record.romm})

    def _get_control_risk_level(self):
        """Look up Control Risk for this account.

        The Significant Account (ba9b2f0) worksheet's Risk is checked
        first (more specific, one worksheet per account), falling back to
        the Business Cycle Internal Control (eabdaad) worksheet whose
        ``detail_ids.standard_detail_ids`` (matched by account type) covers
        this account. Not tracked by ``@api.depends`` (cross-model search,
        not a relational field path) - re-running "Load Detail" on the
        worksheet re-triggers this on the recreated lines.
        """
        self.ensure_one()
        general_audit = self.worksheet_id.general_audit_id

        ba9b2f0 = self.env["general_audit_ws_ba9b2f0"].search(
            [
                ("general_audit_id", "=", general_audit.id),
                ("standard_detail_id", "=", self.standard_detail_id.id),
                ("risk", "!=", False),
            ],
            limit=1,
        )
        if ba9b2f0:
            return ba9b2f0.risk

        eabdaad_detail = self.env["general_audit_ws_eabdaad.detail"].search(
            [
                ("worksheet_id.general_audit_id", "=", general_audit.id),
                ("standard_detail_ids", "in", self.standard_detail_id.id),
                ("worksheet_id.risk", "!=", False),
            ],
            limit=1,
        )
        if eabdaad_detail:
            return eabdaad_detail.worksheet_id.risk

        return False
