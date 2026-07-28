# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import api, fields, models


class GeneralAuditWSb9d8a5cSummary(models.Model):
    """Summary line: Aggregated assessment results per engagement team member.

    Provides a consolidated, per-person view of the competency, availability,
    and independency evaluation results within the ``general_audit_ws_b9d8a5c``
    worksheet. The summary is automatically populated from the individual
    analysis sub-records via computed fields.

    Computed fields:
    - ``compentency_result``: Derived from ``competency_analysis_ids``
    - ``availability_result``: Derived from ``availability_analysis_ids``
    - ``independency_result``: Derived from ``independency_analysis_ids``

    This summary allows the engagement partner to make a holistic decision
    about each proposed team member's overall suitability for the engagement,
    as required by SA 220 (Quality Control for an Audit of Financial Statements).

    Model: ``general_audit_ws_b9d8a5c.summary``
    Parent worksheet: ``general_audit_ws_b9d8a5c``
    SA Reference: SA 220
    """

    _name = "general_audit_ws_b9d8a5c.summary"
    _description = (
        "Competency, Availability and Independency "
        "Of Assignment Team (b9d8a5c) - summary"
    )
    _order = "sequence, id"
    _sql_constraints = [
        (
            "unique_worksheet_employee",
            "unique(worksheet_id, employee_id)",
            "Employee must be unique per worksheet.",
        ),
    ]

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_b9d8a5c",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        required=True,
        ondelete="restrict",
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
        compute_sudo=True,
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
        compute_sudo=True,
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
        compute_sudo=True,
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
        compute_sudo=True,
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
        ondelete="restrict",
    )
    state = fields.Selection(
        related="worksheet_id.state",
        compute_sudo=True,
    )
