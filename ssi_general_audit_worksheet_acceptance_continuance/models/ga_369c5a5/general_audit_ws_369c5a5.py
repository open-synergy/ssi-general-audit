# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS369c5a5(models.Model):
    """Worksheet: Previous Financial Reporting Issues.

    Documents and assesses issues identified in the client's prior-period
    financial reports. As part of the engagement acceptance procedures under
    SA 300 and SA 220, the auditor evaluates whether previous reporting
    problems — such as disagreements with management, material misstatements,
    delayed filings, or qualified opinions — elevate the risk of the engagement.

    The checklist-based assessment produces an overall risk level (Low /
    Medium / High) that contributes to the Acceptance and Continuance
    of Client Relationships Analysis (806c4e1).

    Model: ``general_audit_ws_369c5a5``
    SA Reference: SA 220, SA 300
    Module: ``ssi_general_audit_worksheet_acceptance_continuance``
    """

    _name = "general_audit_ws_369c5a5"
    _description = "Previous Financial Reporting Issues (369c5a5)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_369c5a5"
    )
    _checklist_model_name = "general_audit_ws_369c5a5.checklist"
    _item_model_name = "general_audit_ws_369c5a5.item"

    risk = fields.Selection(
        string="Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        help="Overall risk assessment for this worksheet based on the checklist evaluation.",
    )

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_369c5a5.checklist",
        help=(
            "Checklist lines associated with this worksheet "
            "(Previous Financial Reporting Issues)."
        ),
    )
