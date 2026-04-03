# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSD8AAEBC(models.Model):
    """
    WS.010.1 — Engagement Letter Checklist (d8aaebc)

    Documents the auditor's review of terms of engagement as required by
    ISA 210 / SA 210 (Agreeing the Terms of Audit Engagements).  Before
    accepting or continuing an audit engagement the auditor must establish
    that the preconditions for an audit are present and that the engagement
    letter (or equivalent agreement) is in place and appropriately covers:

    - Management's responsibilities (financial statements, internal control,
      providing the auditor with all necessary information).
    - The auditor's responsibilities and the scope of the audit.
    - The form and content of the auditor's report.
    - Any agreed limitations on the scope of the engagement.

    This checklist worksheet systematically captures Yes/No/N-A responses
    for each required element, ensuring completeness before field work begins.
    The worksheet follows the standard worksheet workflow:
    Draft → Open → Confirm → Done.

    **ISA / SA references:** ISA 210 / SA 210 — Agreeing the Terms of
    Audit Engagements
    """

    _name = "general_audit_ws_d8aaebc"
    _description = "Engagement Letter Checklist (d8aaebc)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_engagement_letter_checklist."
        "worksheet_type_d8aaebc"
    )
    _checklist_model_name = "general_audit_ws_d8aaebc.checklist"
    _item_model_name = "general_audit_ws_d8aaebc.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_d8aaebc.checklist",
        help="""Checklist lines associated with this worksheet.
Each line captures the assessment/answer for a specific engagement-letter checklist item.""",
    )
