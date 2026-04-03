# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa025441Item(models.Model):
    """
    Checklist item master for the Financial Statement Disclosure Checklist (a025441).

    Each item represents a **single disclosure requirement** from a specific
    financial accounting standard and relevant accounting standard.  Examples:

    * "PSAK 1 — Presentation of Financial Statements: Basis of preparation
      disclosed" (under Fair Presentation and Compliance framework).
    * "PSAK 25 — Accounting Policies, Changes in Accounting Estimates and
      Errors: Nature of changes and reason for change disclosed".

    Items are ordered by ``financial_accounting_standard_id`` then
    ``sequence``, enabling systematic review of all applicable disclosure
    requirements grouped by standard.
    """

    _name = "general_audit_ws_a025441.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Financial Statement Disclosure (a025441) - " "Checklist Item"
    _order = "financial_accounting_standard_id, sequence, id"

    code = fields.Char(
        default="/",
        help="Item code or number. Use '/' to auto-generate the code.",
    )
    financial_accounting_standard_id = fields.Many2one(
        string="Financial Accounting Standard",
        comodel_name="accountant.financial_accounting_standard",
        required=True,
        help="Accounting standard (e.g., IFRS, GAAP) applied in this audit.",
    )
    relevant_accounting_standard_id = fields.Many2one(
        string="Relevant Accounting Standard",
        comodel_name="client_relevant_account_type",
        required=True,
        help="Relevant Accounting Standard (e.g., PSAK 102) applied in this audit.",
    )
