# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSb9d8a5cPersonnel(models.Model):
    """Detail line: Candidate personnel for the audit engagement team.

    Records each employee being considered for inclusion in the engagement
    team within the ``general_audit_ws_b9d8a5c`` worksheet. Each line
    captures the candidate's job role, years of experience, whether they
    are formally proposed as a team member, and supporting evidence
    attachments for competency verification.

    Only employees with ``audit_ok = True`` can be selected. This dataset
    forms the basis for the competency, availability, and independency
    analysis sub-records generated via ``action_create_summary``.

    Model: ``general_audit_ws_b9d8a5c.personnel``
    Parent worksheet: ``general_audit_ws_b9d8a5c``
    SA Reference: SA 220
    """

    _name = "general_audit_ws_b9d8a5c.personnel"
    _description = (
        "Competency, Availability and Independency "
        "Of Assignment Team (b9d8a5c) - Personnel"
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
        domain="[('audit_ok', '=', True)]",
        ondelete="restrict",
    )
    job_id = fields.Many2one(
        string="Job",
        comodel_name="hr.job",
        required=True,
        ondelete="restrict",
    )
    year_experience = fields.Integer(
        string="Experience (years)",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    proposed = fields.Selection(
        string="Proposed As Team",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        default="no",
    )
    competency_attachment_ids = fields.Many2many(
        string="Competency Attachments",
        comodel_name="ir.attachment",
        relation="rel_ga_b9d8a5c_personnel_2_competency",
        column1="b9d8a5c_personnel_id",
        column2="attachment_id",
        domain="[('res_model', '=', 'general_audit_ws_b9d8a5c'), "
        "('res_id', '=', worksheet_id)]",
    )

    time_availability_attachment_ids = fields.Many2many(
        string="Time Availability Attachments",
        comodel_name="ir.attachment",
        relation="rel_ga_b9d8a5c_personnel_2_time_availability",
        column1="b9d8a5c_personnel_id",
        column2="attachment_id",
        domain="[('res_model', '=', 'general_audit_ws_b9d8a5c'), "
        "('res_id', '=', worksheet_id)]",
    )

    state = fields.Selection(
        related="worksheet_id.state",
        compute_sudo=True,
    )

    @api.onchange(
        "employee_id",
    )
    def onchange_job_id(self):
        self.job_id = False
        if self.employee_id:
            self.job_id = self.employee_id.job_id
