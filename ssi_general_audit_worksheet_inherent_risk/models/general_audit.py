# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAudit(models.Model):
    _name = "general_audit"
    _description = "General Audit"
    _inherit = [
        "general_audit",
    ]

    significant_risk_account_type_ids = fields.Many2many(
        string="Significant Account Types",
        comodel_name="client_account_type",
        compute="_compute_significant_risk_account_type_ids",
        rel="rel_general_audit_2_significant_risk_account_type",
        column1="general_audit_id",
        column2="account_type_id",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "standard_detail_ids",
        "standard_detail_ids.significant_risk",
    )
    def _compute_significant_risk_account_type_ids(self):
        StandardDetail = self.env["general_audit.standard_detail"]
        for record in self:
            result = []
            criteria = [
                ("general_audit_id", "=", record.id),
                (
                    "significant_risk",
                    "=",
                    True,
                ),
            ]
            details = StandardDetail.search(criteria)
            if len(details) > 0:
                result = details.mapped("type_id.id")
            record.significant_risk_account_type_ids = [(6, 0, result)]
