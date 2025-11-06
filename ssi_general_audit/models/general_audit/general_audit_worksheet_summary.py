# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


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
    )
