# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSfc75636Category(models.Model):
    _name = "general_audit_ws_fc75636.category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Independen Auditor Report (fc75636) - " "Category"

    code = fields.Char(
        default="/",
        help="Unique short code for the team role. Use '/' to auto-generate.",
    )
