# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSD8AAEBCChecklist(models.Model):
    _name = "general_audit_ws_d8aaebc.checklist"
    _description = "Audit Working Plan (d8aaebc) - Checklist"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_d8aaebc",
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
        comodel_name="general_audit_engagement_letter_checklist",
        required=True,
    )
    checklist_ok = fields.Boolean(
        string="Passed?",
        required=True,
        default=True,
    )
