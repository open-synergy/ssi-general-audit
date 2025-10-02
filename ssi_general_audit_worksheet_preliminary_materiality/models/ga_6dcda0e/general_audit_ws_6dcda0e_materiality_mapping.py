# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class GeneralAuditWS6dcda0e1MaterialityMapping(models.Model):
    _name = "general_audit_ws_6dcda0e_materiality_mapping"
    _description = "General Audit WS 6DCDA0E1 - Materiality Mapping"
    _order = "sequence, worksheet_id, id"

    @api.depends(
        "balance",
        "worksheet_id.materiality_type",
        "use_specific_materiality",
        "specific_materiality",
        "worksheet_id.worksheet_d9d2b44_id.overall_materiality",
        "worksheet_id.worksheet_d9d2b44_id.performance_materiality",
        "standard_detail_id",
    )
    def _compute_materiality(self):
        for document in self:
            materiality = "im"
            base = balance = 0.0
            worksheet = document.worksheet_id

            if worksheet.worksheet_d9d2b44_id:
                worksheet_d9d2b44 = worksheet.worksheet_d9d2b44_id

                if worksheet_d9d2b44.base_amount_source == "interim":
                    balance = document.standard_detail_id.interim_balance
                elif worksheet_d9d2b44.base_amount_source == "extrapolation":
                    balance = document.standard_detail_id.adjusted_extrapolation_balance
                elif worksheet_d9d2b44.base_amount_source == "home":
                    balance = document.standard_detail_id.home_statement_balance

                if worksheet.materiality_type == "om":
                    base = worksheet_d9d2b44.overall_materiality
                else:
                    base = worksheet_d9d2b44.performance_materiality

                if abs(balance) >= base:
                    materiality = "m"

                document.materiality = materiality

                if document.use_specific_materiality:
                    materiality = "m"

            document.final_materiality = materiality
            document.balance = balance

    worksheet_id = fields.Many2one(
        string="# WS-6DDDA0E",
        comodel_name="general_audit_ws_6dcda0e",
        required=True,
        ondelete="cascade",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="general_audit.standard_detail",
        required=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="standard_detail_id.currency_id",
        store=True,
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        related="standard_detail_id.type_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="standard_detail_id.sequence",
        store=True,
    )
    balance = fields.Monetary(
        string="Balance",
        compute="_compute_materiality",
        related=False,
        store=True,
        currency_field="currency_id",
    )
    materiality = fields.Selection(
        string="Materiality",
        selection=[("m", "Material"), ("im", "Immaterial")],
        compute="_compute_materiality",
        store=True,
    )
    use_specific_materiality = fields.Boolean(
        string="Use Specific Materiality",
        default=False,
    )
    specific_materiality = fields.Monetary(
        string="Specific Materiality",
        required=True,
        default=0.0,
        currency_field="currency_id",
    )
    final_materiality = fields.Selection(
        string="Final Materiality",
        selection=[("m", "Material"), ("im", "Immaterial")],
        compute="_compute_materiality",
        store=True,
    )
    specific_materiality_reason = fields.Text(
        string="Specific Materiality Reason",
    )
