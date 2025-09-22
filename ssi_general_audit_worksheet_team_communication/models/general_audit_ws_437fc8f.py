# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS437fc8f(models.Model):
    _name = "general_audit_ws_437fc8f"
    _description = "Assignment Letter (437fc8f)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_team_communication." "worksheet_type_437fc8f"
    )
    _checklist_model_name = "general_audit_ws_437fc8f.checklist"
    _item_model_name = "general_audit_ws_437fc8f.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_437fc8f.checklist",
    )
