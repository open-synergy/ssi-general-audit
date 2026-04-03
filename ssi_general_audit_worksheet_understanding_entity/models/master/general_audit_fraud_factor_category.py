# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditFraudFactorCategory(models.Model):
    """Master: Fraud Factor Category.

    Top-level categorisation of fraud risk factors aligned to the fraud
    triangle concept from ISA 240 / SA 240:
    - Incentives/Pressures: motivations to commit fraud
    - Opportunities: circumstances enabling fraud
    - Attitudes/Rationalizations: justifications for fraudulent behaviour

    Categories group ``general_audit_fraud_factor`` records and are used to
    structure the Fraud Factor Analysis worksheet (c0e0eec).
    """

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
