# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd8aaebcChecklist(models.Model):
    _name = "general_audit_ws_d8aaebc.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Engagement Letter (d8aaebc) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_d8aaebc",
        required=True,
        ondelete="cascade",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_d8aaebc.item",
        required=True,
    )
