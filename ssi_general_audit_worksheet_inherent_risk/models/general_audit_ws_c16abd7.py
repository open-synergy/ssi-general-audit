# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc16abd7(models.Model):
    _name = "general_audit_ws_c16abd7"
    _description = "Financial Statement Level Inherent Risk (c16abd7)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_inherent_risk." "worksheet_type_c16abd7"

    risk_material_missstatement = fields.Selection(
        string="Risk Material Misstatement",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    auditor_respons = fields.Text(
        string="Auditor Respons",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
