# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditBusinessFunction(models.Model):
    """Master: Business Function.

    Reference list of operational business functions (e.g., order taking,
    invoicing, cash receipt, goods receipt) that are part of the entity's
    transaction processing cycles. Each function belongs to a transaction class
    and is linked to relevant business documents. Used in the Business Cycle
    Summaries worksheet (a604795) to map entity processes per ISA 315.
    """

    _name = "general_audit_business_function"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Business Function"
    _order = "class_transaction_id, sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    class_transaction_id = fields.Many2one(
        string="Class of Transaction",
        comodel_name="general_audit_class_transaction",
        ondelete="restrict",
        required=True,
    )
    business_document_ids = fields.Many2many(
        string="Business Documents",
        comodel_name="general_audit_business_document",
        relation="rel_business_function_2_document",
        column1="business_function_id",
        column2="business_document_id",
    )
