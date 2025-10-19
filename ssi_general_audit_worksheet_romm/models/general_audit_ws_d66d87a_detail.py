# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd66d87aDetail(models.Model):
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

    pr_assersion_type_ids = fields.Many2many(
        string="Assersion Types on Presentation and Disclosure",
        related="standard_detail_id.pr_assersion_type_ids",
        inverse="_inverse_to_standard_detail",
        help=(
            "Presentation & Disclosure (P&D) assertion types inherited from the "
            "standard detail. Changes here will be synchronized back to the standard detail."
        ),
    )
    romm = fields.Selection(
        string="Risk Material Misstatement",
        related="standard_detail_id.romm",
        readonly=False,
        store=True,
        help=(
            "Assessed ROMM for this standard detail and assertion; editable here and "
            "stored on the standard detail."
        ),
    )
    planned_response_toc = fields.Boolean(
        string="Planned Response TOC",
        default=False,
        related="standard_detail_id.planned_response_toc",
        readonly=False,
        store=True,
        help=(
            "Indicates that tests of controls (ToC) are planned based on the ROMM assessment."
        ),
    )
    planned_response_analytic_procedure = fields.Boolean(
        string="Planned Response Analytic Procedure",
        default=False,
        related="standard_detail_id.planned_response_analytic_procedure",
        readonly=False,
        store=True,
        help=(
            "Indicates that analytical procedures are planned based on the ROMM assessment."
        ),
    )
    planned_response_tod = fields.Boolean(
        string="Planned Response ToD",
        default=False,
        related="standard_detail_id.planned_response_tod",
        readonly=False,
        store=True,
        help=(
            "Indicates that tests of details (ToD) are planned based on the ROMM assessment."
        ),
    )
    planned_response_interim = fields.Boolean(
        string="Planned Response on Interim",
        default=False,
        related="standard_detail_id.planned_response_interim",
        readonly=False,
        store=True,
        help=("Planned timing includes the interim period."),
    )
    planned_response_ye = fields.Boolean(
        string="Planned Response on Year End",
        default=False,
        related="standard_detail_id.planned_response_ye",
        readonly=False,
        store=True,
        help=("Planned timing includes year-end procedures."),
    )

    def _inverse_to_standard_detail(self):
        for record in self:
            record.standard_detail_id.write(
                {
                    "pr_assersion_type_ids": [(6, 0, record.pr_assersion_type_ids.ids)],
                }
            )
