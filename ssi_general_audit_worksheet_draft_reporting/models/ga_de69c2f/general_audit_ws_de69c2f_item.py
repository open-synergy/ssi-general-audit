# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSde69c2fItem(models.Model):
    _name = "general_audit_ws_de69c2f.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Final Discussion (de69c2f) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="Item code or number. Use '/' to auto-generate the code.",
    )
    checklist_type = fields.Selection(
        string="Type of Checklist",
        selection=[
            ("audit_result", "Audit Result"),
            ("mgmt_letter", "Management Letter"),
            ("mgmt_representation", "Management Representation"),
        ],
        required=True,
        help="Defines the category of checklist where this item is used.",
    )
