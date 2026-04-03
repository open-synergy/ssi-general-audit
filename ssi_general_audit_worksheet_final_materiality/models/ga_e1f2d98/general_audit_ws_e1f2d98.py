# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSe1f2d98(models.Model):
    """
    WS.080.3 — Final Analytical Procedures — Vertical and Horizontal
    Analysis (e1f2d98)

    Implements the quantitative **vertical and horizontal analysis**
    component of the final analytical procedures, as required by ISA 520 /
    SA 520.  This worksheet is linked to the corresponding Preliminary
    Analytic Procedure worksheet (``general_audit_ws_b32655a``) from the
    planning phase, loading the same line items and adding audited-
    period figures for comparison.

    For each line item the worksheet records:

    - **Vertical analysis** (common-size %) for the previous, end-period,
      and audited trial balances.
    - **Horizontal analysis** (period-over-period Δ%) comparing previous
      to end-period and previous to audited amounts.
    - Whether each line warrants attention (inherited from the preliminary
      worksheet but updatable by the auditor).
    - A free-text explanation for lines flagged as requiring attention.

    Total asset and total revenue amounts are computed automatically from
    the General Audit computation records to serve as base figures for
    the vertical analysis denominators.

    **ISA / SA references:** ISA 520 / SA 520 — Analytical Procedures
    """

    _name = "general_audit_ws_e1f2d98"
    _description = (
        "Final Analytical Procedures (e1f2d98) - " "Vertical and Horisontal Analysis"
    )
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_final_materiality." "worksheet_type_e1f2d98"
    )

    ws_b32655a_id = fields.Many2one(
        string="# Preliminary Analytic Procedure",
        comodel_name="general_audit_ws_b32655a",
        readonly=True,
        required=False,
        ondelete="restrict",
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help=(
            "Reference to the Preliminary Analytic Procedure worksheet "
            "used to generate this Final Analytical Procedures worksheet."
        ),
    )
    analysis_ids = fields.One2many(
        string="Analysis",
        comodel_name="general_audit_ws_e1f2d98.vertical_horizontal_analysis",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Vertical and horizontal analysis lines generated from the General "
            "Audit standard details."
        ),
    )

    @api.depends(
        "general_audit_id",
        "general_audit_id.computation_ids",
        "general_audit_id.computation_ids.audited_amount",
        "general_audit_id.computation_ids.home_amount",
        "general_audit_id.computation_ids.previous_amount",
    )
    def _compute_total_asset_revenue(self):
        company = self.env.company
        ta_item_id = (
            company.ta_computation_item_id
            and company.ta_computation_item_id.id
            or False
        )
        tr_item_id = (
            company.tr_computation_item_id
            and company.tr_computation_item_id.id
            or False
        )
        for record in self:
            end_period_ta = (
                end_period_tr
            ) = audited_ta = audited_tr = previous_ta = previous_tr = 0.0
            if ta_item_id:
                end_period_ta = record.general_audit_id.computation_ids.filtered(
                    lambda x: x.computation_item_id.id == ta_item_id
                ).home_amount
                audited_ta = record.general_audit_id.computation_ids.filtered(
                    lambda x: x.computation_item_id.id == ta_item_id
                ).audited_amount
                previous_ta = record.general_audit_id.computation_ids.filtered(
                    lambda x: x.computation_item_id.id == ta_item_id
                ).previous_amount
            if tr_item_id:
                end_period_tr = record.general_audit_id.computation_ids.filtered(
                    lambda x: x.computation_item_id.id == tr_item_id
                ).home_amount
                audited_tr = record.general_audit_id.computation_ids.filtered(
                    lambda x: x.computation_item_id.id == tr_item_id
                ).audited_amount
                previous_tr = record.general_audit_id.computation_ids.filtered(
                    lambda x: x.computation_item_id.id == tr_item_id
                ).previous_amount

            record.previous_total_asset = previous_ta
            record.previous_total_revenue = previous_tr
            record.end_period_total_asset = end_period_ta
            record.end_period_total_revenue = end_period_tr
            record.audited_total_asset = audited_ta
            record.audited_total_revenue = audited_tr

    previous_total_asset = fields.Monetary(
        string="Total Asset (Previous)",
        compute="_compute_total_asset_revenue",
        compute_sudo=True,
        store=True,
        help="Total asset amount from the previous trial balance.",
    )
    previous_total_revenue = fields.Monetary(
        string="Total Revenue (Previous)",
        compute="_compute_total_asset_revenue",
        compute_sudo=True,
        store=True,
        help="Total revenue amount from the previous trial balance.",
    )
    end_period_total_asset = fields.Monetary(
        string="Total Asset (End Period)",
        compute="_compute_total_asset_revenue",
        compute_sudo=True,
        store=True,
        help="Total asset amount from the end period trial balance.",
    )
    end_period_total_revenue = fields.Monetary(
        string="Total Revenue (End Period)",
        compute="_compute_total_asset_revenue",
        compute_sudo=True,
        store=True,
        help="Total revenue amount from the end period trial balance.",
    )
    audited_total_asset = fields.Monetary(
        string="Total Asset (Audited)",
        compute="_compute_total_asset_revenue",
        compute_sudo=True,
        store=True,
        help="Total asset amount from the audited trial balance.",
    )
    audited_total_revenue = fields.Monetary(
        string="Total Revenue (Audited)",
        compute="_compute_total_asset_revenue",
        compute_sudo=True,
        store=True,
        help="Total revenue amount from the audited trial balance.",
    )

    def action_load_analysis(self):
        for record in self.sudo():
            record._load_analysis()

    def _load_analysis(self):
        self.ensure_one()
        criteria = [
            ("worksheet_id", "=", self.ws_b32655a_id.id),
        ]
        all_details = self.env[
            "general_audit_ws_b32655a.vertical_horizontal_analysis"
        ].search(criteria)
        exiting_details = self.analysis_ids.mapped("prelim_analysis_id")

        to_adds = all_details - exiting_details
        to_removes = exiting_details - all_details

        for to_add in to_adds:
            self.env["general_audit_ws_e1f2d98.vertical_horizontal_analysis"].create(
                {
                    "worksheet_id": self.id,
                    "prelim_analysis_id": to_add.id,
                    "industry_average": to_add.industry_average,
                    "vertical_need_attention": to_add.vertical_need_attention,
                    "horizontal_need_attention": to_add.horizontal_need_attention,
                    "explanation": to_add.explanation,
                }
            )

        for to_remove in to_removes:
            line = self.analysis_ids.filtered(
                lambda x: x.prelim_analysis_id.id == to_remove.id
            )
            line.sudo().unlink()
