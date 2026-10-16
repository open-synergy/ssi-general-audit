# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWsA8c54f3Category(models.Model):
    """
    Master: Audit Final Memorandum Checklist Category (a8c54f3).

    Provides a configurable category used to group items in the Audit
    Final Memorandum review checklist (a8c54f3). The default categories
    are shipped as module data.
    """

    _name = "general_audit_ws_a8c54f3.category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Audit Final Memorandum (a8c54f3) - Category"

    code = fields.Char(
        default="/",
        help="Unique short code for the category. Use '/' to auto-generate.",
    )
