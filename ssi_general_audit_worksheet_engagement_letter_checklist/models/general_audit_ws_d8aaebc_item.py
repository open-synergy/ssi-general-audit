# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd8aaebcItem(models.Model):
    """
    Engagement Letter Checklist — Item Master (d8aaebc)

    Master-data model that holds the library of checklist questions /
    requirements used when completing the Engagement Letter Checklist
    worksheet (WS.010.1).  Items are loaded automatically onto the
    worksheet via ``mixin.checklist``.  Inherits
    ``mixin.checklist.item`` which provides the name, description, and
    is_required flag.
    """

    _name = "general_audit_ws_d8aaebc.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Engagement Letter (d8aaebc) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="""Internal code for the checklist item.
Defaults to '/'; may be replaced by a generated sequence depending on configuration.""",
    )
