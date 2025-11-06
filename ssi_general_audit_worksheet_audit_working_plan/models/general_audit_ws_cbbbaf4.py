# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSCBBBAF4(models.Model):
    _name = "general_audit_ws_cbbbaf4"
    _description = "Audit Working Plan (cbbbaf4)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_audit_working_plan." "worksheet_type_cbbbaf4"
    )

    budget_plan_status = fields.Selection(
        selection=[
            ("prepared", "Prepared"),
            ("not_prepared", "Not Prepared"),
        ],
        default="not_prepared",
    )
    industry_id = fields.Many2one(
        related="general_audit_id.industry_id",
    )
    ownership_type_id = fields.Many2one(
        related="general_audit_id.ownership_type_id",
    )
    engagement_date = fields.Date(
        string="Pre-Engagement Date",
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    risk_assessment_date = fields.Date(
        string="Risk Assessment Date",
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    fieldwork_date = fields.Date(
        string="Fieldwork Date",
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    pullout_date = fields.Date(
        string="Pullout Date",
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    reporting_date = fields.Date(
        string="Reporting Date",
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )

    @api.depends(
        "engagement_date",
        "reporting_date",
    )
    def _compute_effective_days(self):
        for rec in self:
            rec.effective_days = 0
            if rec.engagement_date and rec.reporting_date:
                start = rec.engagement_date
                end = rec.reporting_date
                day_count = 0
                current = start
                while current <= end:
                    if current.weekday() < 5:  # 0=Monday, ..., 4=Friday
                        day_count += 1
                    current += timedelta(days=1)
                rec.effective_days = day_count

    effective_days = fields.Integer(
        string="Number of Effective Days",
        compute="_compute_effective_days",
        compute_sudo=True,
    )

    # MAN HOUR ALLOCATION
    @api.model
    def default_allocation_template_id(self):
        company = self.env.company
        allocation = company.allocation_template_id
        return allocation and allocation.id or False

    allocation_template_id = fields.Many2one(
        string="Template",
        comodel_name="allocation_template",
        default=lambda self: self.default_allocation_template_id(),
        required=False,
        readonly=True,
        ondelete="restrict",
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    allocation_total_hour_id = fields.Many2one(
        string="Total Hour",
        comodel_name="allocation_total_hour",
        readonly=True,
        ondelete="restrict",
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    total_manhour_allocation = fields.Float(
        string="Total Manhour Allocation",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "allocation_template_id",
        "total_manhour_allocation",
        "allocation_template_id.pe_percentage",
        "allocation_template_id.ra_percentage",
        "allocation_template_id.rr_percentage",
        "allocation_template_id.wr_percentage",
    )
    def _compute_allocation(self):
        for rec in self:
            if rec.allocation_template_id and rec.total_manhour_allocation:
                total_hour = rec.total_manhour_allocation
                template_id = rec.allocation_template_id
                rec.pe_manhour_allocation = total_hour * template_id.pe_percentage / 100
                rec.ra_manhour_allocation = total_hour * template_id.ra_percentage / 100
                rec.rr_manhour_allocation = total_hour * template_id.rr_percentage / 100
                rec.wr_manhour_allocation = total_hour * template_id.wr_percentage / 100
            else:
                rec.pe_manhour_allocation = 0.0
                rec.ra_manhour_allocation = 0.0
                rec.rr_manhour_allocation = 0.0
                rec.wr_manhour_allocation = 0.0

    pe_manhour_allocation = fields.Float(
        string="Pre-Engagement Manhour Allocation",
        compute="_compute_allocation",
        compute_sudo=True,
        store=True,
    )
    ra_manhour_allocation = fields.Float(
        string="Risk Assessment Manhour Allocation",
        compute="_compute_allocation",
        compute_sudo=True,
        store=True,
    )
    rr_manhour_allocation = fields.Float(
        string="Risk Response Manhour Allocation",
        compute="_compute_allocation",
        compute_sudo=True,
        store=True,
    )
    wr_manhour_allocation = fields.Float(
        string="Reporting Manhour Allocation",
        compute="_compute_allocation",
        compute_sudo=True,
        store=True,
    )

    team_allocation_ids = fields.One2many(
        string="Team Allocations",
        comodel_name="general_audit_ws_cbbbaf4.team_allocation",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "team_allocation_ids",
        "team_allocation_ids.pe_allocation",
        "team_allocation_ids.ra_allocation",
        "team_allocation_ids.rr_allocation",
        "team_allocation_ids.reporting_allocation",
    )
    def _compute_total_manhour(self):
        for record in self:
            pe = ra = rr = reporting = 0.0
            for allocation in record.team_allocation_ids:
                pe += allocation.pe_allocation
                ra += allocation.ra_allocation
                rr += allocation.rr_allocation
                reporting += allocation.reporting_allocation
            record.total_pe_manhour = pe
            record.total_ra_manhour = ra
            record.total_rr_manhour = rr
            record.total_reporting_manhour = reporting
            record.total_manhour = pe + ra + rr + reporting

    total_pe_manhour = fields.Float(
        string="Total Pre-Engagement Allocation",
        compute="_compute_total_manhour",
        store=True,
        compute_sudo=True,
    )
    total_ra_manhour = fields.Float(
        string="Total Risk Assessment Allocation",
        compute="_compute_total_manhour",
        store=True,
        compute_sudo=True,
    )
    total_rr_manhour = fields.Float(
        string="Total Risk Response Allocation",
        compute="_compute_total_manhour",
        store=True,
        compute_sudo=True,
    )
    total_reporting_manhour = fields.Float(
        string="Total Reporting Allocation",
        compute="_compute_total_manhour",
        store=True,
        compute_sudo=True,
    )
    total_manhour = fields.Float(
        string="Total",
        compute="_compute_total_manhour",
        store=True,
        compute_sudo=True,
    )
    need_eqcr = fields.Boolean(
        string="Need EQCR",
        default=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    reasonable = fields.Boolean(
        string="Service hour allocation is reasonable?",
        default=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    team_competency_ids = fields.One2many(
        string="Team Competency Analysis",
        comodel_name="general_audit_ws_cbbbaf4.team_competency",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    # Different
    @api.depends(
        "pe_manhour_allocation",
        "ra_manhour_allocation",
        "rr_manhour_allocation",
        "wr_manhour_allocation",
        "total_manhour_allocation",
        "total_pe_manhour",
        "total_ra_manhour",
        "total_rr_manhour",
        "total_reporting_manhour",
        "total_manhour",
    )
    def _compute_diff_manhour(self):
        for record in self:
            record.diff_pe_manhour = (
                record.total_pe_manhour - record.pe_manhour_allocation
            )
            record.diff_ra_manhour = (
                record.total_ra_manhour - record.ra_manhour_allocation
            )
            record.diff_rr_manhour = (
                record.total_rr_manhour - record.rr_manhour_allocation
            )
            record.diff_reporting_manhour = (
                record.total_reporting_manhour - record.wr_manhour_allocation
            )
            record.dif_total_manhour = (
                record.total_manhour - record.total_manhour_allocation
            )

    diff_pe_manhour = fields.Float(
        string="Pre-Engagement",
        compute="_compute_diff_manhour",
        store=True,
        compute_sudo=True,
    )
    diff_ra_manhour = fields.Float(
        string="Risk Assessment",
        compute="_compute_diff_manhour",
        store=True,
        compute_sudo=True,
    )
    diff_rr_manhour = fields.Float(
        string="Risk Response",
        compute="_compute_diff_manhour",
        store=True,
        compute_sudo=True,
    )
    diff_reporting_manhour = fields.Float(
        string="Reporting",
        compute="_compute_diff_manhour",
        store=True,
        compute_sudo=True,
    )
    dif_total_manhour = fields.Float(
        string="Total",
        compute="_compute_diff_manhour",
        store=True,
        compute_sudo=True,
    )

    # LINK - 1 (PE.110)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_1_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_806c4e1"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_1_ids = obj.search(criteria).ids

    allowed_link_1_ids = fields.Many2many(
        string="Allowed Link 1",
        comodel_name="general_audit_ws_806c4e1",
        compute="_compute_allowed_link_1_ids",
        store=False,
    )

    link_1 = fields.Many2one(
        string="PE.110",
        ondelete="restrict",
        comodel_name="general_audit_ws_806c4e1",
    )
    link_1_risk = fields.Selection(
        string="Risk (PE.110)",
        related="link_1.risk",
        store=True,
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_1(self):
        self.link_1 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_806c4e1"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria)
            if result:
                self.link_1 = result.id

    # LINK - 2 (PE.110.3)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_2_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_b9d8a5c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_2_ids = obj.search(criteria).ids

    allowed_link_2_ids = fields.Many2many(
        string="Allowed Link 2",
        comodel_name="general_audit_ws_b9d8a5c",
        compute="_compute_allowed_link_2_ids",
        store=False,
    )
    link_2 = fields.Many2one(
        string="PE.110.3",
        ondelete="restrict",
        comodel_name="general_audit_ws_b9d8a5c",
    )
    link_2_risk = fields.Selection(
        string="Risk (PE.110.3)",
        related="link_2.risk",
        store=True,
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_2(self):
        self.link_2 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_b9d8a5c"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria)
            if result:
                self.link_2 = result.id

    @ssi_decorator.post_open_action()
    def _10_create_team(self):
        self.ensure_one()
        self._create_allocation_team()
        self._create_competency_team()

    def _create_allocation_team_data(self, summary):
        self.ensure_one()
        data = {
            "worksheet_id": self.id,
            "team_id": summary.employee_id.id,
            "sequence": summary.sequence,
            "role_id": summary.team_role_id.id,
        }
        return data

    def _update_allocation_team_data(self, summary):
        self.ensure_one()
        data = {
            "team_id": summary.employee_id.id,
            "sequence": summary.sequence,
            "role_id": summary.team_role_id.id,
        }
        return data

    def action_refresh_allocation_team(self):
        for record in self:
            record._create_allocation_team()

    def _create_allocation_team(self):
        self.ensure_one()
        Allocation = self.env["general_audit_ws_cbbbaf4.team_allocation"]

        if not self.link_2:
            return

        summaries = self.link_2.summary_ids.filtered(lambda x: x.select_team == "yes")
        emps = self.link_2.summary_ids.filtered(
            lambda x: x.select_team == "yes"
        ).mapped("employee_id")
        mapping = {chk.team_id.id: chk for chk in self.team_allocation_ids}
        for summary in summaries:
            if summary.employee_id.id not in mapping:
                Allocation.create(self._create_allocation_team_data(summary))
            else:
                mapping[summary.employee_id.id].write(
                    self._update_allocation_team_data(summary)
                )

        emp_ids = set(emps.ids)
        for chk in self.team_allocation_ids:
            if chk.team_id.id not in emp_ids:
                chk.unlink()

    def action_refresh_competency_team(self):
        for record in self:
            record._create_competency_team()

    def _prepare_competency_data(self, summary):
        self.ensure_one()
        data = []
        Competency = self.env["general_audit_ws_b9d8a5c.competency"]
        Upgrade = self.env["general_audit_competency_upgrade"]
        criteria = [
            ("employee_id", "=", summary.employee_id.id),
        ]
        competencies = Competency.search(criteria)
        if competencies:
            competency_item_ids = competencies.analysis_item_ids.ids
            upgrades = Upgrade.search([]).mapped("compentency_item_id").ids
            result = [x for x in upgrades if x not in competency_item_ids]
            data = (
                Upgrade.search([])
                .filtered(lambda y: y.compentency_item_id.id in result)
                .ids
            )
        return data

    def _create_competency_team_data(self, summary):
        self.ensure_one()
        competency_ids = self._prepare_competency_data(summary)
        data = {
            "worksheet_id": self.id,
            "team_id": summary.employee_id.id,
            "sequence": summary.sequence,
            "competency_upgrade_ids": [(6, 0, competency_ids)],
        }
        return data

    def _update_competency_team_data(self, summary):
        self.ensure_one()
        competency_ids = self._prepare_competency_data(summary)
        data = {
            "team_id": summary.employee_id.id,
            "sequence": summary.sequence,
            "competency_upgrade_ids": [(6, 0, competency_ids)],
        }
        return data

    def _create_competency_team(self):
        self.ensure_one()
        Competency = self.env["general_audit_ws_cbbbaf4.team_competency"]

        if not self.link_2:
            return

        summaries = self.link_2.summary_ids.filtered(lambda x: x.select_team == "yes")
        emps = self.link_2.summary_ids.filtered(
            lambda x: x.select_team == "yes"
        ).mapped("employee_id")
        mapping = {chk.team_id.id: chk for chk in self.team_competency_ids}
        for summary in summaries:
            if summary.employee_id.id not in mapping:
                Competency.create(self._create_competency_team_data(summary))
            else:
                mapping[summary.employee_id.id].write(
                    self._update_competency_team_data(summary)
                )

        emp_ids = set(emps.ids)
        for chk in self.team_competency_ids:
            if chk.team_id.id not in emp_ids:
                chk.unlink()

    @api.onchange(
        "allocation_total_hour_id",
        "allocation_total_hour_id.total_hour",
    )
    def onchange_total_manhour_allocation(self):
        if self.allocation_total_hour_id:
            self.total_manhour_allocation = self.allocation_total_hour_id.total_hour

    @api.constrains(
        "engagement_date",
        "risk_assessment_date",
        "fieldwork_date",
        "pullout_date",
        "reporting_date",
    )
    def _check_dates_order(self):
        for rec in self:
            if rec.reporting_date and rec.pullout_date:
                if rec.reporting_date < rec.pullout_date:
                    msg_err = "Reporting Date must be greater than Pullout Date."
                    raise ValidationError(msg_err)
            if rec.pullout_date and rec.fieldwork_date:
                if rec.pullout_date < rec.fieldwork_date:
                    msg_err = "Pullout Date must be greater than Fieldwork Date."
                    raise ValidationError(msg_err)
            if rec.fieldwork_date and rec.risk_assessment_date:
                if rec.fieldwork_date < rec.risk_assessment_date:
                    msg_err = (
                        "Fieldwork Date must be greater than Risk Assessment Date."
                    )
                    raise ValidationError(msg_err)
            if rec.risk_assessment_date and rec.engagement_date:
                if rec.risk_assessment_date < rec.engagement_date:
                    msg_err = (
                        "Risk Assessment Date must be greater than Engagement Date."
                    )
                    raise ValidationError(msg_err)

    def _get_fields_required_before_confirm(self):
        _super = super(GeneralAuditWSCBBBAF4, self)
        res = _super._get_fields_required_before_confirm()
        res += [
            "link_1",
            "link_2",
        ]
        return res

    def _get_custom_field_labels(self):
        return {
            "link_1": _("Acceptance and Continuance of Client Relationships Analysis"),
            "link_2": _(
                "Competency, availability, and " "independency of assignment team"
            ),
        }
