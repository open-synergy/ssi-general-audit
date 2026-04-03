# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSEABDAAD(models.Model):
    """Worksheet — Business Cycle Internal Control (eabdaad).

    Evaluates the design and operating effectiveness of key internal controls
    for one business cycle (e.g., Sales & Receivables, Purchases & Payables,
    Payroll).  The auditor selects the relevant ``business_cycle_id`` and the
    applicable key internal controls are drawn from the master.

    For each key control, the worksheet records:
    * Control detail including the control activity and applicable assertions
    * What-Can-Go-Wrong (WCGW) scenarios at the assertion level
    * Risk identification items showing the risk the control is meant to address
    * The auditor's evaluation of control effectiveness, resulting in an overall
      ``risk`` conclusion (Low / High) for the cycle

    A 'Low' conclusion indicates the auditor intends to rely on those controls
    and will plan tests of controls; 'High' triggers expanded substantive testing.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 315/SA 315 (Identifying and Assessing Risks);
    ISA 330/SA 330 (Auditor's Responses to Assessed Risks).
    """

    _name = "general_audit_ws_eabdaad"
    _description = "Business Cycle Internal Control (eabdaad)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_control_risk." "worksheet_type_eabdaad"

    risk = fields.Selection(
        string="Risk",
        selection=[
            ("low", "Low"),
            ("high", "High"),
        ],
        help="Overall risk assessment for this worksheet based on the checklist evaluation.",
    )
    business_cycle_id = fields.Many2one(
        string="Business Cycle",
        comodel_name="client_business_process",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Business cycle being evaluated in this worksheet.",
    )
    key_internal_control_ids = fields.Many2many(
        string="Allowed Business Cycle Key Internal Controls",
        related="business_cycle_id.key_internal_control_ids",
        store=False,
        help="Allowed key internal controls for the selected business cycle.",
    )
    allowed_business_cycle_ids = fields.Many2many(
        string="Allowed Business Cycles",
        related="general_audit_id.business_cycle_ids",
        store=False,
        help="Business cycles included in scope for the General Audit.",
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_eabdaad.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Detail lines describing key controls within the business cycle.",
    )

    @ssi_decorator.pre_confirm_check()
    def _10_check_business_cycle(self):
        self.ensure_one()
        criteria = [
            ("general_audit_id", "=", self.general_audit_id.id),
            ("type_id", "=", self.type_id.id),
            ("business_cycle_id", "=", self.business_cycle_id.id),
            ("id", "!=", self.id),
        ]
        check = self.search(criteria)
        if check:
            error_message = """
            Context: Confirmation for %s
            Database ID: %s
            Problem: Business cycle %s is already used for General Audit %s.
            """ % (
                self.type_id.display_name,
                self.id,
                self.business_cycle_id.display_name,
                self.display_name,
            )
            raise ValidationError(_(error_message))
