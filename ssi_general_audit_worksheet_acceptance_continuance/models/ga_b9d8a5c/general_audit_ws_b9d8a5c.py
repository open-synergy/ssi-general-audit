# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSb9d8a5c(models.Model):
    _name = "general_audit_ws_b9d8a5c"
    _description = (
        "Competency, Availability and Independency " "Of Assignment Team (b9d8a5c)"
    )
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_b9d8a5c"
    )

    risk = fields.Selection(
        string="Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
    )
    personnel_ids = fields.One2many(
        string="List of Personnel",
        comodel_name="general_audit_ws_b9d8a5c.personnel",
        inverse_name="worksheet_id",
    )
    competency_analysis_ids = fields.One2many(
        string="Competency Analysis",
        comodel_name="general_audit_ws_b9d8a5c.competency",
        inverse_name="worksheet_id",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    availability_analysis_ids = fields.One2many(
        string="Availability Analysis",
        comodel_name="general_audit_ws_b9d8a5c.availability",
        inverse_name="worksheet_id",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    independency_analysis_ids = fields.One2many(
        string="Independency Analysis",
        comodel_name="general_audit_ws_b9d8a5c.independency",
        inverse_name="worksheet_id",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    summary_ids = fields.One2many(
        string="Summary",
        comodel_name="general_audit_ws_b9d8a5c.summary",
        inverse_name="worksheet_id",
        readonly=True,
        states={"open": [("readonly", False)]},
    )

    def action_populate_personnel(self):
        """Generic method untuk populate personnel dari employee"""
        for record in self.sudo():
            record._populate_personnel()

    def action_create_summary(self):
        for record in self.sudo():
            record._create_competency_team()
            record._create_availability_team()
            record._create_independency_team()
            record._create_summary()

    def _populate_personnel(self):
        self.ensure_one()
        Employee = self.env["hr.employee"]
        Personnel = self.env["general_audit_ws_b9d8a5c.personnel"]
        emps = Employee.search(
            [
                ("audit_ok", "=", True),
            ]
        )

        # mapping existing personnel by employee_id
        emp_map = {chk.employee_id.id: chk for chk in self.personnel_ids}

        # 1. Tambah / update
        for emp in emps:
            if emp.id not in emp_map:
                Personnel.create(
                    {
                        "worksheet_id": self.id,
                        "employee_id": emp.id,
                        "job_id": emp.job_id.id,
                    }
                )

        # 2. Hapus yang sudah tidak ada di master
        emp_ids = set(emps.ids)
        for chk in self.personnel_ids:
            if chk.employee_id.id not in emp_ids:
                chk.unlink()

    def _prepare_team_data(self, personnel):
        self.ensure_one()
        data = {
            "worksheet_id": self.id,
            "employee_id": personnel.employee_id.id,
            "sequence": personnel.sequence,
        }
        return data

    def _create_competency_team(self):
        self.ensure_one()
        Competency = self.env["general_audit_ws_b9d8a5c.competency"]
        personnels = self.personnel_ids.filtered(lambda x: x.proposed == "yes")
        emps = self.personnel_ids.filtered(lambda x: x.proposed == "yes").mapped(
            "employee_id"
        )
        mapping = {chk.employee_id.id: chk for chk in self.competency_analysis_ids}
        for personnel in personnels:
            if personnel.employee_id.id not in mapping:
                Competency.create(self._prepare_team_data(personnel))
        emp_ids = set(emps.ids)
        for chk in self.competency_analysis_ids:
            if chk.employee_id.id not in emp_ids:
                chk.unlink()

    def _create_availability_team(self):
        self.ensure_one()
        Availability = self.env["general_audit_ws_b9d8a5c.availability"]
        personnels = self.personnel_ids.filtered(lambda x: x.proposed == "yes")
        emps = self.personnel_ids.filtered(lambda x: x.proposed == "yes").mapped(
            "employee_id"
        )
        mapping = {chk.employee_id.id: chk for chk in self.availability_analysis_ids}
        for personnel in personnels:
            if personnel.employee_id.id not in mapping:
                Availability.create(self._prepare_team_data(personnel))
        emp_ids = set(emps.ids)
        for chk in self.availability_analysis_ids:
            if chk.employee_id.id not in emp_ids:
                chk.unlink()

    def _create_independency_team(self):
        self.ensure_one()
        Independency = self.env["general_audit_ws_b9d8a5c.independency"]
        personnels = self.personnel_ids.filtered(lambda x: x.proposed == "yes")
        emps = self.personnel_ids.filtered(lambda x: x.proposed == "yes").mapped(
            "employee_id"
        )
        mapping = {chk.employee_id.id: chk for chk in self.independency_analysis_ids}
        for personnel in personnels:
            if personnel.employee_id.id not in mapping:
                Independency.create(self._prepare_team_data(personnel))
        emp_ids = set(emps.ids)
        for chk in self.independency_analysis_ids:
            if chk.employee_id.id not in emp_ids:
                chk.unlink()

    def _create_summary(self):
        self.ensure_one()
        Summary = self.env["general_audit_ws_b9d8a5c.summary"]
        personnels = self.personnel_ids.filtered(lambda x: x.proposed == "yes")
        emps = self.personnel_ids.filtered(lambda x: x.proposed == "yes").mapped(
            "employee_id"
        )
        mapping = {chk.employee_id.id: chk for chk in self.summary_ids}
        for personnel in personnels:
            if personnel.employee_id.id not in mapping:
                Summary.create(self._prepare_team_data(personnel))
        emp_ids = set(emps.ids)
        for chk in self.summary_ids:
            if chk.employee_id.id not in emp_ids:
                chk.unlink()
