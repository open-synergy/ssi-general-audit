# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS437fc8fChecklist(models.Model):
    """Checklist value instance for Team Communication Pre-Engagement worksheet.

    Each record represents one auditor's response to a single checklist item
    within the ``general_audit_ws_437fc8f`` worksheet. This model stores the
    actual value/response provided by the audit team for each item, linking the
    item definition (master) with the worksheet instance.

    Inherits from ``mixin.checklist.value`` which provides the response fields
    (e.g., answer, notes, conclusion) defined in the mixin.
    """

    _name = "general_audit_ws_437fc8f.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Team Communication Pre-Engagement (437fc8f) - " "Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_437fc8f",
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
        comodel_name="general_audit_ws_437fc8f.item",
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
