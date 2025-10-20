# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa8f4d88Detail(models.Model):
    _name = "general_audit_ws_a8f4d88.detail"
    _description = "Accounting Estimation (a8f4d88) - Detail"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_a8f4d88",
        string="Worksheet",
        required=True,
        ondelete="cascade",
    )
    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Standard Account",
        required=True,
        ondelete="restrict",
    )
    expert_ids = fields.Many2many(
        comodel_name="general_audit_expert_type", string="Experts Involved"
    )
    estimation_method_ids = fields.Many2many(
        comodel_name="general_audit_accounting_estimation_method",
        string="Estimation Methods Used",
        relation="rel_general_audit_ws_a8f4d88_detail_2_acc_est_method",
        column1="detail_id",
        column2="estimation_method_id",
        required=True,
    )
    relevant_control_id = fields.Many2one(
        comodel_name="general_audit_accounting_estimation_relevant_control",
        string="Relevant Controls",
        relation="rel_general_audit_ws_a8f4d88_detail_2_acc_est_relevant_control",
        column1="detail_id",
        column2="relevant_control_id",
        required=True,
    )
    fair_value_measurement_level = fields.Selection(
        selection=[
            ("level_1", "Level 1"),
            ("level_2", "Level 2"),
            ("level_3", "Level 3"),
        ],
        string="Fair Value Measurement Level",
        required=True,
    )
    assumption = fields.Text(
        string="Key Assumptions",
        required=True,
    )
    reference = fields.Char(
        string="Reference",
        required=True,
    )
    conclusion = fields.Text(
        string="Conclusion",
        required=True,
    )
