# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSbfb6dae(models.Model):
    _name = "general_audit_ws_bfb6dae"
    _description = "Inherent Risk (bfb6dae)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_inherent_risk." "worksheet_type_bfb6dae"
    _checklist_model_name = "general_audit_ws_bfb6dae.checklist"
    _item_model_name = "general_audit_ws_bfb6dae.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_bfb6dae.checklist",
    )
