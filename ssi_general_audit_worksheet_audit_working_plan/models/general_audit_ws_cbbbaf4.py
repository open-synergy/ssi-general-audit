# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSCBBBAF4(models.Model):
    _name = "general_audit_ws_cbbbaf4"
    _description = "Audit Working Plan (cbbbaf4)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_audit_working_plan." "worksheet_type_cbbbaf4"
    )

    engagement_date = fields.Date(
        string="Engagement Date",
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    risk_assesment_date = fields.Date(
        string="Risk Assesment Date",
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
    pe_ra_manhour_allocation = fields.Float(
        string="PE & RA Manhour Allocation",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    rr_manhour_allocation = fields.Float(
        string="RR Manhour Allocation",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    reporting_manhour_allocation = fields.Float(
        string="Reporting Manhour Allocation",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    total_manhour_allocation = fields.Float(
        string="Total Manhour Allocation",
        compute="_compute_total_manhour_allocation",
        store=True,
        compute_sudo=True,
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
    total_ra_manhour = fields.Float(
        string="Total Risk Assesment Allocation",
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
        string="Total Respoting Allocation",
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

    @api.depends(
        "team_allocation_ids",
        "team_allocation_ids.ra_allocation",
        "team_allocation_ids.rr_allocation",
        "team_allocation_ids.reporting_allocation",
    )
    def _compute_total_manhour(self):
        for record in self:
            ra = rr = reporting = 0.0
            for allocation in record.team_allocation_ids:
                ra += allocation.ra_allocation
                rr += allocation.rr_allocation
                reporting += allocation.reporting_allocation
            record.total_ra_manhour = ra
            record.total_rr_manhour = rr
            record.total_reporting_manhour = reporting

    @api.depends(
        "pe_ra_manhour_allocation",
        "rr_manhour_allocation",
        "reporting_manhour_allocation",
    )
    def _compute_total_manhour_allocation(self):
        for record in self:
            result = (
                record.pe_ra_manhour_allocation
                + record.rr_manhour_allocation
                + record.reporting_manhour_allocation
            )
            record.total_manhour_allocation = result
