# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS806c4e1Item(models.Model):
    _name = "general_audit_ws_806c4e1.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = (
        "Acceptance and Continuance of "
        "Client Relationships Analysis (806c4e1) - Item"
    )

    code = fields.Char(
        default="/",
        help="Internal code/identifier for the checklist item. Defaults to '/'.",
    )
