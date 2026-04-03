# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbfb6daeChecklist(models.Model):
    """
    Inherent Risk Assessment Checklist — Checklist Line (bfb6dae)

    A single assessed checklist item within the Inherent Risk Assessment
    Checklist worksheet (WS.060.1).  Each line captures the auditor's
    Yes / No / N-A response for one specific risk indicator.

    Child of ``general_audit_ws_bfb6dae``.  Cascades on parent delete.
    """

    _name = "general_audit_ws_bfb6dae.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Inherent Risk (bfb6dae) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_bfb6dae",
        required=True,
        ondelete="cascade",
        help="Parent Inherent Risk worksheet for this checklist line.",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_bfb6dae.item",
        required=True,
        help="Checklist item/question being evaluated on this line.",
    )
