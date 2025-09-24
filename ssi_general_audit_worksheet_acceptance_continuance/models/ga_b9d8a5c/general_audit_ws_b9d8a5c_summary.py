# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import api, fields, models


class GeneralAuditWSb9d8a5cSummary(models.Model):
    _name = "general_audit_ws_b9d8a5c.summary"
    _description = (
        "Competency, Availability and Independency "
        "Of Assignment Team (b9d8a5c) - summary"
    )

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_b9d8a5c",
        required=True,
        ondelete="cascade",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        required=True,
    )

    @api.depends(
        "employee_id",
        "worksheet_id",
        "worksheet_id.competency_analysis_ids",
    )
    def _compute_compentency_result(self):
        for document in self:
            result = ""
            if document.employee_id and document.worksheet_id:
                competency = document.worksheet_id.competency_analysis_ids.filtered(
                    lambda x: x.employee_id == document.employee_id
                )
                if competency:
                    result = dict(competency[0]._fields["result"].selection).get(
                        competency[0].result, ""
                    )
            document.compentency_result = result

    compentency_result = fields.Char(
        string="Compentency",
        compute="_compute_compentency_result",
        store=True,
    )

    @api.depends(
        "employee_id",
        "worksheet_id",
        "worksheet_id.availability_analysis_ids",
    )
    def _compute_availability_result(self):
        for document in self:
            result = ""
            if document.employee_id and document.worksheet_id:
                availability = document.worksheet_id.availability_analysis_ids.filtered(
                    lambda x: x.employee_id == document.employee_id
                )
                if availability:
                    result = dict(availability[0]._fields["result"].selection).get(
                        availability[0].result, ""
                    )
            document.availability_result = result

    availability_result = fields.Char(
        string="Availability",
        compute="_compute_availability_result",
        store=True,
    )

    @api.depends(
        "employee_id",
        "worksheet_id",
        "worksheet_id.independency_analysis_ids",
    )
    def _compute_independency_result(self):
        for document in self:
            result = ""
            if document.employee_id and document.worksheet_id:
                independency = document.worksheet_id.independency_analysis_ids.filtered(
                    lambda x: x.employee_id == document.employee_id
                )
                if independency:
                    result = dict(independency[0]._fields["result"].selection).get(
                        independency[0].result, ""
                    )
            document.independency_result = result

    independency_result = fields.Char(
        string="Independency",
        compute="_compute_independency_result",
        store=True,
    )
    select_team = fields.Selection(
        string="Select As Team",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    initials = fields.Char(
        related="employee_id.initials",
    )
    team_role_id = fields.Many2one(
        string="Team Role",
        comodel_name="team_role",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        related="worksheet_id.state",
    )
