# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc94e287(models.Model):
    _name = "general_audit_ws_c94e287"
    _description = "Communication With TCWG (c94e287)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_external_communication." "worksheet_type_c94e287"
    )
    _checklist_model_name = "general_audit_ws_c94e287.checklist"
    _item_model_name = "general_audit_ws_c94e287.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_c94e287.checklist",
        help="All checklist line records associated with this worksheet.",
    )
