# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsE59c663ReviewChecklist(models.Model):
    """Review procedure checklist line for the Draft Financial
    Statements worksheet.

    Stores the auditor's answer (Yes/No) and any attachments for one
    review procedure item (WR.160). Lines are populated via
    ``action_populate_review_checklist`` (defined on
    ``general_audit_ws_e59c663``) from the
    ``general_audit_ws_e59c663.review_item`` master.
    """

    _name = "general_audit_ws_e59c663.review_checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Draft Financial Statements (e59c663) - Review Procedure Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_e59c663",
        required=True,
        ondelete="cascade",
        help="Parent worksheet to which this checklist line belongs.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_e59c663.review_item",
        required=True,
        help="Review procedure item that must be answered on this line.",
    )
    attachment_ids = fields.Many2many(
        comodel_name="ir.attachment",
        relation="rel_ga_e59c663_review_checklist_2_attachment",
        column1="e59c663_review_checklist_id",
        column2="attachment_id",
        domain="[('res_model', '=', 'general_audit_ws_e59c663'),"
        "('res_id', '=', worksheet_id)]",
        help=(
            "Supporting documents for this checklist entry. "
            "Only files attached to the parent worksheet are selectable."
        ),
    )
