# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSfc75636Item(models.Model):
    _name = "general_audit_ws_fc75636.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Independen Auditor Report (fc75636) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="Item code or number. Use '/' to auto-generate the code.",
    )
    checklist_type = fields.Selection(
        string="Type of Checklist",
        selection=[
            ("unmodified", "Unmodified Opinion"),
            ("modified", "Modified Auditor’s Report"),
            ("emphasis_other", "Emphasis of Matter and Other Matter"),
        ],
        required=True,
        help="Defines the category of checklist where this item is used.",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_ws_fc75636.category",
    )
