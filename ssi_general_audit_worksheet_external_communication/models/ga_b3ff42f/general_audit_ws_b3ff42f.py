# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb3ff42f(models.Model):
    _name = "general_audit_ws_b3ff42f"
    _description = "Communication With Management (b3ff42f)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_external_communication." "worksheet_type_b3ff42f"
    )
    _checklist_model_name = "general_audit_ws_b3ff42f.checklist"
    _item_model_name = "general_audit_ws_b3ff42f.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_b3ff42f.checklist",
        help="All checklist line records associated with this worksheet.",
    )
