# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditFraudFactor(models.Model):
    """Master: Fraud Factor.

    Defines the fraud factors (conditions) to be assessed during the audit's
    fraud risk evaluation per ISA 240 / SA 240. Each factor belongs to a
    category aligned to the fraud triangle (incentives/pressures, opportunities,
    rationalizations). Factors group sets of specific fraud indicators
    (``general_audit_fraud_factor_indicator``) used in the Fraud Factor
    Analysis worksheet (c0e0eec).
    """

    _name = "general_audit_fraud_factor"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Fraud Factor"
    _order = "category_id, sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_fraud_factor_category",
        ondelete="restrict",
        required=True,
    )
