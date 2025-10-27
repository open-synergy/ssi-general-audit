# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb3ff42fItem(models.Model):
    _name = "general_audit_ws_b3ff42f.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Communication With Management (b3ff42f) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="Short code or identifier for the checklist item. Defaults to '/'.",
    )
    communication_type = fields.Selection(
        string="Type of Communication",
        selection=[
            (
                "understanding",
                "Mutual Understanding of a Supportive Working Relationship",
            ),
            (
                "audit_info",
                "Relevant Audit Plan Information Communicated to Management",
            ),
            ("expected_info", "Information Expected to Be Obtained from Management"),
            ("significant_findings", "Significant Findings"),
        ],
        required=True,
        help=(
            "Classifies the item by the nature of communication with management. "
            "Use to group items and support reporting and filtering."
        ),
    )
