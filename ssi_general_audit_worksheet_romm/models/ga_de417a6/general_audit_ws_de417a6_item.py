# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSde417a6Item(models.Model):
    """
    Checklist item master for the ROMM Checklist (de417a6).

    Each item represents a **single risk assessment procedure step** that
    the auditor must confirm has been completed as part of the risk
    identification and assessment process required by ISA 315 / SA 315.
    """

    _name = "general_audit_ws_de417a6.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "ROMM (de417a6) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help=(
            "Optional code or reference for the checklist item. Use '/' to auto-number "
            "or let the system assign a code."
        ),
    )
