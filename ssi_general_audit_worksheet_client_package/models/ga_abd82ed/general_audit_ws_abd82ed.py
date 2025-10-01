# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSabd82ed(models.Model):
    _name = "general_audit_ws_abd82ed"
    _description = "Client Assistance Package (abd82ed)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_client_package." "worksheet_type_abd82ed"
    )
    _checklist_model_name = "general_audit_ws_abd82ed.checklist"
    _item_model_name = "general_audit_ws_abd82ed.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_abd82ed.checklist",
    )
    position = fields.Selection(
        string="Position",
        selection=[
            ("current", "Current"),
            ("interim", "Interim"),
        ],
    )
