# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb9d8a5cAvailability(models.Model):
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
    )
    result = fields.Selection(
        string="Result",
        selection=[
            ("sufficient", "Sufficient"),
            ("time_limit", "There Is Time Limit"),
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
    )
