# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb1f820cItem(models.Model):
    """Master item definition for Team Communication Risk Assessment checklist.

    Defines the standard audit checklist items used in the
    ``general_audit_ws_b1f820c`` worksheet. Items express risk areas and
    communication requirements per ISA 315 and ISA 240, and are classified
    by ``communication_type`` to differentiate entity understanding discussions
    from specialist consultations.

    This master list is shared across all audit engagements. Auditors respond
    to each item in ``general_audit_ws_b1f820c.checklist`` per engagement.

    Inherits from ``mixin.checklist.item``.
    """

    _name = "general_audit_ws_b1f820c.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Team Communication Risk Assessment (b1f820c) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help=(
            "Unique identifier code for this checklist item. "
            "Used for reference and organization purposes."
        ),
    )
    communication_type = fields.Selection(
        string="Type of Communication",
        selection=[
            ("understanding", "Engagement Team Understanding"),
            ("consultation", "Consultation during the Engagement"),
        ],
        required=True,
        help=(
            "Specifies the communication category for this checklist item. "
            "Choose 'Engagement Team Understanding' for pre-engagement understanding, "
            "or 'Consultation during the Engagement' for consultations "
            "held during the engagement."
        ),
    )
