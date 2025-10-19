# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSe51bb1cDetail(models.Model):
    _name = "general_audit_ws_e51bb1c.detail"
    _description = "Lead Schedule - Key Audit Procedures (e51bb1c) - Detail"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_e51bb1c",
        string="# Worksheet",
        required=True,
        ondelete="cascade",
    )
    audit_procedure_id = fields.Many2one(
        comodel_name="general_audit_audit_procedure",
        string="Audit Procedure",
        required=True,
        ondelete="restrict",
    )
    audit_procedure_category_id = fields.Many2one(
        comodel_name="general_audit_audit_procedure_category",
        string="Category",
        related="audit_procedure_id.category_id",
        store=True,
    )
    assertion_type_ids = fields.Many2many(
        comodel_name="general_audit_assersion_type",
        string="Assertions",
        required=False,
        relation="rel_ws_e51bb1c_detail_2_assertion_type",
        column1="detail_id",
        column2="assertion_type_id",
    )
    status = fields.Selection(
        selection=[
            ("performed", "Performed"),
            ("not_performed", "Not Performed"),
            ("not_relevant", "Not Relevant"),
        ],
        string="Status",
        required=True,
        default="not_relevant",
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Assigned To",
        required=False,
    )
    reference = fields.Char(
        string="Reference",
        required=False,
    )
