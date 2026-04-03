# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class AccountingApplication(models.Model):
    """Master: Accounting Application.

    Reference list of accounting software and information systems used by
    audit clients to process transactions and prepare financial statements.
    Used in the Main Business Activity worksheet (ae11f7e) to document the
    entity's IT environment as part of ISA 315 entity understanding.
    """

    _name = "accounting_application"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accounting Application"

    code = fields.Char(
        default="/",
    )
