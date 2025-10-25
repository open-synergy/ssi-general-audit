# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSdae9f3c(models.Model):
    _name = "general_audit_ws_dae9f3c"
    _description = "Audit Evidence Evaluation (dae9f3c)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_review." "worksheet_type_dae9f3c"
    _checklist_model_name = "general_audit_ws_dae9f3c.checklist"
    _item_model_name = "general_audit_ws_dae9f3c.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_dae9f3c.checklist",
    )
