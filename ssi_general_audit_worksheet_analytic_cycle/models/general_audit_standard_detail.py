# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import fields, models


class GeneralAuditStandardDetail(models.Model):
    """
    General Audit Standard Detail — Analytical Procedures – Cycle Extension

    Extends ``general_audit.standard_detail`` with the result of the
    Analytical Procedures – Cycle worksheet (a3c9d2e) category that covers
    this standard account (``related_account_type_ids`` tagged on the
    category). Written back by
    ``general_audit_ws_a3c9d2e.checklist._inverse_to_standard_detail`` so
    that the assessed cycle result is available to downstream processes
    (risk assessment, confidence factor).

    **SA reference:** SA 520 — Prosedur Analitis
    """

    _name = "general_audit.standard_detail"
    _inherit = ["general_audit.standard_detail"]

    analytical_procedures_cycle_result = fields.Selection(
        string="Analytical Procedures – Cycle Result",
        selection=[
            ("high", "High"),
            ("moderate", "Moderate"),
        ],
        help=(
            "Result of the Analytical Procedures – Cycle category covering "
            "this standard detail."
        ),
    )
