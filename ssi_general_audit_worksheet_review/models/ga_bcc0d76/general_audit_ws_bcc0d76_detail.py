# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbcc0d76ODetail(models.Model):
    """
    Quality review detail line for Audit Quality Review (bcc0d76).

    One record per main worksheet reviewed; stores the reviewer's quality
    assessment for that worksheet including:

    * ``general_worksheet_id`` — the linked ``general_audit_worksheet`` record.
    * ``parent_type_id`` / ``sequence`` / ``code_internal`` — for ordering.
    * ``conclusion_id`` / ``review`` — conclusion and review notes carried
      from the worksheet record.
    * ``review_result`` — reviewer's quality judgment (Satisfactory,
      Needs Improvement, Unsatisfactory, etc.).

    These records are referenced 1-to-1 by the Audit Evidence Evaluation
    worksheet (``general_audit_ws_cae598e.detail``).
    """

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
        help="State of the parent worksheet.",
    )
    general_worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_worksheet",
        ondelete="restrict",
        help="Linked general worksheet being reviewed in this record.",
    )
    parent_type_id = fields.Many2one(
        related="general_worksheet_id.parent_type_id",
        store=True,
        help="Type/category of the linked general worksheet.",
    )
    code_internal = fields.Char(
        related="parent_type_id.code_internal",
        store=True,
        help="Internal code of the worksheet type used for ordering or grouping.",
    )
    sequence = fields.Integer(
        related="parent_type_id.sequence",
        store=True,
        help="Ordering sequence of the worksheet type.",
    )
    conclusion_id = fields.Many2one(
        related="general_worksheet_id.conclusion_id",
        help="Conclusion record associated with the linked worksheet.",
    )
    conclusion = fields.Text(
        related="general_worksheet_id.conclusion",
        help="Conclusion text taken from the linked worksheet.",
    )
    recommendation = fields.Text(
        string="Reviewer’s Recommendation",
        help="Reviewer’s recommendation based on the evaluation of the worksheet.",
    )
    follow_up = fields.Text(
        string="Follow-Up on Reviewer’s Recommendation",
        help=(
            "Actions taken or proposed to address the reviewer’s recommendation, "
            "including responsible parties and timelines if applicable."
        ),
    )
    review_result = fields.Selection(
        string="Review Result",
        selection=[("compliant", "Comply"), ("non_compliant", "Not Comply")],
        help="Outcome of the review for this area: Comply or Not Comply.",
    )
    review_date = fields.Date(
        string="Date",
        help="Date when the review was performed or finalized.",
    )
