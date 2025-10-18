# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSde417a6Checklist(models.Model):
    _name = "general_audit_ws_de417a6.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "ROMM (de417a6) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_de417a6",
        required=True,
        ondelete="cascade",
        help=(
            "Worksheet that this checklist response belongs to. Deleting the worksheet "
            "will also delete its checklist responses."
        ),
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_de417a6.item",
        required=True,
        help=("Checklist item being answered on this worksheet."),
    )
