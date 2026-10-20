# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSf9a2c3dDetail(models.Model):
    """Test of Detail Planning Line (f9a2c3d.detail).

    One record per standard account of the General Audit. Nine columns
    describe the planning of the Test of Detail for that account:

    1. Standard Account and Account Type
    2. Balance, taken from the Specific Materiality worksheet (6dcda0e)
    3. Performance Materiality
    4. ROMM
    5. Assertion Types
    6. AP Result, taken from Analytical Procedures - Cycle (a3c9d2e)
    7. Timing
    8. Extent
    9. Primary Audit Technique

    Columns 1 to 6 are loaded by the **Detail** button of the worksheet
    and are never edited by hand. Columns 7 to 9 are chosen by the
    auditor while the worksheet is open.
    """

    _name = "general_audit_ws_f9a2c3d.detail"
    _description = "Test of Detail Planning Line (f9a2c3d)"
    _order = "worksheet_id, standard_detail_id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_f9a2c3d",
        required=True,
        ondelete="cascade",
        help="Test of Detail Planning worksheet that owns this line.",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Account",
        comodel_name="general_audit.standard_detail",
        required=True,
        ondelete="restrict",
        help="Standard account of the General Audit planned by this line.",
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        related="standard_detail_id.type_id",
        store=True,
        compute_sudo=True,
        help="Account type of the standard account.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="standard_detail_id.currency_id",
        store=True,
        compute_sudo=True,
        help="Currency of the standard account.",
    )

    # --- Balance and performance materiality ---

    @api.depends(
        "standard_detail_id",
        "worksheet_id.general_audit_id",
    )
    def _compute_balance(self):
        """Take the balance of the Specific Materiality mapping line.

        The balance is the one the Specific Materiality worksheet
        (6dcda0e) uses for the same standard account, so both columns
        share one basis. It is ``0.0`` when no mapping line exists. The
        mapping lives on another model, so the value is refreshed each
        time the **Detail** button recreates the lines.

        :return: nothing; assigns ``balance``
        """
        Mapping = self.env["general_audit_ws_6dcda0e_materiality_mapping"]
        for record in self:
            result = 0.0
            mapping = Mapping.search(record._get_mapping_criteria(), limit=1)
            if mapping:
                result = mapping.balance
            record.balance = result

    balance = fields.Monetary(
        string="Balance",
        currency_field="currency_id",
        compute="_compute_balance",
        store=True,
        compute_sudo=True,
        help=(
            "Balance of the standard account, taken from the Specific "
            "Materiality worksheet (6dcda0e). 0.0 when the account has no "
            "line there."
        ),
    )

    @api.depends(
        "standard_detail_id",
        "worksheet_id.general_audit_id",
    )
    def _compute_performance_materiality(self):
        """Choose the materiality threshold of the standard account.

        The specific materiality of the mapping line is used when
        ``Use Specific Materiality`` is ticked. Otherwise the ``base``
        of the Specific Materiality worksheet (6dcda0e) of the same audit
        is used, which follows the Materiality Type chosen there. The
        mapping and that worksheet live on other models, so the value is
        refreshed each time the **Detail** button recreates the lines.

        :return: nothing; assigns ``performance_materiality``
        """
        Mapping = self.env["general_audit_ws_6dcda0e_materiality_mapping"]
        Worksheet = self.env["general_audit_ws_6dcda0e"]
        for record in self:
            result = 0.0
            mapping = Mapping.search(record._get_mapping_criteria(), limit=1)
            if mapping and mapping.use_specific_materiality:
                result = mapping.specific_materiality
            else:
                worksheet = mapping.worksheet_id or Worksheet.search(
                    record._get_specific_materiality_criteria(), limit=1
                )
                result = worksheet.base
            record.performance_materiality = result

    performance_materiality = fields.Monetary(
        string="Performance Materiality",
        currency_field="currency_id",
        compute="_compute_performance_materiality",
        store=True,
        compute_sudo=True,
        help=(
            "Specific materiality of the account when Use Specific "
            "Materiality is ticked in the Specific Materiality worksheet "
            "(6dcda0e). Otherwise the Balance base of that worksheet."
        ),
    )

    def _get_mapping_criteria(self):
        """Return the domain of the mapping line of this account.

        :return: a domain on the Specific Materiality mapping lines
        """
        self.ensure_one()
        return [
            ("standard_detail_id", "=", self.standard_detail_id.id),
            (
                "worksheet_id.general_audit_id",
                "=",
                self.worksheet_id.general_audit_id.id,
            ),
        ]

    def _get_specific_materiality_criteria(self):
        """Return the domain of the Specific Materiality worksheets.

        :return: a domain limited to the audit of this line
        """
        self.ensure_one()
        return [("general_audit_id", "=", self.worksheet_id.general_audit_id.id)]

    # --- Risk information ---

    romm = fields.Selection(
        string="ROMM",
        related="standard_detail_id.romm",
        store=True,
        compute_sudo=True,
        help=(
            "Risk of material misstatement assessed in the Account Level "
            "ROMM worksheet (d66d87a)."
        ),
    )
    pr_assersion_type_ids = fields.Many2many(
        string="Assersion Types",
        comodel_name="general_audit_assersion_type",
        related="standard_detail_id.pr_assersion_type_ids",
        compute_sudo=True,
        help=(
            "Assertion types of the standard account, as set in the "
            "Account Level ROMM worksheet (d66d87a)."
        ),
    )

    @api.depends("standard_detail_id.analytical_procedures_cycle_result")
    def _compute_ap_result(self):
        """Read the result of the Analytical Procedures - Cycle worksheet.

        :return: nothing; assigns ``ap_result``, ``none`` when empty
        """
        for record in self:
            result = "none"
            cycle_result = record.standard_detail_id.analytical_procedures_cycle_result
            if cycle_result:
                result = cycle_result
            record.ap_result = result

    ap_result = fields.Selection(
        string="AP Result",
        selection=[
            ("high", "High"),
            ("moderate", "Moderate"),
            ("none", "None"),
        ],
        compute="_compute_ap_result",
        store=True,
        compute_sudo=True,
        help=(
            "Result of the Analytical Procedures - Cycle worksheet "
            "(a3c9d2e) for this account. None when it has no result."
        ),
    )

    # --- Planning chosen by the auditor ---

    timing_id = fields.Many2one(
        string="Timing",
        comodel_name="general_audit_ws_f9a2c3d_timing",
        ondelete="restrict",
        help="When the Test of Detail is performed.",
    )
    extent_id = fields.Many2one(
        string="Extent",
        comodel_name="general_audit_ws_f9a2c3d_extent",
        ondelete="restrict",
        help="How much of the account population is tested.",
    )
    technique_ids = fields.Many2many(
        string="Primary Audit Technique",
        comodel_name="general_audit_ws_f9a2c3d_technique",
        relation="rel_ga_ws_f9a2c3d_detail_2_technique",
        column1="detail_id",
        column2="technique_id",
        help="Audit techniques used for the test. More than one may be chosen.",
    )
