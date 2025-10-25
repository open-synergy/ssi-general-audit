# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbe62e79(models.Model):
    _name = "general_audit_ws_be62e79"
    _description = "Financial Statement Disclosure Review (be62e79)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_review." "worksheet_type_be62e79"
    _checklist_model_name = "general_audit_ws_be62e79.checklist"
    _item_model_name = "general_audit_ws_be62e79.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_be62e79.checklist",
        help="Checklist lines for this worksheet.",
    )
