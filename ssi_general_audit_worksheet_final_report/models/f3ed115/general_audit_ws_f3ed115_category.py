# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWsF3ed115Category(models.Model):
    """
    Master: Final Communication With TCWG Checklist Category (f3ed115).

    Provides a configurable category used to group items in the Final
    Communication With TCWG checklist (f3ed115). Items and category
    contents are intentionally left empty until the actual checklist
    content is formulated.
    """

    _name = "general_audit_ws_f3ed115.category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Final Communication With TCWG (f3ed115) - Category"

    code = fields.Char(
        default="/",
        help="Unique short code for the category. Use '/' to auto-generate.",
    )
