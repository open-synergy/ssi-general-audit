# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSd1ecfb7(models.Model):
    """
    Re-performance Audit Procedure Worksheet (WS-D1ECfb7).

    Implements the **Re-performance** audit procedure as defined in ISA 500 /
    SA 500 (Audit Evidence). Re-performance involves the auditor's independent
    execution of procedures or controls that were originally performed as part of
    the entity's internal control system — for example, re-performing the ageing
    of accounts receivable, re-reconciling a bank account, or independently
    re-executing an approval workflow to confirm that the control operates as
    designed.

    Unlike recalculation (which verifies only mathematical accuracy),
    re-performance re-executes the **complete procedure end-to-end**. This makes
    it especially effective as a test of controls: the auditor determines whether
    the control would have detected or prevented a material misstatement if it had
    been operating properly during the period under audit.

    **Audit purpose:**

    - Documents the auditor's full independent re-execution of a client procedure
      or internal control activity.
    - Links the re-performance to a specific Key Audit Procedure (WS-E51BB1C)
      and the relevant financial statement assertions.
    - Associates the worksheet with the relevant standard account type for
      traceability across the audit file.
    - Provides substantive evidence or test-of-controls evidence that complements
      inquiry, observation, and analytical procedures, supporting the auditor's
      conclusion under ISA 330.

    **ISA / SA references:** ISA 500 / SA 500 — Audit Evidence;
    ISA 315 / SA 315 — Identifying and Assessing the Risks of Material
    Misstatement; ISA 330 / SA 330 — The Auditor's Responses to Assessed Risks.
    """

    _name = "general_audit_ws_d1ecfb7"
    _description = "Reperformance Audit Procedure (d1ecfb7)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_audit_procedure_reperformance."
        "worksheet_type_d1ecfb7"
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
        relation="general_audit_ws_d1ecfb7_assertion_type_rel",
        column1="worksheet_id",
        column2="assertion_type_id",
        string="Assertion Types",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Assertion types relevant to this observation procedure.",
    )
    worksheet_result = fields.Text(
        string="Worksheet Result",
        help="Rich-text result or conclusion of this reperformance audit procedure.",
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
