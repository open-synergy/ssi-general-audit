# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS369c5a5Checklist(models.Model):
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
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_369c5a5.item",
        required=True,
    )
