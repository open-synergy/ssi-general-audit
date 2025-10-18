# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class AccountingApplication(models.Model):
    _name = "accounting_application"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accounting Application"

    code = fields.Char(
        default="/",
    )
