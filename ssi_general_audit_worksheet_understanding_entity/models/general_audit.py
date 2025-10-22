# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAudit(models.Model):
    _name = "general_audit"
    _description = "General Audit"
    _inherit = [
        "general_audit",
    ]

    business_cycle_ids = fields.Many2many(
        string="Business Cycles",
        comodel_name="client_business_process",
        relation="rel_general_audit_2_business_cycle",
        column1="general_audit_id",
        column2="business_process_id",
        readonly=True,
        help=("Business cycles relevant to the audit engagement"),
    )
    other_report_ids = fields.Many2many(
        string="Other Reports",
        comodel_name="general_audit_other_report",
        relation="rel_general_audit_2_other_report",
        column1="general_audit_id",
        column2="other_report_id",
        readonly=True,
        help=("Other reports relevant to the audit engagement"),
    )
    ws_ae11f7e_expert_ids = fields.One2many(
        string="WS AE11F7E Details",
        comodel_name="general_audit_ws_ae11f7e.expert",
        inverse_name="general_audit_id",
        readonly=True,
    )
    expert_type_ids = fields.Many2many(
        string="Expert Needed",
        comodel_name="general_audit_expert_type",
        relation="rel_general_audit_2_expert_type",
        column1="general_audit_id",
        column2="expert_type_id",
        compute="_compute_expert_type_ids",
        store=True,
        compute_sudo=True,
        help=("Types of experts needed for the audit engagement"),
    )

    # Impacted standard account
    expert_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Use of Expert",
        comodel_name="client_account_type",
        compute="_compute_impacted_account_types",
        relation="rel_general_audit_2_expert_impacted_account_type",
        column1="general_audit_id",
        column2="type_id",
        store=True,
        compute_sudo=True,
        help=("Standard account types impacted by the use of experts"),
    )

    previous_audit_information_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Previous Audit Information",
        comodel_name="client_account_type",
        compute="_compute_previous_audit_information_impacted_account_types",
        relation="rel_general_audit_2_prev_audit_info_impacted_account_type",
        column1="general_audit_id",
        column2="type_id",
        store=True,
        compute_sudo=True,
        help=(
            "Standard account types impacted by previous significant audit information"
        ),
    )

    previous_other_information_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Previous Other Information",
        comodel_name="client_account_type",
        compute="_compute_previous_other_information_impacted_account_types",
        relation="rel_general_audit_2_prev_other_info_impacted_account_type",
        column1="general_audit_id",
        column2="type_id",
        store=True,
        compute_sudo=True,
        help=(
            "Standard account types impacted by previous significant other information"
        ),
    )

    other_information_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Other Information",
        comodel_name="client_account_type",
        compute="_compute_other_information_impacted_account_types",
        relation="rel_general_audit_2_other_info_impacted_account_type",
        column1="general_audit_id",
        column2="type_id",
        store=True,
        compute_sudo=True,
        help=("Standard account types impacted by other significant information"),
    )
    regulation_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Regulation",
        comodel_name="client_account_type",
        compute="_compute_regulation_impacted_account_types",
        relation="rel_general_audit_2_regulation_impacted_account_type",
        column1="general_audit_id",
        column2="type_id",
        store=True,
        compute_sudo=True,
        help=("Standard account types impacted by regulations"),
    )
    preparation_of_financial_statements_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Preparation of Financial Statements",
        comodel_name="client_account_type",
        compute="_compute_preparation_of_financial_statements_impacted_account_types",
        relation="rel_general_audit_2_prep_fin_stmt_impacted_account_type",
        column1="general_audit_id",
        column2="type_id",
        store=True,
        compute_sudo=True,
        help=(
            "Standard account types impacted by the preparation of financial statements"
        ),
    )
    fraud_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Fraud Risk",
        comodel_name="client_account_type",
        compute="_compute_fraud_impacted_account_types",
        relation="rel_general_audit_2_fraud_impacted_account_type",
        column1="general_audit_id",
        column2="type_id",
        store=True,
        compute_sudo=True,
        help=("Standard account types impacted by fraud risk"),
    )
    business_environment_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Business Environment",
        comodel_name="client_account_type",
        compute="_compute_business_environment_impacted_account_types",
        relation="rel_general_audit_2_business_env_impacted_account_type",
        column1="general_audit_id",
        column2="type_id",
        store=True,
        compute_sudo=True,
        help=("Standard account types impacted by business environment"),
    )

    @api.depends(
        "standard_detail_ids",
        "standard_detail_ids.business_environmeny_impacted",
    )
    def _compute_business_environment_impacted_account_types(self):
        for record in self:
            criteria = [
                ("general_audit_id", "=", record.id),
                ("business_environmeny_impacted", "=", True),
            ]
            result = (
                self.env["general_audit.standard_detail"]
                .search(criteria)
                .mapped("type_id.id")
            )
            record.business_environment_impacted_account_type_ids = [(6, 0, result)]

    @api.depends(
        "standard_detail_ids",
        "standard_detail_ids.fraud_impacted",
    )
    def _compute_fraud_impacted_account_types(self):
        for record in self:
            criteria = [
                ("general_audit_id", "=", record.id),
                ("fraud_impacted", "=", True),
            ]
            result = (
                self.env["general_audit.standard_detail"]
                .search(criteria)
                .mapped("type_id.id")
            )
            record.fraud_impacted_account_type_ids = [(6, 0, result)]

    @api.depends(
        "standard_detail_ids",
        "standard_detail_ids.preparation_of_financial_statements_impacted",
    )
    def _compute_preparation_of_financial_statements_impacted_account_types(self):
        for record in self:
            criteria = [
                (
                    "general_audit_id",
                    "=",
                    record.id,
                ),
                (
                    "preparation_of_financial_statements_impacted",
                    "=",
                    True,
                ),
            ]
            result = (
                self.env["general_audit.standard_detail"]
                .search(criteria)
                .mapped("type_id.id")
            )
            record.preparation_of_financial_statements_impacted_account_type_ids = [
                (6, 0, result)
            ]

    @api.depends(
        "standard_detail_ids",
        "standard_detail_ids.regulation_impacted",
    )
    def _compute_regulation_impacted_account_types(self):
        for record in self:
            criteria = [
                ("general_audit_id", "=", record.id),
                ("regulation_impacted", "=", True),
            ]
            result = (
                self.env["general_audit.standard_detail"]
                .search(criteria)
                .mapped("type_id.id")
            )
            record.regulation_impacted_account_type_ids = [(6, 0, result)]

    @api.depends(
        "standard_detail_ids",
        "standard_detail_ids.previous_other_information_impacted",
    )
    def _compute_previous_other_information_impacted_account_types(self):
        for record in self:
            criteria = [
                ("general_audit_id", "=", record.id),
                ("previous_other_information_impacted", "=", True),
            ]
            result = (
                self.env["general_audit.standard_detail"]
                .search(criteria)
                .mapped("type_id.id")
            )
            record.previous_other_information_impacted_account_type_ids = [
                (6, 0, result)
            ]

    @api.depends(
        "standard_detail_ids",
        "standard_detail_ids.other_information_impacted",
    )
    def _compute_other_information_impacted_account_types(self):
        for record in self:
            criteria = [
                ("general_audit_id", "=", record.id),
                ("other_information_impacted", "=", True),
            ]
            result = (
                self.env["general_audit.standard_detail"]
                .search(criteria)
                .mapped("type_id.id")
            )
            record.other_information_impacted_account_type_ids = [(6, 0, result)]

    @api.depends(
        "standard_detail_ids",
        "standard_detail_ids.expert_impacted",
    )
    def _compute_impacted_account_types(self):
        for record in self:
            criteria = [
                ("general_audit_id", "=", record.id),
                ("expert_impacted", "=", True),
            ]
            result = (
                self.env["general_audit.standard_detail"]
                .search(criteria)
                .mapped("type_id.id")
            )
            record.expert_impacted_account_type_ids = [(6, 0, result)]

    @api.depends(
        "standard_detail_ids",
        "standard_detail_ids.previous_audit_information_impacted",
    )
    def _compute_previous_audit_information_impacted_account_types(self):
        for record in self:
            criteria = [
                ("general_audit_id", "=", record.id),
                ("previous_audit_information_impacted", "=", True),
            ]
            result = (
                self.env["general_audit.standard_detail"]
                .search(criteria)
                .mapped("type_id.id")
            )
            record.previous_audit_information_impacted_account_type_ids = [
                (6, 0, result)
            ]

    @api.depends(
        "ws_ae11f7e_expert_ids",
        "ws_ae11f7e_expert_ids.type_id",
    )
    def _compute_expert_type_ids(self):
        for record in self:
            result = []
            if record.ws_ae11f7e_expert_ids:
                result = record.mapped("ws_ae11f7e_expert_ids.type_id.id")
            record.expert_type_ids = result
