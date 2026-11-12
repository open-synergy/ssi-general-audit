# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa8c54f3Conclusion(models.Model):
    """Conclusion summary of one worksheet type in the final memorandum.

    One line per worksheet type listed in ``conclusion_source_type_ids`` of
    the final memorandum worksheet type. Lines are created by Reload Links
    only. The summary follows the worksheet when exactly one exists and is
    typed by the user when several exist.
    """

    _name = "general_audit_ws_a8c54f3.conclusion"
    _description = "Final Audit Memorandum Conclusion (a8c54f3)"
    _inherit = [
        "general_audit_conclusion_line_mixin",
    ]

    worksheet_id = fields.Many2one(
        string="# Final Audit Memorandum",
        comodel_name="general_audit_ws_a8c54f3",
        required=True,
        ondelete="cascade",
        help="Final Audit Memorandum that owns this line.",
    )
