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
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="general_audit.standard_detail",
        required=True,
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        related="standard_detail_id.type_id",
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="standard_detail_id.currency_id",
        store=True,
    )
    pr_assersion_type_ids = fields.Many2many(
        string="Assersion Types on Presentation and Disclosure",
        related="standard_detail_id.pr_assersion_type_ids",
        inverse="_inverse_to_standard_detail",
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
    )
    planned_response_analytic_procedure = fields.Boolean(
        string="Planned Response Analytic Procedure",
        default=False,
        related="standard_detail_id.planned_response_analytic_procedure",
        readonly=False,
        store=True,
    )
    planned_response_tod = fields.Boolean(
        string="Planned Response ToD",
        default=False,
        related="standard_detail_id.planned_response_tod",
        readonly=False,
        store=True,
    )
    planned_response_interim = fields.Boolean(
        string="Planned Response on Interim",
        default=False,
        related="standard_detail_id.planned_response_interim",
        readonly=False,
        store=True,
    )
    planned_response_ye = fields.Boolean(
        string="Planned Response on Year End",
        default=False,
        related="standard_detail_id.planned_response_ye",
        readonly=False,
        store=True,
    )

    def _inverse_to_standard_detail(self):
        for record in self:
            record.standard_detail_id.write(
                {
                    "pr_assersion_type_ids": [(6, 0, record.pr_assersion_type_ids.ids)],
                }
            )
