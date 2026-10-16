# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWsA8c54f3Item(models.Model):
    """
    Checklist item master for Audit Final Memorandum (a8c54f3).

    Master-data model for the review checklist items used in the Audit
    Final Memorandum worksheet. Grouped by
    ``general_audit_ws_a8c54f3.category``. The default checklist is
    shipped as module data.
    """

    _name = "general_audit_ws_a8c54f3.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Audit Final Memorandum (a8c54f3) - Checklist Item"

    code = fields.Char(
        default="/",
        help="Item code or number. Use '/' to auto-generate the code.",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_ws_a8c54f3.category",
        help="Category used to group items on the checklist.",
        ondelete="restrict",
    )
