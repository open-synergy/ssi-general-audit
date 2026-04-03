# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWScda3a68Detail(models.Model):
    """
    Management's Expert Worksheet — Evaluation Detail Line (cda3a68)

    One evaluation line within the Management's Expert worksheet
    (WS.040.2).  Each line covers a specific evaluation factor and
    allows the auditor to record an explanation or reference supporting
    the assessment of that factor for the management-engaged expert.

    Child of ``general_audit_ws_cda3a68``.  Cascades on parent delete.
    """

    _name = "general_audit_ws_cda3a68.detail"
    _inherit = [
        "mixin.expert.detail",
    ]
    _description = "Management Expert (cda3a68) - Details"

    expert_id = fields.Many2one(
        string="# Expert",
        comodel_name="general_audit_ws_cda3a68",
        required=True,
        ondelete="cascade",
    )
    factor_id = fields.Many2one(
        string="Factor",
        comodel_name="general_audit_ws_cda3a68.factor",
        required=True,
    )
