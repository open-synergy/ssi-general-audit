# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb9d8a5cAvailability(models.Model):
    """Analysis line: Availability assessment per engagement team member.

    Represents the individual time-availability evaluation for one team
    member within the ``general_audit_ws_b9d8a5c`` worksheet. The auditor
    assesses whether the employee has adequate scheduled time to fulfil the
    engagement obligations without conflicts or time constraints.

    The ``analysis_item_ids`` field links to the predefined availability
    criteria (``general_audit_ws_b9d8a5c.availability_item``) that were
    evaluated.

    Result values:
    - ``sufficient``: The team member has adequate capacity for the engagement.
    - ``time_constraint``: Scheduling conflicts or workload issues exist.

    Model: ``general_audit_ws_b9d8a5c.availability``
    Parent worksheet: ``general_audit_ws_b9d8a5c``
    SA Reference: SA 220
    """

    _name = "general_audit_ws_b9d8a5c.availability"
    _description = (
        "Competency, Availability and Independency "
        "Of Assignment Team (b9d8a5c) - availability"
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
    result = fields.Selection(
        string="Result",
        selection=[
            ("sufficient", "Sufficient"),
            ("time_constraint", "There is time constraint"),
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
        comodel_name="general_audit_ws_b9d8a5c.availability_item",
        relation="rel_ga_b9d8a5c_availability_2_availability_item",
        column1="availability_id",
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
        compute_sudo=True,
    )
