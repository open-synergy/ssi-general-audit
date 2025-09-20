# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS09253feItem(models.Model):
    _name = "general_audit_ws_09253fe.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Independence Statement (09253fe) - " "Checklist Item"

    code = fields.Char(
        default="/",
    )
