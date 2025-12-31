# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc2375d8Checklist(models.Model):
    _name = "general_audit_ws_c2375d8.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Final Analytical Procedures (c2375d8) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_c2375d8",
        required=True,
        ondelete="cascade",
        help="""Reference to the parent Final Analytical Procedures worksheet.
Required. Deleting the worksheet cascades and removes its checklist lines.""",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_c2375d8.item",
        required=True,
        help="Checklist item/question being evaluated on this line.",
    )
    analysis_type = fields.Selection(
        related="item_id.analysis_type",
        compute_sudo=True,
        help="Type of analysis for this line, inherited from the linked checklist item.",
    )
