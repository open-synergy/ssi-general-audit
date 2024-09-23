# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSA604795BusinessFunction(models.Model):
    _name = "general_audit_ws_a604795.business_function"
    _description = "Worksheet a604795 - Business Function"
    _order = "worksheet_id, id"

    detail_id = fields.Many2one(
        string="Detail",
        comodel_name="general_audit_ws_a604795.detail",
        required=True,
        ondelete="cascade",
    )
    worksheet_id = fields.Many2one(
        related="detail_id.worksheet_id",
        store=True,
    )
    business_function_id = fields.Many2one(
        string="Business Functions",
        comodel_name="general_audit_business_function",
        required=True,
    )
    business_document_ids = fields.Many2many(
        string="Business Documents",
        comodel_name="general_audit_business_document",
        relation="rel_general_audit_ws_a604795_function_2_document",
        column1="detail_id",
        column2="business_document_id",
    )
