# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSf5e7049Item(models.Model):
    """Master data: Checklist item template for Management Integrity worksheet.

    Defines the predefined criteria and questions used in the checklist of
    the ``general_audit_ws_f5e7049`` worksheet. Inherits ``mixin.checklist.item``
    providing the item title, option set, and scoring structure.

    Items cover integrity indicators such as management ethics, fraud history,
    related-party transactions, and governance concerns.

    Model: ``general_audit_ws_f5e7049.item``
    """

    _name = "general_audit_ws_f5e7049.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Management Integrity (f5e7049) - " "Checklist Item"

    code = fields.Char(
        default="/",
    )
