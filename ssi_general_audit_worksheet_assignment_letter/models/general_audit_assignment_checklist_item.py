# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditAssignmentLetterChecklist(models.Model):
    _name = "general_audit_assignment_letter_checklist"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Assignment Letter Checklist"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
