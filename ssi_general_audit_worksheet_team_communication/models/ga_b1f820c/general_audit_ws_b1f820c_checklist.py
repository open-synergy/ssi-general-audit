# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb1f820cChecklist(models.Model):
    _name = "general_audit_ws_b1f820c.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Team Communication Risk Assessment (b1f820c) - " "Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_b1f820c",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet this checklist value belongs to. "
            "Used to group checklist values by worksheet. Deleting the worksheet "
            "will also remove associated checklist lines."
        ),
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_b1f820c.item",
        required=True,
        help=(
            "Reference to the checklist item definition that this checklist value "
            "corresponds to."
        ),
    )
    communication_type = fields.Selection(
        related="item_id.communication_type",
        compute_sudo=True,
    )
