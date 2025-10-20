# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSAE11F7EAccountingPolicy(models.Model):
    _name = "general_audit_ws_ae11f7e.accounting_policy"
    _description = "Worksheet ae11f7e - Relevant Accounting Policy"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae11f7e",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This policy record will be deleted if the worksheet is deleted."
        ),
    )
    policy = fields.Text(
        required=True,
        help=(
            "Describe the relevant accounting policy applied by the entity "
            "(recognition, measurement, presentation, disclosure)."
        ),
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_ae11f7e_accounting_policy_2_account_type",
        column1="accounting_policy_id",
        column2="type_id",
        required=True,
        help=(
            "Standard account types impacted by this policy. "
            "Used to link the policy to related accounts."
        ),
    )
    relevant_account_type_ids = fields.Many2many(
        string="Relevant Standard Accounts",
        comodel_name="client_relevant_account_type",
        relation="rel_ga_ws_ae11f7e_accounting_policy_2_relevant_account",
        column1="accounting_policy_id",
        column2="type_id",
        required=True,
        help=(
            "Standard account types impacted by this policy. "
            "Used to link the policy to relevant accounts."
        ),
    )
