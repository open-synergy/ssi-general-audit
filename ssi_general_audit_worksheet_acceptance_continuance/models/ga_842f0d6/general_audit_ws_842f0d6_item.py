# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS842f0d6Item(models.Model):
    _name = "general_audit_ws_842f0d6.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Money Laudring Issues (842f0d6) - " "Checklist Item"

    code = fields.Char(
        default="/",
    )
