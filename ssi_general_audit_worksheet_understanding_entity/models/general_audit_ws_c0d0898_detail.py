# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc0d0898ODetail(models.Model):
    _name = "general_audit_ws_c0d0898.detail"
    _description = "Worksheet c0d0898 - Detail"
    _order = "worksheet_id, going_concern_category_id, going_concern_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_c0d0898",
        required=True,
        ondelete="cascade",
    )
    going_concern_id = fields.Many2one(
        string="Going Concern",
        comodel_name="general_audit_going_concern",
        required=True,
    )
    going_concern_category_id = fields.Many2one(
        string="Going Concern Category",
        related="going_concern_id.category_id",
        store=True,
    )
    going_concern_exist = fields.Boolean(
        string="Going Concern Exist",
        default=False,
    )
    consideration = fields.Text(
        string="Impact To Financial Report",
        required=False,
    )
