# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa753ab9(models.Model):
    _name = "general_audit_ws_a753ab9"
    _description = "Audit Planning Memorandum (a753ab9)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_planning_memorandum." "worksheet_type_a753ab9"
    )
    _checklist_model_name = "general_audit_ws_a753ab9.checklist"
    _item_model_name = "general_audit_ws_a753ab9.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_a753ab9.checklist",
    )
