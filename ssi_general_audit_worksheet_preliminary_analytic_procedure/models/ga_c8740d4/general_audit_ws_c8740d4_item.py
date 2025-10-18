# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc8740d4Item(models.Model):
    _name = "general_audit_ws_c8740d4.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Preliminary Analytic Procedure (c8740d4) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help=(
            "Short code of the checklist item. The default '/' can be "
            "replaced by an automatically generated sequence or custom code."
        ),
    )
