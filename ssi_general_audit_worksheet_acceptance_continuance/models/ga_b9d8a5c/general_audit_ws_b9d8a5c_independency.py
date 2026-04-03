# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb9d8a5cIndependency(models.Model):
    """Analysis line: Independence assessment per engagement team member.

    Represents the individual independence evaluation for one team member
    within the ``general_audit_ws_b9d8a5c`` worksheet. The auditor assesses
    whether the employee is free from relationships, financial interests, or
    other circumstances that could compromise independence from the client.

    The ``analysis_item_ids`` field links to the predefined independence
    threat items (``general_audit_ws_b9d8a5c.independency_item``) that were
    identified for this team member.

    Result values:
    - ``sufficient``: The team member is independent from the client.
    - ``insufficient``: Independence threats exist that cannot be mitigated.

    Model: ``general_audit_ws_b9d8a5c.independency``
    Parent worksheet: ``general_audit_ws_b9d8a5c``
    SA Reference: SA 220, ISQC 1
    """

    _name = "general_audit_ws_b9d8a5c.independency"
    _description = (
        "Competency, Availability and Independency "
        "Of Assignment Team (b9d8a5c) - independency"
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
            ("insufficient", "Insufficient"),
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
        comodel_name="general_audit_ws_b9d8a5c.independency_item",
        relation="rel_ga_b9d8a5c_independency_2_independency_item",
        column1="independency_id",
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
