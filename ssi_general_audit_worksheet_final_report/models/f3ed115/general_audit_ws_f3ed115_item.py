# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWsF3ed115Item(models.Model):
    """
    Checklist item master for Final Communication With TCWG (f3ed115).

    Master-data model for the checklist items used in the Final
    Communication With TCWG worksheet. Grouped by
    ``general_audit_ws_f3ed115.category``. Content is intentionally
    left empty until the checklist is formulated by the user.
    """

    _name = "general_audit_ws_f3ed115.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Final Communication With TCWG (f3ed115) - Checklist Item"

    code = fields.Char(
        default="/",
        help="Item code or number. Use '/' to auto-generate the code.",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_ws_f3ed115.category",
        help="Category used to group items on the checklist.",
        ondelete="restrict",
    )
