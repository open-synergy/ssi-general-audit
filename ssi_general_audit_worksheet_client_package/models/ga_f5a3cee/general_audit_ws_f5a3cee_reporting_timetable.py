# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsF5a3ceeReportingTimetable(models.Model):
    """Reporting timetable line for the Data Collection worksheet (f5a3cee).

    Tracks a manually entered reporting deliverable (free-text description
    plus an optional due/received date), independent from ``detail_ids``
    which is auto-populated from the client's account mapping.  Rows are
    added and removed by the user, not by any automated process.
    """

    _name = "general_audit_ws_f5a3cee.reporting_timetable"
    _description = "Data Collection (f5a3cee) - Reporting Timetable"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_f5a3cee",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent Data Collection worksheet. "
            "Deleting the worksheet will remove its reporting timetable "
            "lines."
        ),
    )
    description = fields.Char(
        string="Description",
        required=True,
        help="Free-text description of the reporting deliverable.",
    )
    date = fields.Date(
        string="Date",
        required=False,
        help="Date associated with the reporting deliverable.",
    )
    attachment_ids = fields.Many2many(
        string="Attachments",
        comodel_name="ir.attachment",
        relation="rel_ga_f5a3cee_reporting_timetable_2_attachment",
        column1="f5a3cee_reporting_timetable_id",
        column2="attachment_id",
        domain="[('res_model', '=', 'general_audit_ws_f5a3cee'), "
        "('res_id', '=', worksheet_id)]",
        help=(
            "Files attached as supporting evidence. "
            "Only attachments linked to this worksheet can be selected."
        ),
    )
    complete_ok = fields.Boolean(
        string="Completed",
        default=False,
        help=(
            "Mark as completed once the reporting deliverable described "
            "by this line has been received and reviewed."
        ),
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help="State of the parent worksheet.",
    )
