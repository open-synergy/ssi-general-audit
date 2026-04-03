# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS09253feItem(models.Model):
    """
    Independence Statement — Checklist Item Master (09253fe)

    Master-data model holding the library of independence requirements
    used in the Independence Statement worksheet (WS.020.1).  Items
    correspond to the independence threats and safeguard checks
    prescribed by the IESBA Code of Ethics and ISA 200 / SA 200, such
    as financial interest, family relationships, and non-audit services.
    Items are loaded automatically onto the worksheet via
    ``mixin.checklist``.
    """

    _name = "general_audit_ws_09253fe.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Independence Statement (09253fe) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="""Internal code for the checklist item.
Defaults to '/'; may be replaced by a generated sequence depending on configuration.""",
    )
