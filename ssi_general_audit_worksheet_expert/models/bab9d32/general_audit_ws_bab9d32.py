# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbab9d32(models.Model):
    _name = "general_audit_ws_bab9d32"
    _description = "Auditor Expert (bab9d32)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.expert",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_expert." "worksheet_type_bab9d32"
    _detail_model_name = "general_audit_ws_bab9d32.detail"
    _factor_model_name = "general_audit_ws_bab9d32.factor"

    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_bab9d32.detail",
        help=(
            "Checklist lines associated with this worksheet "
            "(Previous Financial Reporting Issues)."
        ),
    )
