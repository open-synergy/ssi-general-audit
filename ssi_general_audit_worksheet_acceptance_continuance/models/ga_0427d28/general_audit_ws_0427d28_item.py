# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS369c5a5Item(models.Model):
    """Master data: Checklist item template for Previous Financial Reporting Issues.

    Defines the predefined criteria and questions used in the checklist of
    the ``general_audit_ws_369c5a5`` worksheet. Inherits ``mixin.checklist.item``
    providing the item title, option set, and scoring structure.

    Items cover prior-period reporting issues such as audit qualifications,
    material misstatements, delayed filings, and management disagreements.

    Note: This class is physically located in the ``ga_0427d28`` directory
    but defines the ``general_audit_ws_369c5a5.item`` model.

    Model: ``general_audit_ws_369c5a5.item``
    """

    _name = "general_audit_ws_369c5a5.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Previous Financial Reporting Issues (369c5a5) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="Internal code/identifier for the checklist item. Defaults to '/'.",
    )
