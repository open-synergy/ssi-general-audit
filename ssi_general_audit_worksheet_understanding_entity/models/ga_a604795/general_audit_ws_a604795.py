# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSa604795(models.Model):
    """Worksheet: Business Cycle Summaries (a604795) — RA.150.4.

    Documents the detailed analysis of the entity's business cycles (transaction
    classes) as part of understanding the entity and its environment, in
    accordance with ISA 315 (Revised) / SA 315.

    For each business cycle (e.g., revenue cycle, procurement cycle, payroll
    cycle), the auditor documents:

    - Business process selected (``business_process_id``)
    - Estimated transaction volume for the period
    - Classes of transactions within the cycle (``detail_ids``)
    - Business functions that drive each transaction class
    - Business documents used or generated per function
    - Related account types affected by the cycle
    - Assigned audit team members responsible for this cycle
    - Link to the Audit Working Plan worksheet (``ws_cbbbaf4_id``)

    Understanding transaction classes and business functions enables the auditor
    to assess where misstatements could arise, identify controls to test, and
    design appropriate audit responses.

    Inherits from ``general_audit_worksheet_mixin``.
    """

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
    estimated_transaction_volume = fields.Integer(
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Estimated number of transactions expected to occur within the scope "
            "of this business cycle for the relevant audit period. Editable only "
            "when the worksheet is Open."
        ),
    )

    main_business_activity_process_id = fields.Many2one(
        string="Main Business Activity Process",
        comodel_name="general_audit_ws_ae11f7e",
        compute="_compute_main_business_activity_process_id",
        compute_sudo=True,
        store=True,
        help=(
            "Main Business Activity Process (KKA RA.150.3) worksheet for "
            "the same General Audit engagement. Provided so this "
            "worksheet can be cross-referenced back to its Main Business "
            "Activity Process without duplicating the lookup logic."
        ),
    )

    @api.depends("general_audit_id")
    def _compute_main_business_activity_process_id(self):
        """Cross-reference this business cycle to its KKA RA.150.3.

        Resolve the "Main Business Activity Process" (RA.150.3) worksheet
        belonging to the same General Audit as this "Business Cycle
        Summaries" (RA.150.4) worksheet. Mirrors, in reverse, the
        ``business_cycle_summary_ids`` lookup on
        ``general_audit_ws_ae11f7e``.

        :return: nothing; assigns ``main_business_activity_process_id``
        """
        Worksheet = self.env["general_audit_ws_ae11f7e"]  # pylint: disable=invalid-name
        for record in self:
            result = False
            if record.general_audit_id:
                worksheet = Worksheet.search(
                    [("general_audit_id", "=", record.general_audit_id.id)],
                    limit=1,
                )
                result = worksheet.id if worksheet else False
            record.main_business_activity_process_id = result

    def _compute_allowed_ws_cbbbaf4_ids(self):
        for record in self:
            result = []
            Worksheet = self.env["general_audit_ws_cbbbaf4"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            worksheets = Worksheet.search(criteria)
            if worksheets:
                result = worksheets.ids
            record.allowed_ws_cbbbaf4_ids = [(6, 0, result)]

    allowed_ws_cbbbaf4_ids = fields.Many2many(
        string="Allowed Worksheet CBBAF4",
        comodel_name="general_audit_ws_cbbbaf4",
        compute="_compute_allowed_ws_cbbbaf4_ids",
        help=("Worksheet CBBAF4 allowed to work on this business cycle."),
    )

    ws_cbbbaf4_id = fields.Many2one(
        string="# Worksheet CBBAF4",
        comodel_name="general_audit_ws_cbbbaf4",
        readonly=True,
        ondelete="restrict",
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=("Link to Worksheet CBBAF4 - " "Audit Working Plan."),
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

    def _compute_member_initials(self):
        for rec in self:
            initials = rec.assigned_team_member_ids.mapped("initials")
            rec.member_initials = ", ".join(initials)

    member_initials = fields.Char(
        string="Initials", compute="_compute_member_initials", store=False
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
            if record.ws_cbbbaf4_id:
                result = record.ws_cbbbaf4_id.mapped("team_allocation_ids.team_id").ids
            record.allowed_team_member_ids = [(6, 0, result)]

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

    def _get_fields_required_before_confirm(self):
        _super = super(GeneralAuditWSa604795, self)
        res = _super._get_fields_required_before_confirm()
        res += ["ws_cbbbaf4_id"]
        return res
