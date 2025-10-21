# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbab9d32Detail(models.Model):
    _name = "general_audit_ws_bab9d32.detail"
    _inherit = [
        "mixin.expert.detail",
    ]
    _description = "Auditor Expert (bab9d32) - Details"

    expert_id = fields.Many2one(
        string="# Expert",
        comodel_name="general_audit_ws_bab9d32",
        required=True,
        ondelete="cascade",
    )
    factor_id = fields.Many2one(
        string="Factor",
        comodel_name="general_audit_ws_bab9d32.factor",
        required=True,
    )
