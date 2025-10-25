# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditInherentRiskFactor(models.Model):
    _name = "general_audit_inherent_risk_factor"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Inherent Risk Factor"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Display order of the inherent risk factor in lists and reports.",
    )
    direct_impact = fields.Boolean(
        string="Direct Impact to Risk",
        default=False,
        help="""If enabled, this factor directly affects the inherent risk assessment.
Used to differentiate factors with and without direct impact in worksheets.""",
    )
