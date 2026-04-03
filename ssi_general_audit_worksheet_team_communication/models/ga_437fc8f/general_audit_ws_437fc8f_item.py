# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS437fc8fItem(models.Model):
    """Master item definition for Team Communication Pre-Engagement checklist.

    Defines the standard audit checklist items to be evaluated in the
    ``general_audit_ws_437fc8f`` worksheet. Items are seeded from master data
    and categorized by ``communication_type`` to distinguish pre-engagement
    understanding matters from in-engagement consultations.

    This master list is shared across all audit engagements. Auditors respond
    to each item in ``general_audit_ws_437fc8f.checklist`` per engagement.

    Inherits from ``mixin.checklist.item`` for consistent item management.
    """

    _name = "general_audit_ws_437fc8f.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Team Communication Pre-Engagement (437fc8f) - " "Checklist Item"

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
