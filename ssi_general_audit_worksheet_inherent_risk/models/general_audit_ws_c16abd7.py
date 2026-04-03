# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc16abd7(models.Model):
    """
    WS.060.3 — Financial Statement Level Inherent Risk (c16abd7)

    Documents the auditor's **financial-statement level inherent risk**
    assessment as required by ISA 315 / SA 315.  Unlike account-level
    inherent risk (WS.060.2), this worksheet looks at risks that affect
    the financial statements as a whole — i.e., risks that are pervasive
    rather than specific to particular assertions or accounts.

    The auditor evaluates financial-statement level risks by reviewing
    conclusions from several upstream understanding-phase worksheets:

    - **Fraud Factor Analysis** (``general_audit_ws_c0e0eec``) — Identifies
      fraud risk factors per ISA 240 / SA 240 requirements.
    - **Understanding of Preparation of Financial Statements**
      (``general_audit_ws_f6a227``) — Assessment of the entity's financial
      reporting framework and competence.
    - **Going Concern Analysis** (``general_audit_ws_c0d0898``) — Evaluation
      of going-concern risk factors per ISA 570 / SA 570.
    - **Understanding of the Business Environment**
      (``general_audit_ws_bdcdfc5``, multiple) — Entity-level risk factors.

    The auditor documents a conclusion on the overall financial-statement
    level inherent risk (low / medium / high) and records the review notes
    from each linked upstream worksheet.

    **ISA / SA references:** ISA 240 / SA 240 — The Auditor's Responsibilities
    Relating to Fraud; ISA 315 / SA 315 — Identifying and Assessing the Risks
    of Material Misstatement; ISA 570 / SA 570 — Going Concern
    """

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
        ondelete="restrict",
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
        ondelete="restrict",
        help="Link to the Understanding of preparation of Financial Statements worksheet.",
    )
    ws_f6a227_id_review = fields.Text(
        related="ws_f6a227_id.review",
        string="Review Note on Understanding of preparation of Financial Statements",
        readonly=True,
        help=(
            "Review note from the linked Understanding of "
            "preparation of Financial Statements worksheet."
        ),
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
        ondelete="restrict",
        help="Link to the Going Concern Analysis worksheet.",
    )
    ws_c0d0898_id_review = fields.Text(
        related="ws_c0d0898_id.review",
        string="Review Note on Going Concern Analysis",
        readonly=True,
        help="Review note from the linked Going Concern Analysis worksheet.",
    )
    ws_bdcdfc5_ids = fields.Many2many(
        string="# Understanding of the Business Environment",
        comodel_name="general_audit_ws_bdcdfc5",
        relation="general_audit_ws_c16abd7_bdcdfc5_rel",
        column1="ws_c16abd7_id",
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
        help="Overall assessed risk of material misstatement at the financial statement level.",
    )
    auditor_respons = fields.Text(
        string="Auditor Respons",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Planned auditor response considering the assessed risks "
            "at the financial statement level."
        ),
    )

    # Impacted standard account
    expert_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Use of Expert",
        comodel_name="client_account_type",
        related="general_audit_id.expert_impacted_account_type_ids",
        readonly=True,
        store=False,
        help="Account types impacted by the use of an expert (derived from General Audit).",
    )
    previous_audit_information_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Previous Audit Information",
        comodel_name="client_account_type",
        related="general_audit_id.previous_audit_information_impacted_account_type_ids",
        readonly=True,
        store=False,
        help=(
            "Account types impacted by previous audit information "
            "(derived from General Audit)."
        ),
    )
    previous_other_information_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Previous Other Information",
        comodel_name="client_account_type",
        related="general_audit_id.previous_other_information_impacted_account_type_ids",
        readonly=True,
        store=False,
        help=(
            "Account types impacted by previous other information "
            "(derived from General Audit)."
        ),
    )
    other_information_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Other Information",
        comodel_name="client_account_type",
        related="general_audit_id.other_information_impacted_account_type_ids",
        readonly=True,
        store=False,
        help="Account types impacted by other information (derived from General Audit).",
    )
    regulation_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Relevant Regulations",
        comodel_name="client_account_type",
        related="general_audit_id.regulation_impacted_account_type_ids",
        readonly=True,
        store=False,
        help="Account types impacted by relevant regulations (derived from General Audit).",
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
        help=(
            "Account types impacted by the preparation of "
            "financial statements (derived from General Audit)."
        ),
    )
    fraud_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Fraud Risk",
        comodel_name="client_account_type",
        related="general_audit_id.fraud_impacted_account_type_ids",
        readonly=True,
        store=False,
        help="Account types impacted by fraud risk (derived from General Audit).",
    )
    business_environment_impacted_account_type_ids = fields.Many2many(
        string="Standard Accounts Impacted by Business Environment",
        comodel_name="client_account_type",
        related="general_audit_id.business_environment_impacted_account_type_ids",
        readonly=True,
        store=False,
        help=(
            "Account types impacted by business environment factors "
            "(derived from General Audit)."
        ),
    )
