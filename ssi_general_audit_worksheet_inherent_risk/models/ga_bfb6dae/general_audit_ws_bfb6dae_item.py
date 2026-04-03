# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbfb6daeItem(models.Model):
    """
    Inherent Risk Assessment Checklist — Checklist Item Master (bfb6dae)

    Master-data model for the checklist items used in the Inherent Risk
    Assessment Checklist worksheet (WS.060.1).  Each item represents one
    inherent risk indicator to be evaluated.  Items are loaded
    automatically onto the worksheet via ``mixin.checklist``.
    """

    _name = "general_audit_ws_bfb6dae.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Inherent Risk (bfb6dae) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="""Internal code for the checklist item.
Defaults to '/'; may be replaced by a generated sequence depending on configuration.""",
    )
