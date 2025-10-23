# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSde69c2f(models.Model):
    _name = "general_audit_ws_de69c2f"
    _description = "Final Discussion (de69c2f)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_draft_reporting." "worksheet_type_de69c2f"
    )
    _checklist_model_name = "general_audit_ws_de69c2f.checklist"
    _item_model_name = "general_audit_ws_de69c2f.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_de69c2f.checklist",
        help="Checklist lines for this worksheet.",
    )
