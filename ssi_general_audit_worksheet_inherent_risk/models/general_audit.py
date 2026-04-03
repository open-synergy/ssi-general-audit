# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAudit(models.Model):
    """
    General Audit — Inherent Risk Extension

    Extends ``general_audit`` with a computed field that aggregates the
    account types identified as having **significant risk** based on the
    inherent risk assessments recorded in the standard detail lines.

    ``significant_risk_account_type_ids`` is recomputed whenever the
    ``significant_risk`` flag is updated on any
    ``general_audit.standard_detail`` line belonging to this engagement.
    The field is consumed by the Financial Statement Level Inherent Risk
    worksheet (WS.060.3) and other downstream modules that need to know
    which account types carry significant risk for this engagement.

    **ISA / SA references:** ISA 315 / SA 315 — Identifying and Assessing
    the Risks of Material Misstatement
    """

    _name = "general_audit"
    _description = "General Audit"
    _inherit = [
        "general_audit",
    ]

    significant_risk_account_type_ids = fields.Many2many(
        string="Significant Account Types",
        comodel_name="client_account_type",
        compute="_compute_significant_risk_account_type_ids",
        relation="rel_general_audit_2_significant_risk_account_type",
        column1="general_audit_id",
        column2="account_type_id",
        store=True,
        compute_sudo=True,
        help="""Account types identified as having significant risk based on standard details.
Computed and stored; updates automatically when significant risk flags change.""",
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
