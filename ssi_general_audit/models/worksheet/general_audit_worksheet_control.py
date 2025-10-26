# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models, tools


class GeneralAuditWorksheetControl(models.Model):
    _name = "general_audit.worksheet_control"
    _description = "Accountant General Audit Worksheet Control"
    _auto = False
    _order = "general_audit_id, type_id"

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

    def _compute_worksheet_id(self):
        for record in self:
            result = False
            worksheets = record.general_audit_id.worksheet_ids.filtered(
                lambda r: r.parent_type_id.id == record.type_id.id
            )
            if len(worksheets) > 0:
                result = worksheets[0]
            record.worksheet_id = result

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_worksheet",
        compute="_compute_worksheet_id",
        store=False,
        help="Linked worksheet record for this audit and type, if any.",
    )
    required = fields.Boolean(
        string="Required",
        help="True if this worksheet type is mandatory for the audit.",
    )
    user_id = fields.Many2one(
        string="Responsible",
        related="worksheet_id.user_id",
        help="Employee responsible for preparing the worksheet.",
    )
    conclusion_id = fields.Many2one(
        string="Conclusion",
        related="worksheet_id.conclusion_id",
        help="Conclusion selected on the worksheet.",
    )
    state = fields.Selection(
        string="State",
        related="worksheet_id.state",
        help="Current workflow state of the worksheet.",
    )

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        self._cr.execute(
            """CREATE or REPLACE VIEW %s as (
            SELECT
                row_number() OVER() as id,
                a.general_audit_id,
                a.type_id,
                a.required
            FROM (
            SELECT general_audit_id, type_id, required
            FROM general_audit_worksheet_control_required
            UNION
            SELECT general_audit_id, type_id, required
            FROM general_audit_worksheet_control_additional
            ) AS a
        )"""
            % (self._table,)
        )
