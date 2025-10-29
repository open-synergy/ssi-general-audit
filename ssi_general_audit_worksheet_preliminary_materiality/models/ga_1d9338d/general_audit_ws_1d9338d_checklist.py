# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS1d9338dChecklist(models.Model):
    _name = "general_audit_ws_1d9338d.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Preliminary Materiality (1d9338d) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_1d9338d",
        required=True,
        ondelete="cascade",
        help=(
            "Parent worksheet (1d9338d). Required. Deleting the worksheet "
            "will cascade and remove its checklist items."
        ),
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_1d9338d.item",
        required=True,
        help="Checklist item definition referenced by this line.",
    )
    checklist_type = fields.Selection(
        related="item_id.checklist_type",
        help="Type/category of the checklist item, inherited from the item.",
    )
