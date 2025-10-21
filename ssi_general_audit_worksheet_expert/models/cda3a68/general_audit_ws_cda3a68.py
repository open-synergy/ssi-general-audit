# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWScda3a68(models.Model):
    _name = "general_audit_ws_cda3a68"
    _description = "Management Expert (cda3a68)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.expert",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_expert." "worksheet_type_cda3a68"
    _detail_model_name = "general_audit_ws_cda3a68.detail"
    _factor_model_name = "general_audit_ws_cda3a68.factor"

    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_cda3a68.detail",
        help=(
            "Checklist lines associated with this worksheet "
            "(Previous Financial Reporting Issues)."
        ),
    )
