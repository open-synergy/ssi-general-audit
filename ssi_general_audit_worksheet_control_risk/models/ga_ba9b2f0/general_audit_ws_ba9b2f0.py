# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSBA9B2F0(models.Model):
    """Worksheet — Significant Account Internal Control (ba9b2f0).

    Evaluates the design and operating effectiveness of key internal controls
    for one significant account type (e.g., Revenue, Accounts Receivable,
    Inventory).  The auditor selects the relevant ``account_type_id`` and the
    applicable key internal controls are auto-filtered from the master.

    For each control, the auditor identifies:
    * What can go wrong (WCGW) at the assertion level
    * Risk identification items linked to the business-risk register
    * Assessment of whether the control is effective (driving the overall
      ``risk`` conclusion: Low or High)

    This worksheet is central to the risk-response strategy: a 'Low' control
    risk conclusion supports a reliance-on-controls testing approach, while
    'High' calls for expanded substantive procedures.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 315/SA 315 (Identifying and Assessing Risks);
    ISA 330/SA 330 (Auditor's Responses to Assessed Risks).
    """

    _name = "general_audit_ws_ba9b2f0"
    _description = "Significant Account Internal Control (ba9b2f0)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_control_risk." "worksheet_type_ba9b2f0"

    risk = fields.Selection(
        string="Risk",
        selection=[
            ("low", "Low"),
            ("high", "High"),
        ],
        help="Overall risk assessment for this worksheet based on the checklist evaluation.",
    )
    account_type_id = fields.Many2one(
        string="Standard Account",
        comodel_name="client_account_type",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Standard account type being evaluated in this worksheet.",
    )
    account_key_internal_control_ids = fields.Many2many(
        string="Allowed Significant Account Key Internal Controls",
        related="account_type_id.account_key_internal_control_ids",
        store=False,
        help=(
            "Allowed key internal controls derived from the selected standard "
            "account type."
        ),
    )
    significant_risk_account_type_ids = fields.Many2many(
        string="Significant Account Types",
        related="general_audit_id.significant_risk_account_type_ids",
        store=False,
        help=(
            "Standard account types marked as significant risks for the "
            "General Audit."
        ),
    )

    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="general_audit.standard_detail",
        compute="_compute_standard_detail_id",
        store=True,
        compute_sudo=True,
        help=(
            "Matched standard detail for the selected account type within this "
            "General Audit."
        ),
    )

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_ba9b2f0.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Detail lines describing controls for the selected standard account.",
    )

    @api.depends(
        "account_type_id",
    )
    def _compute_standard_detail_id(self):
        StandardDetail = self.env["general_audit.standard_detail"]
        for record in self:
            result = []
            general_audit = record.general_audit_id
            criteria = [
                ("general_audit_id", "=", general_audit.id),
                ("type_id", "=", record.account_type_id.id),
            ]
            standard_details = StandardDetail.search(criteria)
            if len(standard_details) > 0:
                result = standard_details[0]
            record.standard_detail_id = result

    @ssi_decorator.pre_confirm_check()
    def _10_check_account_type(self):
        self.ensure_one()
        criteria = [
            ("general_audit_id", "=", self.general_audit_id.id),
            ("type_id", "=", self.type_id.id),
            ("account_type_id", "=", self.account_type_id.id),
            ("id", "!=", self.id),
        ]
        check = self.search(criteria)
        if check:
            error_message = """
            Context: Confirmation for %s
            Database ID: %s
            Problem: Standard account %s is already used for General Audit %s.
            """ % (
                self.type_id.display_name,
                self.id,
                self.account_type_id.display_name,
                self.display_name,
            )
            raise ValidationError(_(error_message))
