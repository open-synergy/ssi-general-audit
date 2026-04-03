# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS806c4e1Checklist(models.Model):
    """Checklist value line for Acceptance and Continuance of Client Relationships Analysis.

    Each record represents one evaluated checklist criterion within a
    ``general_audit_ws_806c4e1`` worksheet. Inherits ``mixin.checklist.value``
    which provides the response fields (e.g., Yes / No / N/A) and links
    each response to a predefined item template (``general_audit_ws_806c4e1.item``).

    Model: ``general_audit_ws_806c4e1.checklist``
    Parent worksheet: ``general_audit_ws_806c4e1``
    """

    _name = "general_audit_ws_806c4e1.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = (
        "Acceptance and Continuance of "
        "Client Relationships Analysis (806c4e1) - Checklist"
    )

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_806c4e1",
        required=True,
        ondelete="cascade",
        help="Reference to the parent worksheet for Acceptance and Continuance of "
        "Client Relationships Analysis. This field establishes the relationship "
        "between the checklist item and its corresponding worksheet.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_806c4e1.item",
        required=True,
        help="The specific checklist item that this record represents. "
        "Each checklist item contains predefined criteria or questions "
        "that need to be evaluated for the client relationship analysis.",
    )
