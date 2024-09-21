# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSF63F569(models.Model):
    _name = "general_audit_ws_f63f569"
    _description = "General Control Evaluation (f63f569)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_control_risk." "worksheet_type_f63f569"

    set_id = fields.Many2one(
        string="General Control Set",
        comodel_name="general_audit_general_control_set",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_f63f569.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    indicator_ids = fields.One2many(
        string="Indicators",
        comodel_name="general_audit_ws_f63f569.indicator",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @ssi_decorator.post_open_action()
    def _01_compute_detail(self):
        self.detail_ids.unlink()
        Detail = self.env["general_audit_ws_f63f569.detail"]
        Indicator = self.env["general_audit_ws_f63f569.indicator"]
        general_control_set = self.set_id
        for control in general_control_set.general_control_ids:
            data = {
                "worksheet_id": self.id,
                "control_id": control.id,
            }
            detail = Detail.create(data)
            for indicator in general_control_set.general_control_indicator_ids.filtered(
                lambda r: r.control_id.id == control.id
            ):
                data = {
                    "detail_id": detail.id,
                    "indicator_id": indicator.id,
                }
                Indicator.create(data)
