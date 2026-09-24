# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsE59c663Item(models.Model):
    """Checklist item master for the Draft Financial Statements worksheet.

    Defines the individual components that must be present in a complete
    set of draft financial statements (e.g., 'Statement of Financial
    Position', 'Impairment of non-financial assets'), mirroring the
    client's WR.160.1 completeness checklist sheet.  The ``code`` field
    preserves the original WR.160.1 numbering (e.g. ``5.2.14``).
    """

    _name = "general_audit_ws_e59c663.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Draft Financial Statements (e59c663) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="Item code matching WR.160.1 numbering, e.g. '5.2.14'. "
        "Use '/' to auto-generate the code.",
    )
