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
        help=(
            "Reference to the parent a604795 detail line that this business function "
            "belongs to. When the detail record is deleted, this business function "
            "record will be automatically removed due to cascade deletion policy."
        ),
    )
    worksheet_id = fields.Many2one(
        related="detail_id.worksheet_id",
        store=True,
        help=(
            "Reference to the parent worksheet (a604795) automatically derived from "
            "the associated detail record. This field is stored in the database to "
            "improve performance when filtering and generating reports based on worksheet."
        ),
    )
    business_function_id = fields.Many2one(
        string="Business Functions",
        comodel_name="general_audit_business_function",
        required=True,
        ondelete="restrict",
        help=(
            "Specific business function that is relevant to and supports the selected "
            "class of transaction. This defines the operational activities and processes "
            "that drive the transaction class within the client's business cycle."
        ),
    )
    business_document_ids = fields.Many2many(
        string="Business Documents",
        comodel_name="general_audit_business_document",
        relation="rel_general_audit_ws_a604795_function_2_document",
        column1="detail_id",
        column2="business_document_id",
        help=(
            "Collection of business documents that are either used as input, "
            "generated as output, or otherwise supporting this business function. "
            "These documents serve as audit evidence and help understand the "
            "documentation flow within the business process."
        ),
    )
