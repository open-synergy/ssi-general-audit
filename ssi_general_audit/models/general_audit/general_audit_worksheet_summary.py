# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWorksheetSummary(models.Model):
    _name = "general_audit.worksheet_summary"
    _description = "General Audit - Worksheet"
    _auto = True
    _order = "general_audit_id, category_id, type_id"

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        ondelete="cascade",
        help="Audit referencing this control entry.",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="general_audit_worksheet_type",
        required=False,
        ondelete="restrict",
        help="Worksheet type being controlled (required/additional).",
    )
    category_id = fields.Many2one(
        related="type_id.category_id",
        string="Category",
        compute_sudo=True,
        store=True,
    )
    is_required = fields.Boolean(
        string="Required",
        help="True if this worksheet type is mandatory for the audit.",
    )
    max_worksheet = fields.Integer(
        string="Max Worksheet",
        help="Maximum number of worksheets allowed for this type.",
    )
    image_128 = fields.Image(
        related="type_id.image_128",
        string="Type Image",
        compute_sudo=True,
    )
    num_of_worksheet = fields.Integer(
        string="Number of Worksheets",
        compute="_compute_num_of_worksheet",
        store=True,
        compute_sudo=True,
        help="Number of worksheets created for this type.",
    )
    num_of_finish_worksheet = fields.Integer(
        string="Number of Finished Worksheets",
        compute="_compute_num_of_worksheet",
        store=True,
        compute_sudo=True,
        help="Number of finished worksheets for this type.",
    )
    finish = fields.Boolean(
        string="Finished",
        compute="_compute_num_of_worksheet",
        store=True,
        compute_sudo=True,
        help="True if all required worksheets of this type are finished.",
    )
    worksheet_ids = fields.Many2many(
        string="Worksheets",
        comodel_name="general_audit_worksheet",
        compute="_compute_worksheet_ids",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "general_audit_id",
        "type_id",
    )
    def _compute_worksheet_ids(self):
        Worksheet = self.env["general_audit_worksheet"]
        for record in self:
            domain = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("parent_type_id", "=", record.type_id.id),
            ]
            record.worksheet_ids = Worksheet.search(domain).ids

    @api.depends(
        "general_audit_id",
        "type_id",
        "general_audit_id.worksheet_ids",
        "general_audit_id.worksheet_ids.state",
        "general_audit_id.worksheet_ids.parent_type_id",
    )
    def _compute_num_of_worksheet(self):
        Worksheet = self.env["general_audit_worksheet"]
        for record in self:
            record.finish = False
            domain = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("parent_type_id", "=", record.type_id.id),
            ]
            record.num_of_worksheet = Worksheet.search_count(domain)
            domain.append(("state", "=", "done"))
            record.num_of_finish_worksheet = Worksheet.search_count(domain)
            if record.num_of_finish_worksheet > 0:
                record.finish = True

    def action_open_worksheet(self):
        self.ensure_one()
        WindowAction = self.env["ir.actions.act_window"]
        criteria = [
            ("res_model", "=", self.type_id.model_name),
        ]
        action = WindowAction.search(criteria).read()[0]
        action["domain"] = [
            ("general_audit_id", "=", self.general_audit_id.id),
        ]
        return action
