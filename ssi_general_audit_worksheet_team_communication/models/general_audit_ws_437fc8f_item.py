# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS437fc8fItem(models.Model):
    _name = "general_audit_ws_437fc8f.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Team Communication (437fc8f) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help=(
            "Unique identifier code for this checklist item. "
            "Used for reference and organization purposes."
        ),
    )
