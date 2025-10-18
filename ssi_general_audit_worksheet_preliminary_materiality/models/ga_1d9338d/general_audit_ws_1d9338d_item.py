# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS1d9338dItem(models.Model):
    _name = "general_audit_ws_1d9338d.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Preliminary Materiality (1d9338d) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help=(
            "Technical code/reference for the checklist item. Use '/' to "
            "let the system generate a code."
        ),
    )
