# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditFraudFactorCategory(models.Model):
    _name = "general_audit_fraud_factor_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Fraud Factor Category"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
