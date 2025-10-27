# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSa604795(models.Model):
    _name = "general_audit_ws_a604795"
    _description = "Business Cycle Summaries (a604795)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_a604795"
    )

    business_process_id = fields.Many2one(
        string="Business Cycle",
        comodel_name="client_business_process",
        readonly=True,
        ondelete="restrict",
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Selected business cycle for this worksheet. "
            "Editable only when the worksheet is Open."
        ),
    )
    ws_b9d8a5c_id = fields.Many2one(
        string="# Worksheet B9D8A5C",
        comodel_name="general_audit_ws_b9d8a5c",
        readonly=True,
        ondelete="restrict",
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Link to Worksheet B9D8A5C - Competency, "
            "Availability and Independency Of Assignment Team."
        ),
    )
    allowed_team_member_ids = fields.Many2many(
        string="Allowed Team Members",
        comodel_name="hr.employee",
        compute="_compute_allowed_team_member_ids",
        help=("Team members allowed to be assigned to " "work on this business cycle."),
    )
    assigned_team_member_ids = fields.Many2many(
        string="Assigned Team Members",
        comodel_name="hr.employee",
        relation="general_audit_ws_a604795_employee_rel",
        column1="worksheet_id",
        column2="employee_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=("Team members assigned to work on this " "business cycle."),
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_a604795.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Detailed assessment lines for this worksheet.",
    )

    def _compute_allowed_team_member_ids(self):
        for record in self:
            result = []
            if record.ws_b9d8a5c_id:
                result = record.ws_b9d8a5c_id.mapped("team_allocation_ids.team_id")
            record.allowed_team_member_ids = result

    @ssi_decorator.pre_confirm_check()
    def _10_check_business_process(self):
        self.ensure_one()
        criteria = [
            ("general_audit_id", "=", self.general_audit_id.id),
            ("type_id", "=", self.type_id.id),
            ("business_process_id", "=", self.business_process_id.id),
            ("id", "!=", self.id),
        ]
        check = self.search(criteria)
        if check:
            error_message = """
            Context: Confirmation for %s
            Database ID: %s
            Problem: Business cycle %s is already used for General Audit %s.
            """ % (
                self.type_id.display_name,
                self.id,
                self.business_process_id.display_name,
                self.display_name,
            )
            raise ValidationError(_(error_message))
