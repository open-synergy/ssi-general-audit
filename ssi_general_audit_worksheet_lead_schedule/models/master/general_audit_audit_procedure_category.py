# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditAuditProcedureCategory(models.Model):
    _name = "general_audit_audit_procedure_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Audit Procedure Category"

    code = fields.Char(
        default="/",
        help="Unique short code for the team role. Use '/' to auto-generate.",
    )
    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Account Type",
        required=True,
        ondelete="restrict",
    )
    assertion_type_ids = fields.Many2many(
        comodel_name="general_audit_assersion_type",
        string="Applicable Assertions",
        required=True,
        relation="rel_audit_procedure_category_2_assertion_type",
        column1="category_id",
        column2="assertion_type_id",
    )
