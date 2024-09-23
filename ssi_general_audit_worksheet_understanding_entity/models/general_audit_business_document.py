# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditBusinessDocument(models.Model):
    _name = "general_audit_business_document"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Business Document"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    business_function_ids = fields.Many2many(
        string="Business Functions",
        comodel_name="general_audit_business_function",
        relation="rel_business_function_2_document",
        column1="business_document_id",
        column2="business_function_id",
    )
