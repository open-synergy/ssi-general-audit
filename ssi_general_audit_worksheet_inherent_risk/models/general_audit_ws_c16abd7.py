# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc16abd7(models.Model):
    _name = "general_audit_ws_c16abd7"
    _description = "Financial Statement Level Inherent Risk (c16abd7)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_inherent_risk." "worksheet_type_c16abd7"

    # Link

    ws_c0e0eec_id = fields.Many2one(
        string="# Fraud Factor Analysis",
        comodel_name="general_audit_ws_c0e0eec",
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help="Link to Fraud Factor Analysis worksheet.",
    )
    ws_c0e0eec_id_review = fields.Text(
        string="Review Note on Fraud Factor Analysis",
        related="ws_c0e0eec_id.review",
        readonly=True,
        help="Review note from the linked Fraud Factor Analysis worksheet.",
    )
    ws_f6a227_id = fields.Many2one(
        string="# Understanding of preparation of Financial Statements",
        comodel_name="general_audit_ws_f6a227",
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    ws_f6a227_id_review = fields.Text(
        related="ws_f6a227_id.review",
        string="Review Note on Understanding of preparation of Financial Statements",
        readonly=True,
    )
    ws_c0d0898_id = fields.Many2one(
        string="# Going Concern Analysis",
        comodel_name="general_audit_ws_c0d0898",
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    ws_c0d0898_id_review = fields.Text(
        related="ws_c0d0898_id.review",
        string="Review Note on Going Concern Analysis",
        readonly=True,
    )
    ws_bdcdfc5_ids = fields.Many2many(
        string="# Understanding of the Business Environment",
        comodel_name="general_audit_ws_bdcdfc5",
        relation="general_audit_ws_c165170_bdcdfc5_rel",
        column1="ws_c165170_id",
        column2="ws_bdcdfc5_id",
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help="Links to Understanding of the Business Environment worksheets.",
    )

    risk_material_missstatement = fields.Selection(
        string="Risk Material Misstatement",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    auditor_respons = fields.Text(
        string="Auditor Respons",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    # Impacted standard account
    expert_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Use of Expert",
        comodel_name="client_account_type",
        related="general_audit_id.expert_impacted_account_type_ids",
        readonly=True,
        store=False,
    )
    previous_audit_information_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Previous Audit Information",
        comodel_name="client_account_type",
        related="general_audit_id.previous_audit_information_impacted_account_type_ids",
        readonly=True,
        store=False,
    )
    previous_other_information_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Previous Other Information",
        comodel_name="client_account_type",
        related="general_audit_id.previous_other_information_impacted_account_type_ids",
        readonly=True,
        store=False,
    )
    other_information_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Other Information",
        comodel_name="client_account_type",
        related="general_audit_id.other_information_impacted_account_type_ids",
        readonly=True,
        store=False,
    )
    regulation_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Relevant Regulations",
        comodel_name="client_account_type",
        related="general_audit_id.regulation_impacted_account_type_ids",
        readonly=True,
        store=False,
    )
    preparation_of_financial_statements_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Preparation of Financial Statements",
        comodel_name="client_account_type",
        related=(
            "general_audit_id."
            "preparation_of_financial_statements_impacted_account_type_ids"
        ),
        readonly=True,
        store=False,
    )
    fraud_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Fraud Risk",
        comodel_name="client_account_type",
        related="general_audit_id.fraud_impacted_account_type_ids",
        readonly=True,
        store=False,
    )
    business_environment_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Business Environment",
        comodel_name="client_account_type",
        related="general_audit_id.business_environment_impacted_account_type_ids",
        readonly=True,
        store=False,
    )
