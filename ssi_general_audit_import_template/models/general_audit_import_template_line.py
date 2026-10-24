# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditImportTemplateLine(models.Model):
    """Column definition of a General Audit import template.

    One line is one column of the CSV file produced by the parent
    template: its title goes to the header row and its example value
    goes to the example row.
    """

    _name = "general_audit_import_template.line"
    _description = "General Audit Import Template Column"
    _order = "template_id, sequence"

    template_id = fields.Many2one(
        string="# Template",
        comodel_name="general_audit_import_template",
        required=True,
        ondelete="cascade",
        help="Import template that owns this column.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Position of the column in the CSV file, lowest first.",
    )
    name = fields.Char(
        string="Column Title",
        required=True,
        help="Title of the column, written to the header row of the CSV.",
    )
    example_value = fields.Char(
        string="Example Value",
        help="Sample value written to the example row under this column.",
    )
    note = fields.Char(
        string="Note",
        help="Free remark about the expected content of this column.",
    )
