# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsE59c663Checklist(models.Model):
    """Checklist line for the Draft Financial Statements worksheet.

    Stores the auditor's answer (Present/Not Present/Not Applicable) and
    any comments/attachments for one financial statement completeness
    item (WR.160.1).  Lines are auto-populated via ``mixin.checklist``
    from the ``general_audit_ws_e59c663.item`` master.
    """

    _name = "general_audit_ws_e59c663.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Draft Financial Statements (e59c663) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_e59c663",
        required=True,
        ondelete="cascade",
        help="Parent worksheet to which this checklist line belongs.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_e59c663.item",
        required=True,
        help="Checklist item that must be answered on this line.",
    )
    comment = fields.Text(
        help="Additional comment or explanation for this checklist item.",
    )
    attachment_ids = fields.Many2many(
        comodel_name="ir.attachment",
        relation="rel_ga_e59c663_checklist_2_attachment",
        column1="e59c663_checklist_id",
        column2="attachment_id",
        domain="[('res_model', '=', 'general_audit_ws_e59c663'),"
        "('res_id', '=', worksheet_id)]",
        help=(
            "Supporting documents for this checklist entry. "
            "Only files attached to the parent worksheet are selectable."
        ),
    )
