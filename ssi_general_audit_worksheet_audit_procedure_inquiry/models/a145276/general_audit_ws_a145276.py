# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSa145276(models.Model):
    """Worksheet for documenting Inquiry audit procedures (WS-A145276).

    In accordance with ISA 500 / SA 500 (Audit Evidence) and ISA 240 / SA 240,
    inquiry is one of the primary audit procedures used to obtain audit evidence
    by seeking information from knowledgeable persons — both financial and
    non-financial — inside or outside the entity.

    This worksheet records a structured inquiry session, including:
    - The source of information (person or party being inquired)
    - The position/role of the source within the entity
    - The key audit procedure and assertion types being addressed
    - A list of audit questions (``question_ids``) and the corresponding answers
      obtained from the inquiry
    - Background context for the inquiry
    - A summary of findings
    - An overall risk assessment (Low / Medium / High) based on the responses

    The worksheet is linked to the Key Audit Procedures worksheet (WS-E51BB1C /
    Lead Schedule) so that inquiry findings can be traced back to the specific
    planned audit procedure that they support.

    Workflow: Draft → Open → Confirm → Done
    """

    _name = "general_audit_ws_a145276"
    _description = "Inquiry Audit Procedure (a145276)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_audit_procedure_inquiry." "worksheet_type_a145276"
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
        help="Account types allowed for selection in this inquiry procedure.",
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
        help="The standard account type related to this inquiry procedure.",
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
        relation="general_audit_ws_a145276_assertion_type_rel",
        column1="worksheet_id",
        column2="assertion_type_id",
        string="Assertion Types",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The assertion types applicable to this inquiry procedure.",
    )
    source_of_information = fields.Char(
        string="Source of Information",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The source of information for this inquiry procedure.",
    )
    source_of_information_position = fields.Char(
        string="Source of Information Position",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The position of the source of information for this inquiry procedure.",
    )
    result = fields.Selection(
        string="Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Overall risk assessment for this inquiry procedure.",
    )
    background = fields.Text(
        string="Background",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Background information for this inquiry procedure.",
    )
    summary = fields.Text(
        string="Summary",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Summary of findings for this inquiry procedure.",
    )
    question_ids = fields.One2many(
        comodel_name="general_audit_ws_a145276.question",
        inverse_name="worksheet_id",
        string="Questions",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="List of questions and answers for this inquiry procedure.",
    )
    worksheet_result = fields.Text(
        string="Worksheet Result",
        help="Rich-text result or conclusion of this inquiry audit procedure.",
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
