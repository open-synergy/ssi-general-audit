# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditAuditProcedure(models.Model):
    _name = "general_audit_audit_procedure"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Audit Procedure"

    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Account Type",
        required=True,
    )
    category_id = fields.Many2one(
        comodel_name="general_audit_audit_procedure_category",
        string="Category",
        required=True,
    )

    @api.onchange("account_type_id")
    def onchange_category_id(self):
        self.category_id = False
