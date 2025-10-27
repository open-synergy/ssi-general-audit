# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSae48e68(models.Model):
    _name = "general_audit_ws_ae48e68"
    _description = "External Communication (ae48e68)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_external_communication." "worksheet_type_ae48e68"
    )
    _checklist_model_name = "general_audit_ws_ae48e68.checklist"
    _item_model_name = "general_audit_ws_ae48e68.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_ae48e68.checklist",
        help="All checklist line records associated with this worksheet.",
    )
