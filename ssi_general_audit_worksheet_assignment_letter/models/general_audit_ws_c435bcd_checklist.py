# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc435bcdChecklist(models.Model):
    """Individual checklist response entry for the Assignment Letter worksheet.

    Each record represents an auditor's answer to one checklist item
    (``general_audit_ws_c435bcd.item``) within a specific Assignment Letter
    worksheet (``general_audit_ws_c435bcd``).  The record is owned by the
    worksheet and is automatically deleted when the worksheet is removed.

    Inherits ``mixin.checklist.value`` which provides:
    - ``option_id`` — the selected answer option (e.g. Yes / No / N/A).
    - ``notes`` — free-text remarks from the auditor.
    - Computed fields for presenting the result in summarised views.

    Typical usage
    -------------
    When an auditor opens the Assignment Letter worksheet, the system
    auto-populates one checklist row per active ``general_audit_ws_c435bcd.item``
    template.  The auditor selects an option for each row and saves the form.
    """

    _name = "general_audit_ws_c435bcd.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Assignment Letter (c435bcd) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_c435bcd",
        required=True,
        ondelete="cascade",
        help="Reference to the Assignment Letter worksheet that this "
        "checklist item belongs to. When the worksheet is deleted, "
        "this checklist entry will be automatically removed.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_c435bcd.item",
        required=True,
        help="The specific checklist item template that defines what needs "
        "to be verified or completed for this assignment letter worksheet.",
    )
