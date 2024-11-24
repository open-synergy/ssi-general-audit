# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditEngagementLetterChecklist(models.Model):
    _name = "general_audit_engagement_letter_checklist"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Engagement Letter Checklist"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
