# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa033cc6Item(models.Model):
    """Master item definition for the Trial Balance checklist.

    Defines the standard verification checkpoints used in the
    ``general_audit_ws_a033cc6`` (Trial Balance) worksheet. These items
    represent audit procedures required when reviewing the trial balance,
    such as verifying footings, agree-to-general-ledger checks, opening
    balance rollforwards, and audit adjustment tracking.

    This master list is shared across all audit engagements. Auditors complete
    each item per engagement through ``general_audit_ws_a033cc6.checklist``.

    Inherits from ``mixin.checklist.item``.
    """

    _name = "general_audit_ws_a033cc6.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Trial Balance (a033cc6) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help=(
            "Unique identifier code for this trial balance checklist item. "
            "Used for reference and organization of audit procedures."
        ),
    )
