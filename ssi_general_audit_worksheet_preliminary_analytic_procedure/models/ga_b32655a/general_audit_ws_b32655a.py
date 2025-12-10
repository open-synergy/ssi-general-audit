# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSb32655a(models.Model):
    _name = "general_audit_ws_b32655a"
    _description = (
        "Preliminary Analytic Procedure - Vertical and Horizontal Analysis (b32655a)"
    )
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_preliminary_analytic_procedure."
        "worksheet_type_b32655a"
    )

    base_amount_source = fields.Selection(
        string="Balance Type",
        selection=[
            ("extrapolation", "Extrapolation"),
            ("end_period", "End Period"),
        ],
        required=False,
        default="extrapolation",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help=(
            "Select which balance to use for current figures: Extrapolation "
            "(forecasted) or End Period (actual)."
        ),
    )

    analysis_ids = fields.One2many(
        string="Analysis",
        comodel_name="general_audit_ws_b32655a.vertical_horizontal_analysis",
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
        "base_amount_source",
        "general_audit_id",
        "general_audit_id.computation_ids",
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
            ta = tr = 0.0
            if record.base_amount_source == "extrapolation":
                if ta_item_id:
                    ta = record.general_audit_id.computation_ids.filtered(
                        lambda x: x.computation_item_id.id == ta_item_id
                    ).extrapolation_amount
                if tr_item_id:
                    tr = record.general_audit_id.computation_ids.filtered(
                        lambda x: x.computation_item_id.id == tr_item_id
                    ).extrapolation_amount
            else:
                if ta_item_id:
                    ta = record.general_audit_id.computation_ids.filtered(
                        lambda x: x.computation_item_id.id == ta_item_id
                    ).home_amount
                if tr_item_id:
                    tr = record.general_audit_id.computation_ids.filtered(
                        lambda x: x.computation_item_id.id == tr_item_id
                    ).home_amount
            record.total_asset = ta
            record.total_revenue = tr

    total_asset = fields.Float(
        string="Total Asset",
        compute="_compute_total_asset_revenue",
        compute_sudo=True,
        store=True,
        help=(
            "Total Assets used as the base figure depending on Balance Type "
            "(Extrapolation or End Period)."
        ),
    )

    total_revenue = fields.Float(
        string="Total Revenue",
        compute="_compute_total_asset_revenue",
        compute_sudo=True,
        store=True,
        help=(
            "Total Revenue used as the base figure depending on Balance Type "
            "(Extrapolation or End Period)."
        ),
    )

    def action_reload_analysis_ids(self):
        for record in self.sudo():
            record._reload_analysis_ids()
            record.analysis_ids._compute_computation_item()

    def _reload_analysis_ids(self):
        Detail = self.env["general_audit_ws_b32655a.vertical_horizontal_analysis"]

        standard_detail = self.general_audit_id.standard_detail_ids
        mapping = {chk.standard_detail_id.id: chk for chk in self.analysis_ids}
        for detail in standard_detail:
            if detail.id not in mapping:
                Detail.create(
                    {
                        "worksheet_id": self.id,
                        "standard_detail_id": detail.id,
                    }
                )

        standard_detail_ids = set(standard_detail.ids)
        for chk in self.analysis_ids:
            if chk.standard_detail_id.id not in standard_detail_ids:
                chk.unlink()

    @api.onchange("general_audit_id")
    def onchange_analysis_ids(self):
        self.update({"analysis_ids": [(5, 0, 0)]})
        if self.general_audit_id:
            result = []
            for detail in self.general_audit_id.standard_detail_ids:
                result.append(
                    (
                        0,
                        0,
                        {
                            "standard_detail_id": detail.id,
                        },
                    )
                )
            self.update({"analysis_ids": result})

    @ssi_decorator.pre_confirm_check()
    def _10_check_balance_type(self):
        self.ensure_one()
        criteria = [
            ("general_audit_id", "=", self.general_audit_id.id),
            ("type_id", "=", self.type_id.id),
            ("base_amount_source", "=", self.base_amount_source),
            ("id", "!=", self.id),
        ]
        check = self.search(criteria)
        if check:
            error_message = """
            Context: Confirmation for %s
            Database ID: %s
            Problem: Balance type %s is already used for General Audit %s.
            """ % (
                self.type_id.name,
                self.id,
                self.base_amount_source,
                self.name,
            )
            raise ValidationError(_(error_message))
