# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSd45dd19(models.Model):
    """Worksheet for External Confirmation Audit Procedure.

    This worksheet implements the **external confirmation** audit procedure
    as defined in ISA 505 / SA 505 (External Confirmations). External
    confirmation is the process of obtaining and evaluating audit evidence
    through a direct written response from a third party (the confirming
    party) to the auditor, in paper form or by electronic or other medium.

    Typical use cases include:
    - Confirming account receivable balances directly with customers
    - Confirming bank account balances and credit facilities with banks
    - Confirming terms of contracts or agreements with counterparties
    - Confirming legal matters with the client's legal counsel

    Workflow context:
    - References a Key Audit Procedures worksheet (WS-E51BB1C / Lead Schedule)
      to link each confirmation to a specific audit area and assertion
    - Linked to a specific key audit procedure category and assertion types
      (e.g., Existence, Rights & Obligations, Completeness, Accuracy)
    - The ``account_type_id`` field ties the confirmation to the relevant
      financial statement account being audited

    ISA/SA references: ISA 505, SA 505 — External Confirmations
    """

    _name = "general_audit_ws_d45dd19"
    _description = "Confirmation Audit Procedure (d45dd19)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_audit_procedure_confirmation."
        "worksheet_type_d45dd19"
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
        relation="general_audit_ws_d45dd19_assertion_type_rel",
        column1="worksheet_id",
        column2="assertion_type_id",
        string="Assertion Types",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Assertion types relevant to this observation procedure.",
    )
    confirmation_ids = fields.One2many(
        comodel_name="general_audit_ws_d45dd19.confirmation",
        inverse_name="worksheet_id",
        string="Confirmations",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="List of external confirmation requests associated with this "
        "confirmation procedure worksheet.",
    )
    tolerable_amount = fields.Float(
        string="Tolerable Amount",
        digits=(16, 2),
        default=0.0,
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Absolute tolerance for comparing Original vs Confirmation Amount. "
        "Differences within this threshold are considered agreed.",
    )
    # ── Audit Results — Kfo ──────────────────────────────────────────────────
    kfo_amount = fields.Float(
        string="Kfo – Amount (Rp)",
        digits=(16, 2),
        compute="_compute_audit_results",
        store=True,
        compute_sudo=True,
        help="Total book balance (IDR) of confirmations with status Kfo "
        "(Confirmation returned, agreed).",
    )
    kfo_percentage = fields.Float(
        string="Kfo – Percentage (%)",
        digits=(5, 2),
        compute="_compute_audit_results",
        store=True,
        compute_sudo=True,
    )
    kfo_alternative_procedure = fields.Boolean(
        string="Kfo – Alternative Procedure",
        default=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    kfo_alternative_procedure_info = fields.Text(
        string="Kfo – Alternative Procedure Info",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Description of alternative audit procedure performed when "
        "confirmation returned and agreed (Kfo).",
    )
    kfo_document_ref = fields.Char(
        string="Kfo – Document Reference",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Reference number of the supporting document for the "
        "alternative procedure (Kfo).",
    )
    kfo_conclusion = fields.Text(
        string="Kfo – Conclusion",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    # ── Audit Results — Kfb ──────────────────────────────────────────────────
    kfb_amount = fields.Float(
        string="Kfb – Amount (Rp)",
        digits=(16, 2),
        compute="_compute_audit_results",
        store=True,
        compute_sudo=True,
        help="Total book balance (IDR) of confirmations with status Kfb "
        "(Confirmation returned, different).",
    )
    kfb_percentage = fields.Float(
        string="Kfb – Percentage (%)",
        digits=(5, 2),
        compute="_compute_audit_results",
        store=True,
        compute_sudo=True,
    )
    kfb_alternative_procedure = fields.Boolean(
        string="Kfb – Alternative Procedure",
        default=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    kfb_alternative_procedure_info = fields.Text(
        string="Kfb – Alternative Procedure Info",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Description of alternative audit procedure performed when "
        "confirmation returned with differences (Kfb).",
    )
    kfb_document_ref = fields.Char(
        string="Kfb – Document Reference",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Reference number of the supporting document for the "
        "alternative procedure (Kfb).",
    )
    kfb_conclusion = fields.Text(
        string="Kfb – Conclusion",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    # ── Audit Results — Kft ──────────────────────────────────────────────────
    kft_amount = fields.Float(
        string="Kft – Amount (Rp)",
        digits=(16, 2),
        compute="_compute_audit_results",
        store=True,
        compute_sudo=True,
        help="Total book balance (IDR) of confirmations with status Kft "
        "(Confirmation not returned).",
    )
    kft_percentage = fields.Float(
        string="Kft – Percentage (%)",
        digits=(5, 2),
        compute="_compute_audit_results",
        store=True,
        compute_sudo=True,
    )
    kft_alternative_procedure = fields.Boolean(
        string="Kft – Alternative Procedure",
        default=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    kft_alternative_procedure_info = fields.Text(
        string="Kft – Alternative Procedure Info",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Description of alternative audit procedure performed when "
        "confirmation was not returned (Kft).",
    )
    kft_document_ref = fields.Char(
        string="Kft – Document Reference",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Reference number of the supporting document for the "
        "alternative procedure (Kft).",
    )
    kft_conclusion = fields.Text(
        string="Kft – Conclusion",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    # ── Audit Results — Kfk ──────────────────────────────────────────────────
    kfk_amount = fields.Float(
        string="Kfk – Amount (Rp)",
        digits=(16, 2),
        compute="_compute_audit_results",
        store=True,
        compute_sudo=True,
        help="Total book balance (IDR) of confirmations with status Kfk "
        "(Confirmation undeliverable).",
    )
    kfk_percentage = fields.Float(
        string="Kfk – Percentage (%)",
        digits=(5, 2),
        compute="_compute_audit_results",
        store=True,
        compute_sudo=True,
    )
    kfk_alternative_procedure = fields.Boolean(
        string="Kfk – Alternative Procedure",
        default=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    kfk_alternative_procedure_info = fields.Text(
        string="Kfk – Alternative Procedure Info",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Description of alternative audit procedure performed when "
        "confirmation was undeliverable (Kfk).",
    )
    kfk_document_ref = fields.Char(
        string="Kfk – Document Reference",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Reference number of the supporting document for the "
        "alternative procedure (Kfk).",
    )
    kfk_conclusion = fields.Text(
        string="Kfk – Conclusion",
        readonly=True,
        states={"open": [("readonly", False)]},
    )

    @api.depends(
        "confirmation_ids",
        "confirmation_ids.result_status",
        "confirmation_ids.detail_ids.confirmation_data",
    )
    def _compute_audit_results(self):
        for record in self:
            total = 0.0
            for conf in record.confirmation_ids:
                for detail in conf.detail_ids:
                    total += detail._get_total_original_amount()
            for status in ("kfo", "kfb", "kft", "kfk"):
                confs = record.confirmation_ids.filtered(
                    lambda c, s=status: c.result_status == s
                )
                amount = 0.0
                for conf in confs:
                    for detail in conf.detail_ids:
                        amount += detail._get_total_original_amount()
                setattr(record, f"{status}_amount", amount)
                setattr(
                    record,
                    f"{status}_percentage",
                    (amount / total * 100.0) if total else 0.0,
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

    def action_open_confirmations(self):
        self.ensure_one()
        action = self.env.ref(
            "ssi_general_audit_worksheet_audit_procedure_confirmation"
            ".general_audit_ws_d45dd19_confirmation_action"
        ).read()[0]
        action["domain"] = [("worksheet_id", "=", self.id)]
        action["context"] = {"default_worksheet_id": self.id}
        return action
