# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSae48e68Item(models.Model):
    _name = "general_audit_ws_ae48e68.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "External Communication (ae48e68) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help=(
            "Short code or identifier for the checklist item. "
            "Defaults to '/'; it may be replaced by a generated value."
        ),
    )
