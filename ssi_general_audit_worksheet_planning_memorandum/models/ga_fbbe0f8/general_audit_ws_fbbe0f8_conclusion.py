# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSfbbe0f8Conclusion(models.Model):
    """Conclusion summary of one worksheet type in the planning memorandum.

    One line per worksheet type listed in ``conclusion_source_type_ids`` of
    the memorandum worksheet type. Lines are created by Reload Links only.
    The summary follows the worksheet when exactly one exists and is typed
    by the user when several exist.
    """

    _name = "general_audit_ws_fbbe0f8.conclusion"
    _description = "Audit Planning Memorandum - Detail Conclusion (fbbe0f8)"
    _inherit = [
        "general_audit_conclusion_line_mixin",
    ]

    worksheet_id = fields.Many2one(
        string="# Audit Planning Memorandum - Detail",
        comodel_name="general_audit_ws_fbbe0f8",
        required=True,
        ondelete="cascade",
        help="Audit Planning Memorandum - Detail that owns this line.",
    )
