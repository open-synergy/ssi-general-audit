# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditIndependenceStatementChecklist(models.Model):
    _name = "general_audit_independence_statement_checklist"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Independence Statement Checklist"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
