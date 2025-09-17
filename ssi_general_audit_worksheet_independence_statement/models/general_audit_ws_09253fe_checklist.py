# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS09253feChecklist(models.Model):
    _name = "general_audit_ws_09253fe.checklist"
    _description = "Independence Statement (09253fe) - Checklist"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_09253fe",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    checklist_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_independence_letter_checklist",
        required=True,
    )
    checklist_ok = fields.Boolean(
        string="Passed?",
        required=True,
        default=True,
    )
