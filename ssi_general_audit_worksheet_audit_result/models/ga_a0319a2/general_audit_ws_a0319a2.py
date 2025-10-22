# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSa0319a2(models.Model):
    _name = "general_audit_ws_a0319a2"
    _description = "Findings That Influence Opinion (a0319a2)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_audit_result." "worksheet_type_a0319a2"

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_a0319a2.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
    )
