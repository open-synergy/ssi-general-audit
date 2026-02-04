# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSd4d1ac0(models.Model):
    _name = "general_audit_ws_d4d1ac0"
    _description = "Observation Audit Procedure (d4d1ac0)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_audit_procedure_observation."
        "worksheet_type_d4d1ac0"
    )

    ws_e51bb1c_id = fields.Many2one(
        comodel_name="general_audit_ws_e51bb1c",
        string="# WS-E51BB1C",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Reference to the Key Audit Procedures worksheet.",
    )
    detail_ws_e51bb1c_id = fields.Many2one(
        comodel_name="general_audit_ws_e51bb1c.detail",
        string="Detail WS-E51BB1C",
        compute="_compute_detail_ws_e51bb1c_id",
        store=True,
        help="Details from the referenced Key Audit Procedures worksheet.",
        compute_sudo=True,
    )
    allowed_key_audit_procedure_ids = fields.Many2many(
        comodel_name="general_audit_audit_procedure_category",
        string="Allowed Key Audit Procedures",
        help="Key audit procedures that can be selected based on the referenced worksheet.",
        compute="_compute_allowed_key_audit_procedure_ids",
        store=False,
        compute_sudo=True,
    )
    key_audit_procedure_id = fields.Many2one(
        comodel_name="general_audit_audit_procedure_category",
        string="Key Audit Procedure",
        help="The key audit procedure associated with the referenced worksheet.",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
    )
    allowed_account_type_ids = fields.Many2many(
        comodel_name="client_account_type",
        related="general_audit_id.account_type_ids",
        string="Allowed Account Types",
        store=False,
        help="Account types allowed for selection in this observation procedure.",
        compute_sudo=True,
    )
    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Standard Account",
        required=False,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The standard account type related to this observation procedure.",
    )
    allowed_assertion_type_ids = fields.Many2many(
        comodel_name="general_audit_assersion_type",
        string="Allowed Assertion Types",
        help="Assertion types that can be selected based on the key audit procedure.",
        related="detail_ws_e51bb1c_id.assertion_type_ids",
        store=False,
        compute_sudo=True,
    )
    assertion_type_ids = fields.Many2many(
        comodel_name="general_audit_assersion_type",
        relation="general_audit_ws_d4d1ac0_assertion_type_rel",
        column1="worksheet_id",
        column2="assertion_type_id",
        string="Assertion Types",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Assertion types relevant to this observation procedure.",
    )
    allowed_class_of_transaction_ids = fields.Many2many(
        comodel_name="general_audit_class_transaction",
        compute="_compute_allowed_class_of_transaction_ids",
        store=False,
        string="Allowed Classes of Transaction",
        help="Classes of transaction that can be selected based on the business cycle.",
        compute_sudo=True,
    )
    class_of_transaction_id = fields.Many2one(
        comodel_name="general_audit_class_transaction",
        string="Class of Transaction",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
    )
    background = fields.Text(
        string="Background",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Background information for this observation procedure.",
    )
    primary_concern = fields.Text(
        string="Primary Concern",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Primary concern identified during this observation procedure.",
    )
    observation_ids = fields.One2many(
        comodel_name="general_audit_ws_d4d1ac0.observation",
        inverse_name="worksheet_id",
        string="Observations",
        help="List of observations made during this audit procedure.",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
    )
    summary = fields.Text(
        string="Summary",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Summary of findings from this observation procedure.",
    )

    @api.depends(
        "ws_e51bb1c_id",
    )
    def _compute_allowed_key_audit_procedure_ids(self):
        Detail = self.env["general_audit_ws_e51bb1c.detail"]
        for record in self:
            record.allowed_key_audit_procedure_ids = False
            if record.ws_e51bb1c_id:
                criteria = [
                    ("worksheet_id", "=", record.ws_e51bb1c_id.id),
                    ("status", "=", "performed"),
                ]
                details = Detail.search(criteria)
                if details:
                    procedures = details.mapped("audit_procedure_category_id")
                    record.allowed_key_audit_procedure_ids = procedures

    @api.depends(
        "ws_e51bb1c_id",
        "key_audit_procedure_id",
    )
    def _compute_detail_ws_e51bb1c_id(self):
        Detail = self.env["general_audit_ws_e51bb1c.detail"]
        for record in self:
            record.detail_ws_e51bb1c_id = False
            if record.ws_e51bb1c_id and record.key_audit_procedure_id:
                criteria = [
                    ("worksheet_id", "=", record.ws_e51bb1c_id.id),
                    (
                        "audit_procedure_category_id",
                        "=",
                        record.key_audit_procedure_id.id,
                    ),
                ]
                detail = Detail.search(criteria, limit=1)
                if detail:
                    record.detail_ws_e51bb1c_id = detail

    @api.depends(
        "account_type_id",
    )
    def _compute_allowed_class_of_transaction_ids(self):
        ClassOfTransaction = self.env["general_audit_class_transaction"]
        for record in self:
            record.allowed_class_of_transaction_ids = False
            if record.account_type_id:
                criteria = [
                    ("related_account_type_ids", "in", record.account_type_id.id),
                ]
                class_of_transactions = ClassOfTransaction.search(criteria)
                if class_of_transactions:
                    record.allowed_class_of_transaction_ids = class_of_transactions

    @api.onchange(
        "general_audit_id",
    )
    def onchange_account_type_id(self):
        self.account_type_id = False

    @api.onchange(
        "general_audit_id",
    )
    def onchange_ws_e51bb1c_id(self):
        self.ws_e51bb1c_id = False
