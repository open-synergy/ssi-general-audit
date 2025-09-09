# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSf6a227Detail(models.Model):
    _name = "general_audit_ws_f6a227.detail"
    _description = "Worksheet f6a227 - Detail"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_f6a227",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    step_id = fields.Many2one(
        string="Step",
        comodel_name="general_audit_fs_preparation_step",
        required=True,
    )
    description = fields.Text(
        string="Understanding Result",
        required=True,
    )
    control_activity = fields.Text(
        string="Control Activity",
        required=True,
    )
    audit_relevancy = fields.Text(
        string="Audit Relevancy",
        required=True,
    )
    misstatement_identification = fields.Text(
        string="Misstatement Identification",
        required=True,
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_f6a227_detail_2_account_type",
        column1="detail_id",
        column2="type_id",
        required=True,
    )

    def onchange_sequence(self):
        self.sequence = 10
        if self.step_id:
            self.sequence = self.step_id.sequence
