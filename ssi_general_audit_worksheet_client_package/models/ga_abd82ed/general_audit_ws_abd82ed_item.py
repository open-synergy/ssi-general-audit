# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSabd82edItem(models.Model):
    """Checklist item master for the Client Assistance Package worksheet (abd82ed).

    Defines the individual items (documents or data files) that the client must
    provide.  These drive the checklist lines (``general_audit_ws_abd82ed.checklist``)
    auto-created on each worksheet instance via ``mixin.checklist``.
    """

    _name = "general_audit_ws_abd82ed.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Client Assistance Package (abd82ed) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help=(
            "Internal code for the checklist item. "
            "Keep '/' to auto-generate if applicable."
        ),
    )
