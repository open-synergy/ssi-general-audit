# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb1f820c(models.Model):
    _name = "general_audit_ws_b1f820c"
    _description = "Team Communication Risk Assessment (b1f820c)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_team_communication." "worksheet_type_b1f820c"
    )
    _checklist_model_name = "general_audit_ws_b1f820c.checklist"
    _item_model_name = "general_audit_ws_b1f820c.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_b1f820c.checklist",
        help=(
            "Collection of checklist items for this worksheet. "
            "Each checklist item represents a specific audit point "
            "that needs to be evaluated and documented."
        ),
    )
