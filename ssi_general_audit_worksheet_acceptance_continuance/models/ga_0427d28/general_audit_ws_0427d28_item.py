# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS369c5a5Item(models.Model):
    _name = "general_audit_ws_369c5a5.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Previous Financial Reporting Issues (369c5a5) - " "Checklist Item"

    code = fields.Char(
        default="/",
    )
