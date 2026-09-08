# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWS0427d28(models.Model):
    """Worksheet: Communication With Previous Auditor.

    Documents the incoming auditor's communication with the predecessor
    (previous) auditor when accepting a new audit engagement, as required by
    SA 300 (Planning an Audit of Financial Statements) and the IAPI Code of
    Ethics. This step is mandatory for initial engagements.

    The worksheet automatically distinguishes engagement type based on
    ``num_of_consecutive_audit_firm`` from the parent General Audit record:

    - **Initial Engagement** (``engagemet_ok = False``): Fewer than 2
      consecutive years with the same firm; communication with the predecessor
      auditor is required.
    - **Recurring Engagement** (``engagemet_ok = True``): Firm has audited
      the client for 2 or more consecutive years; communication is not mandatory.

    A checklist evaluates whether the required communications have been made
    and any relevant information from the predecessor has been obtained.

    Model: ``general_audit_ws_0427d28``
    SA Reference: SA 300, Code of Ethics IAPI
    Module: ``ssi_general_audit_worksheet_acceptance_continuance``
    """

    _name = "general_audit_ws_0427d28"
    _description = "Communication With Previous Auditor (0427d28)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_0427d28"
    )
    _checklist_model_name = "general_audit_ws_0427d28.checklist"
    _item_model_name = "general_audit_ws_0427d28.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_0427d28.checklist",
        help=(
            "Checklist lines associated with this worksheet "
            "(Communication With Previous Auditor)."
        ),
    )
    risk = fields.Selection(
        string="Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("tidak_relevan", "Not Relevant"),
        ],
        help="Risk assessment for the communication with the previous auditor,\n"
        "including the 'Not Relevant' option when applicable.",
    )
    previous_partner_in_charge = fields.Char(
        string="Previous Partner in Charge",
        help=(
            "Free-text name of the partner in charge at the predecessor "
            "(previous) audit firm. Not a reference to res.partner/"
            "res.users, as no record for the predecessor auditor exists "
            "in the system."
        ),
    )
    previous_report_number = fields.Char(
        string="Previous Report Number",
        help="Report number issued by the predecessor (previous) auditor.",
    )
    previous_report_date = fields.Date(
        string="Previous Report Date",
        help="Date of the report issued by the predecessor (previous) " "auditor.",
    )
    previous_opinion_id = fields.Many2one(
        string="Previous Opinion",
        comodel_name="accountant.opinion",
        help=(
            "Opinion issued by the predecessor (previous) auditor. This "
            "field is unrelated to the current engagement's "
            "general_audit_id.opinion_id; it purely documents information "
            "obtained from the predecessor auditor on this worksheet."
        ),
    )

    @api.depends("general_audit_id", "general_audit_id.num_of_consecutive_audit_firm")
    def _compute_engagemet(self):
        for record in self:
            record.engagemet = "Initial Engagement"
            record.engagemet_ok = False
            if (record.general_audit_id.num_of_consecutive_audit_firm) > 1:
                record.engagemet = "Recurring Engagement"
                record.engagemet_ok = True

    engagemet = fields.Char(
        string="Engagement",
        compute="_compute_engagemet",
        compute_sudo=True,
        store=True,
        help="Computed engagement type based on consecutive audits with the firm:\n"
        "'Initial Engagement' or 'Recurring Engagement'.",
    )
    engagemet_ok = fields.Boolean(
        string="Engagement Type",
        compute="_compute_engagemet",
        compute_sudo=True,
        store=True,
        help=(
            "Computed flag indicating whether the engagement "
            "is recurring (True) or initial (False)."
        ),
    )
