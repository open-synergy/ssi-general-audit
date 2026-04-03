# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WS230AccountAssersionLevelRomm(models.Model):
    """
    Account / Assertion Level ROMM line for the legacy ROMM worksheet (ws_ra230).

    .. deprecated::
        This detail model belongs to the legacy ``ws_ra230`` worksheet.  New
        implementations should use ``general_audit_ws_d66d87a.detail``.

    Each record captures the assessment of ROMM at the account and assertion
    level for one standard detail.  Includes assertion types for both
    transaction-level and Presentation & Disclosure (P&D) assertions,
    overall ROMM, and planned audit response flags.  Values are
    synchronised with the parent ``standard_detail`` record via
    ``_inverse_to_standard_detail``.
    """

    _name = "ws_ra230.account_assersion_level_romm"
    _description = "General Audit - Account Assersion Level ROMM"

    worksheet_id = fields.Many2one(
        string="# RA.210",
        comodel_name="ws_ra230",
        required=True,
        ondelete="cascade",
        help=(
            "The worksheet that owns this line. Deleting the worksheet will "
            "remove its lines."
        ),
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="accountant.general_audit_standard_detail",
        required=True,
        ondelete="restrict",
        help=("Standard detail referenced by this line."),
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
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
    sequence = fields.Integer(
        string="Sequence",
        related="standard_detail_id.sequence",
        store=True,
        help=("Display sequence derived from the standard detail."),
    )
    pr_assersion_type_ids = fields.Many2many(
        string="Assersion Types on Presentation and Disclosure",
        comodel_name="accountant.assersion_type",
        relation="rel_ra230_2_pr_assersion_type",
        column1="standard_detail_id",
        column2="assersion_type_id",
        inverse="_inverse_to_standard_detail",
        help=(
            "Presentation & Disclosure (P&D) assertion types applicable to this "
            "standard detail. Values are synchronized with the standard detail."
        ),
    )
    romm = fields.Selection(
        string="Risk Material Misstatement",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        related="standard_detail_id.romm",
        readonly=False,
        store=True,
        help=(
            "Assessed ROMM for the standard detail; editable here and stored on the "
            "standard detail."
        ),
    )
    planned_response_analytic_procedure = fields.Boolean(
        string="Planned Response Analytic Procedure",
        default=False,
        related="standard_detail_id.planned_response_analytic_procedure",
        readonly=False,
        store=True,
        help=(
            "Indicates that analytical procedures are planned; value is stored on the "
            "standard detail."
        ),
    )
    planned_response_tod = fields.Boolean(
        string="Planned Response ToD",
        default=False,
        related="standard_detail_id.planned_response_tod",
        readonly=False,
        store=True,
        help=(
            "Indicates that tests of details (ToD) are planned; value is stored on the "
            "standard detail."
        ),
    )
    planned_response_interim = fields.Boolean(
        string="Planned Response on Interim",
        default=False,
        related="standard_detail_id.planned_response_interim",
        readonly=False,
        store=True,
        help=(
            "Indicates that interim timing is planned; value is stored on the standard detail."
        ),
    )
    planned_response_ye = fields.Boolean(
        string="Planned Response on Year End",
        default=False,
        related="standard_detail_id.planned_response_ye",
        readonly=False,
        store=True,
        help=(
            "Indicates that year-end timing is planned; value is stored on the standard detail."
        ),
    )

    def _inverse_to_standard_detail(self):
        for record in self:
            record.standard_detail_id.write(
                {
                    "pr_assersion_type_ids": [(6, 0, record.pr_assersion_type_ids.ids)],
                }
            )
