# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditClassTransaction(models.Model):
    _name = "general_audit_class_transaction"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Class Transaction"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    business_function_ids = fields.One2many(
        string="Business Functions",
        comodel_name="general_audit_business_function",
        inverse_name="class_transaction_id",
    )
    related_account_type_ids = fields.Many2many(
        string="Related Account Types",
        comodel_name="client_account_type",
        relation="rel_class_transaction_2_account_type",
        column1="class_transaction_id",
        column2="account_type_id",
    )
