# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS369c5a5(models.Model):
    _name = "general_audit_ws_369c5a5"
    _description = "Previous Financial Reporting Issues (369c5a5)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_369c5a5"
    )
    _checklist_model_name = "general_audit_ws_369c5a5.checklist"
    _item_model_name = "general_audit_ws_369c5a5.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_369c5a5.checklist",
    )
