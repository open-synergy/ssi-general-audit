# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbcc0d76ODetail(models.Model):
    _name = "general_audit_ws_bcc0d76.detail"
    _description = "Audit Quality (bcc0d76) - Detail"
    _order = "worksheet_id, sequence, general_worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_bcc0d76",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This detail will be removed if the worksheet is deleted."
        ),
    )
    state = fields.Selection(
        related="worksheet_id.state",
    )
    general_worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_worksheet",
    )
    parent_type_id = fields.Many2one(
        related="general_worksheet_id.parent_type_id",
        store=True,
    )
    code_internal = fields.Char(
        related="parent_type_id.code_internal",
        store=True,
    )
    sequence = fields.Integer(
        related="parent_type_id.sequence",
        store=True,
    )
    conclusion_id = fields.Many2one(related="general_worksheet_id.conclusion_id")
    conclusion = fields.Text(related="general_worksheet_id.conclusion")
    recommendation = fields.Text(
        string="Reviewer’s Recommendation",
    )
    follow_up = fields.Text(
        string="Follow-Up on Reviewer’s Recommendation",
    )
    review_result = fields.Selection(
        string="Review Result",
        selection=[("compliant", "Compliant"), ("non_compliant", "Non-Compliant")],
    )
    review_date = fields.Date(
        string="Date",
    )
