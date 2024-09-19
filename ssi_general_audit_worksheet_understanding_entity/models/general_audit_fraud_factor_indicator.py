# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditFraudFactorIndicator(models.Model):
    _name = "general_audit_fraud_factor_indicator"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Fraud Factor Indicator"
    _order = "category_id, factor_id, sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    factor_id = fields.Many2one(
        string="Factor",
        comodel_name="general_audit_fraud_factor",
        required=True,
    )
    category_id = fields.Many2one(
        related="factor_id.category_id",
        store=True,
    )
