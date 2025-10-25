# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa025441Checklist(models.Model):
    _name = "general_audit_ws_a025441.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Financial Statement Disclosure (a025441) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_a025441",
        required=True,
        ondelete="cascade",
        help="Parent worksheet to which this checklist line belongs.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_a025441.item",
        required=True,
        help="Checklist item that must be answered on this line.",
    )
    financial_accounting_standard_id = fields.Many2one(
        related="item_id.financial_accounting_standard_id",
        help="Financial accounting standard derived from the selected checklist item.",
    )
    relevant_accounting_standard_id = fields.Many2one(
        related="item_id.relevant_accounting_standard_id",
        help="Relevant accounting standard derived from the selected checklist item.",
    )
    ref = fields.Text(
        string="Reference",
        help=(
            "Cross-reference to working papers, notes, or document sections "
            "that support the answer provided for this checklist line."
        ),
    )
