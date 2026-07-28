# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSb9d8a5c(models.Model):
    """Worksheet: Competency, Availability, and Independency of Assignment Team.

    Assesses whether the proposed audit engagement team collectively meets the
    quality control requirements mandated by SA 220 (Quality Control for an
    Audit of Financial Statements) and ISQC 1 across three dimensions:

    - **Competency** (``competency_analysis_ids``): Each team member has
      the professional knowledge and technical skills required for the
      engagement.
    - **Availability** (``availability_analysis_ids``): Each team member has
      sufficient scheduled time without conflicts or constraints.
    - **Independency** (``independency_analysis_ids``): Each team member is
      independent from the client and free from conflicts of interest.

    Workflow:
    1. Populate the candidate personnel list (``action_populate_personnel``).
    2. Generate the analysis sub-records and summary
       (``action_create_summary``).
    3. Review each analysis dimension and set the overall risk level
       (Low / Medium / High).

    The ``summary_ids`` field provides a consolidated per-person view of
    all three assessment results.

    Model: ``general_audit_ws_b9d8a5c``
    SA Reference: SA 220, ISQC 1
    Module: ``ssi_general_audit_worksheet_acceptance_continuance``
    """

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
        """Generate/re-sync the competency, availability, independency and
        summary lines from the currently proposed personnel.

        Safe to call repeatedly: it is both idempotent (re-running does not
        add extra lines for personnel that already have one) and
        self-healing (any pre-existing duplicate line for the same
        ``employee_id`` on this worksheet is cleaned up, keeping the line
        with the smallest ``id``).

        :return: None
        """
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

    def _sync_team_lines(self, line_field, comodel_name):
        """Synchronise a team analysis/summary O2M with proposed personnel.

        Shared by ``_create_competency_team``, ``_create_availability_team``,
        ``_create_independency_team`` and ``_create_summary`` so the
        de-duplication logic is written once.

        Builds the set of currently *proposed* (``proposed == "yes"``)
        personnel, de-duplicated by ``employee_id`` (a single employee is
        never processed twice even if ``personnel_ids`` itself contains a
        duplicate). For each proposed employee without an existing line, a
        new line is created and the in-memory mapping is updated
        immediately, so the newly created line is visible to the rest of
        this same loop iteration and a second create for the same employee
        can never happen within one run.

        Any line whose ``employee_id`` is no longer proposed is removed.
        Any *excess* line for an ``employee_id`` that already has a line
        (i.e. pre-existing duplicates left over from before this fix) is
        also removed, keeping only the line with the smallest ``id`` — this
        is what allows re-running ``action_create_summary`` to self-heal
        worksheets that already accumulated duplicate rows.

        :param str line_field: field name on this worksheet holding the
            O2M to the analysis/summary model (e.g.
            ``competency_analysis_ids``).
        :param str comodel_name: technical model name of the
            analysis/summary model (e.g.
            ``general_audit_ws_b9d8a5c.competency``).
        :return: None
        """
        self.ensure_one()
        Model = self.env[comodel_name]
        personnels = self.personnel_ids.filtered(lambda x: x.proposed == "yes")
        proposed_emp_ids = set(personnels.mapped("employee_id").ids)

        # Keep only the oldest (smallest id) line per employee_id; queue any
        # extra existing duplicate for removal.
        mapping = {}
        to_unlink = Model.browse()
        for line in self[line_field].sorted("id"):
            emp_id = line.employee_id.id
            if emp_id in mapping:
                to_unlink |= line
            else:
                mapping[emp_id] = line

        # Create missing lines, updating `mapping` inside the loop so a
        # duplicated employee_id in `personnels` cannot create a second line.
        seen_emp_ids = set()
        for personnel in personnels:
            emp_id = personnel.employee_id.id
            if emp_id in seen_emp_ids:
                continue
            seen_emp_ids.add(emp_id)
            if emp_id not in mapping:
                mapping[emp_id] = Model.create(self._prepare_team_data(personnel))

        # Lines whose employee is no longer proposed are stale, remove them.
        for emp_id, line in mapping.items():
            if emp_id not in proposed_emp_ids:
                to_unlink |= line

        if to_unlink:
            to_unlink.unlink()

    def _create_competency_team(self):
        """Sync ``competency_analysis_ids`` with the proposed personnel.

        Delegates to ``_sync_team_lines`` — see its docstring for the
        create/de-duplicate/cleanup contract.

        :return: None
        """
        self.ensure_one()
        self._sync_team_lines(
            "competency_analysis_ids", "general_audit_ws_b9d8a5c.competency"
        )

    def _create_availability_team(self):
        """Sync ``availability_analysis_ids`` with the proposed personnel.

        Delegates to ``_sync_team_lines`` — see its docstring for the
        create/de-duplicate/cleanup contract.

        :return: None
        """
        self.ensure_one()
        self._sync_team_lines(
            "availability_analysis_ids", "general_audit_ws_b9d8a5c.availability"
        )

    def _create_independency_team(self):
        """Sync ``independency_analysis_ids`` with the proposed personnel.

        Delegates to ``_sync_team_lines`` — see its docstring for the
        create/de-duplicate/cleanup contract.

        :return: None
        """
        self.ensure_one()
        self._sync_team_lines(
            "independency_analysis_ids", "general_audit_ws_b9d8a5c.independency"
        )

    def _create_summary(self):
        """Sync ``summary_ids`` with the proposed personnel.

        Delegates to ``_sync_team_lines`` — see its docstring for the
        create/de-duplicate/cleanup contract.

        :return: None
        """
        self.ensure_one()
        self._sync_team_lines("summary_ids", "general_audit_ws_b9d8a5c.summary")
