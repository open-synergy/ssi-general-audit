# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWS842f0d6Checklist(models.Model):
    _name = "general_audit_ws_842f0d6.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Money Laudring Issues (842f0d6) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_842f0d6",
        required=True,
        ondelete="cascade",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_842f0d6.item",
        required=True,
    )

    @api.depends(
        "item_id",
    )
    def _compute_allowed_item_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_842f0d6.item_categ"]
            criteria = [
                ("categ", "=", record.item_id.categ),
            ]
            record.allowed_item_ids = obj.search(criteria).ids

    allowed_item_ids = fields.Many2many(
        string="Allowed Items",
        comodel_name="general_audit_ws_842f0d6.item_categ",
        compute="_compute_allowed_item_ids",
        store=False,
    )
    item_ids = fields.Many2many(
        string="Items",
        comodel_name="general_audit_ws_842f0d6.item_categ",
        relation="rel_ga_842f0d6_item_2_item_categ",
        column1="item_id",
        column2="item_categ_id",
    )
