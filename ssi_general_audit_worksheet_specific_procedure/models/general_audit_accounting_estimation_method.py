# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditAccountingEstimationMethod(models.Model):
    _name = "general_audit_accounting_estimation_method"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Accounting Estimation Method"

    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Standard Account",
        required=True,
        ondelete="restrict",
    )
