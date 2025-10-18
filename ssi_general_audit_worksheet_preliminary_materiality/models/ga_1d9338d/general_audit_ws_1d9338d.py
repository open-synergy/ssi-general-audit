# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS1d9338d(models.Model):
    _name = "general_audit_ws_1d9338d"
    _description = "Preliminary Materiality (1d9338d)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_preliminary_materiality." "worksheet_type_1d9338d"
    )
    _checklist_model_name = "general_audit_ws_1d9338d.checklist"
    _item_model_name = "general_audit_ws_1d9338d.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_1d9338d.checklist",
        help="Checklist lines associated with this worksheet.",
    )
