# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsE59c663ReviewItem(models.Model):
    """Review procedure checklist item master for the Draft Financial
    Statements worksheet.

    Defines the individual review procedure steps that must be
    performed before the draft financial statements are confirmed
    (e.g., 'Perform footing and cross-footing', 'Review the report
    format'), mirroring the client's WR.160 review procedure checklist
    sheet. The ``code`` field preserves the original WR.160 numbering
    (e.g. ``a.2.1``).
    """

    _name = "general_audit_ws_e59c663.review_item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = (
        "Draft Financial Statements (e59c663) - " "Review Procedure Checklist Item"
    )

    code = fields.Char(
        default="/",
        help="Item code matching WR.160 numbering, e.g. 'a.2.1'. "
        "Use '/' to auto-generate the code.",
    )
