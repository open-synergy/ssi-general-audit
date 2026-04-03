# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS369c5a5Checklist(models.Model):
    """Checklist value line for Previous Financial Reporting Issues worksheet.

    Each record represents one evaluated checklist criterion within a
    ``general_audit_ws_369c5a5`` worksheet. Inherits ``mixin.checklist.value``
    which provides the response fields and links each response to a predefined
    item template (``general_audit_ws_369c5a5.item``).

    Note: This class is physically located in the ``ga_0427d28`` directory
    but defines the ``general_audit_ws_369c5a5.checklist`` model.

    Model: ``general_audit_ws_369c5a5.checklist``
    Parent worksheet: ``general_audit_ws_369c5a5``
    """

    _name = "general_audit_ws_369c5a5.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Previous Financial Reporting Issues (369c5a5) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_369c5a5",
        required=True,
        ondelete="cascade",
        help="Reference to the parent worksheet (Communication With Previous Auditor).\n"
        "Links this checklist line to its worksheet and enforces cascade deletion.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_369c5a5.item",
        required=True,
        help="The checklist definition/question represented by this line.\n"
        "Items define criteria to be evaluated in this worksheet.",
    )
