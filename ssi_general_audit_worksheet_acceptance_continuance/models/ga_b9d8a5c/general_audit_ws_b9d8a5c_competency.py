# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import api, fields, models


class GeneralAuditWSb9d8a5cComptency(models.Model):
    """Analysis line: Competency assessment per engagement team member.

    Represents the individual professional competency evaluation for one
    team member within the ``general_audit_ws_b9d8a5c`` worksheet. The
    auditor assesses whether the employee has sufficient knowledge, skills,
    and qualifications for the specific requirements of the engagement.

    The ``year_experience`` is automatically derived from the corresponding
    ``general_audit_ws_b9d8a5c.personnel`` record. The ``analysis_item_ids``
    field links to the predefined competency criteria that were evaluated.

    Result values:
    - ``sufficient``: The team member meets the competency requirements.
    - ``need_update``: Additional training or supervision required.

    Model: ``general_audit_ws_b9d8a5c.competency``
    Parent worksheet: ``general_audit_ws_b9d8a5c``
    SA Reference: SA 220
    """

    _name = "general_audit_ws_b9d8a5c.competency"
    _description = (
        "Competency, Availability and Independency "
        "Of Assignment Team (b9d8a5c) - Competency"
    )
    _order = "sequence, id"

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
    )
    def _compute_year_experience(self):
        Personnel = self.env["general_audit_ws_b9d8a5c.personnel"]
        for record in self:
            criteria = [
                ("worksheet_id", "=", record.worksheet_id.id),
                ("employee_id", "=", record.employee_id.id),
            ]
            personnel = Personnel.search(criteria)
            if personnel:
                record.year_experience = personnel.year_experience
            else:
                record.year_experience = 0

    year_experience = fields.Integer(
        string="Experience (years)",
        compute="_compute_year_experience",
    )
    result = fields.Selection(
        string="Result",
        selection=[
            ("sufficient", "Sufficient"),
            ("need_update", "Need Update"),
        ],
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    analysis_item_ids = fields.Many2many(
        string="Analysis",
        comodel_name="general_audit_ws_b9d8a5c.competency_item",
        relation="rel_ga_b9d8a5c_competency_2_competency_item",
        column1="competency_id",
        column2="item_id",
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
