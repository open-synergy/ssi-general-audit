# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSee819ae(models.Model):
    _name = "general_audit_ws_ee819ae"
    _description = "Commitment and Contingent (ee819ae)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_specific_procedure." "worksheet_type_ee819ae"
    )
    _checklist_model_name = "general_audit_ws_ee819ae.checklist"
    _item_model_name = "general_audit_ws_ee819ae.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_ee819ae.checklist",
    )
