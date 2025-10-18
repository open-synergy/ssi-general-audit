# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc165170(models.Model):
    _name = "general_audit_ws_c165170"
    _description = "Financial Level ROMM (c165170)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_romm." "worksheet_type_c165170"

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
        help=(
            "Overall financial statement-level risk of material misstatement (ROMM) "
            "assessment for this worksheet."
        ),
    )
    auditor_respons = fields.Text(
        string="Auditor Respons",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Summary of the auditor's planned overall responses at the financial "
            "statement level to address the assessed ROMM."
        ),
    )
