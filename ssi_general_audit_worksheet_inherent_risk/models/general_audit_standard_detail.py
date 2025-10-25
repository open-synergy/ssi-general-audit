# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import fields, models


class GeneralAuditStandardDetail(models.Model):
    _name = "general_audit.standard_detail"
    _inherit = ["general_audit.standard_detail"]

    inherent_risk = fields.Selection(
        string="Inherent Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        help="Assessed level of inherent risk for this standard detail (low/medium/high).",
    )
    significant_risk = fields.Boolean(
        string="Significant Risk",
        help=(
            "Indicates whether this standard detail is considered a "
            "significant risk for audit planning and procedures."
        ),
    )
