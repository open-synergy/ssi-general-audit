# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditClassTransaction(models.Model):
    """Master: Class of Transaction.

    Reference list of transaction classes relevant to the audit (e.g., Revenue
    and Receipts, Purchases and Payments, Payroll, Fixed Assets). Per ISA 315,
    auditors must understand the entity's significant classes of transactions,
    how they are initiated, recorded, processed, and reported. Used in the
    Business Cycle Summaries worksheet (a604795) and links to related account
    types for traceability across the audit.
    """

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
