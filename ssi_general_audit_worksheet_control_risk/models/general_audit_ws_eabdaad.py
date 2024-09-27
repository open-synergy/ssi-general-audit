# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSEABDAAD(models.Model):
    _name = "general_audit_ws_eabdaad"
    _description = "Business Cycle Internal Control (eabdaad)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_control_risk." "worksheet_type_eabdaad"

    business_cycle_id = fields.Many2one(
        string="Business Cycle",
        comodel_name="client_business_process",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    allowed_business_cycle_ids = fields.Many2many(
        string="Allowed Business Cycles",
        related="general_audit_id.business_cycle_ids",
        store=False,
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_eabdaad.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
