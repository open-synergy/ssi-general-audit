# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSe301171Item(models.Model):
    """Checklist item master for the Journal Entry Testing worksheet (e301171).

    Defines one journal-entry testing procedure step.  These items drive the
    auto-populated checklist lines on each worksheet instance and can be
    maintained centrally to reflect changes in the firm's testing methodology
    or updates to ISA 240 / SA 240 guidance.
    """

    _name = "general_audit_ws_e301171.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Journal Entry Testing (e301171) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help=(
            "Internal code for the checklist item. "
            "Keep '/' to auto-generate if applicable."
        ),
    )
