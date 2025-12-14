# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSe51bb1c(models.Model):
    _name = "general_audit_ws_e51bb1c"
    _description = "Key Audit Procedures (e51bb1c)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_lead_schedule." "worksheet_type_e51bb1c"

    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Standard Account",
        required=False,
        states={
            "open": [("readonly", False)],
        },
        readonly=True,
        ondelete="restrict",
    )

    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_account_type_ids(self):
        for record in self:
            record.allowed_account_type_ids = self.env["client_account_type"]
            if record.general_audit_id:
                record.allowed_account_type_ids = record.general_audit_id.mapped(
                    "standard_detail_ids.type_id"
                )

    allowed_account_type_ids = fields.Many2many(
        comodel_name="client_account_type",
        string="Allowed Account Types",
        help="Account types that can be selected",
        compute="_compute_allowed_account_type_ids",
        store=False,
    )

    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_employee_ids(self):
        obj = self.env["general_audit_ws_b9d8a5c"]
        for record in self:
            result = False
            record.allowed_employee_ids = self.env["hr.employee"]
            if record.general_audit_id:
                criteria = [
                    ("general_audit_id", "=", record.general_audit_id.id),
                ]
                ws_b9d8a5c = obj.search(criteria)
                if ws_b9d8a5c:
                    summaries = ws_b9d8a5c.summary_ids.filtered(
                        lambda x: x.select_team == "yes"
                    )
                    if summaries:
                        result = summaries.mapped("employee_id")
                record.allowed_employee_ids = result

    allowed_employee_ids = fields.Many2many(
        string="Allowed Employees",
        comodel_name="hr.employee",
        compute="_compute_allowed_employee_ids",
        store=False,
    )
    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_e51bb1c.detail",
        inverse_name="worksheet_id",
        string="Details",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
    )

    def action_load_detail(self):
        for record in self.sudo():
            record.detail_ids.unlink()
            record._load_detail()

    def _load_detail(self):
        self.ensure_one()
        Detail = self.env["general_audit_ws_e51bb1c.detail"]
        Procedure = self.env["general_audit_audit_procedure_category"]

        if not self.account_type_id:
            return True

        procedure_domain = [
            ("account_type_id", "=", self.account_type_id.id),
        ]
        procedure_ids = Procedure.search(procedure_domain)
        mapping = {chk.audit_procedure_category_id.id: chk for chk in self.detail_ids}

        if procedure_ids:
            for procedure in procedure_ids:
                expected_assertions = procedure.assertion_type_ids.ids
                steps = procedure.step_ids
                if procedure.id not in mapping:
                    Detail.create(
                        {
                            "worksheet_id": self.id,
                            "audit_procedure_category_id": procedure.id,
                            "assertion_type_ids": [
                                (6, 0, procedure.assertion_type_ids.ids)
                            ],
                            "step_ids": [(6, 0, steps.ids)],
                        }
                    )
                else:
                    detail = mapping[procedure.id]
                    current_assertions = detail.assertion_type_ids.ids
                    if set(current_assertions) != set(expected_assertions):
                        detail.write(
                            {
                                "assertion_type_ids": [(6, 0, expected_assertions)],
                                "step_ids": [(6, 0, steps.ids)],
                            }
                        )
                    if detail.audit_procedure_category_id.id != procedure.id:
                        detail.write({"audit_procedure_category_id": procedure.id})

            for chk in self.detail_ids:
                if chk.audit_procedure_category_id.id not in procedure_ids.ids:
                    chk.unlink()
