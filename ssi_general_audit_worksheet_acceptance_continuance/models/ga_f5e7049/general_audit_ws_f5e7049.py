# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSf5e7049(models.Model):
    _name = "general_audit_ws_f5e7049"
    _description = "Management Integrity (f5e7049)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_f5e7049"
    )
    _checklist_model_name = "general_audit_ws_f5e7049.checklist"
    _item_model_name = "general_audit_ws_f5e7049.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_f5e7049.checklist",
    )
