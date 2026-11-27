# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsF5a3ceeReportingTimetable(models.Model):
    """Reporting timetable line for the Data Collection worksheet (f5a3cee).

    One entry of the reporting timetable to be followed by the entity: a
    free-text description plus an optional date.  Rows are entered manually
    by the user; nothing is filled from master data.
    """

    _name = "general_audit_ws_f5a3cee.reporting_timetable"
    _description = "Data Collection (f5a3cee) - Reporting Timetable"
    _order = "id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_f5a3cee",
        required=True,
        index=True,
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
