# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS09253feChecklist(models.Model):
    """
    Independence Statement — Checklist Line (09253fe)

    A single assessed checklist item within the Independence Statement
    worksheet (WS.020.1).  Each line captures the engagement team
    member's Yes / No / N-A response and, where applicable, an
    explanation for a specific independence requirement.

    Child of ``general_audit_ws_09253fe``.  Cascades on parent delete.
    """

    _name = "general_audit_ws_09253fe.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Independence Statement (09253fe) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_09253fe",
        required=True,
        ondelete="cascade",
        help="""Reference to the parent Independence Statement worksheet.
Required. Deleting the worksheet cascades and removes its checklist lines.""",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_09253fe.item",
        required=True,
        help="Checklist item/question being evaluated on this line.",
    )
