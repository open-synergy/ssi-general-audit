# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS806c4e1Checklist(models.Model):
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
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_806c4e1.item",
        required=True,
    )
