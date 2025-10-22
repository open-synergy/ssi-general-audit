# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class ClientRelevantAccountType(models.Model):
    _name = "client_relevant_account_type"
    _inherit = ["mixin.master_data"]
    _description = "Relevant Accounting Standards"
    _order = "sequence, id"
    _show_code_on_display_name = False

    code = fields.Char(
        default="/",
        help="Unique short code for the team role. Use '/' to auto-generate.",
    )

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Ordering of the account type.",
    )
