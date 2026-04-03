# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc8740d4Item(models.Model):
    """
    Checklist item master for the Preliminary Analytic Procedure Summary (c8740d4).

    Each item represents a **single procedure step** that the auditor must
    confirm has been performed as part of the preliminary analytical procedure
    phase (e.g., “Vertical and horizontal analysis has been completed and
    reviewed”, “All significant fluctuations exceeding materiality threshold
    have been investigated”).
    """

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
