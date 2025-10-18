# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSde417a6(models.Model):
    _name = "general_audit_ws_de417a6"
    _description = "ROMM (de417a6)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_romm." "worksheet_type_de417a6"
    _checklist_model_name = "general_audit_ws_de417a6.checklist"
    _item_model_name = "general_audit_ws_de417a6.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_de417a6.checklist",
        help=(
            "Checklist responses for this worksheet. Each line stores the answer to a "
            "defined checklist item."
        ),
    )
