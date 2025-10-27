# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd133f46Item(models.Model):
    _name = "general_audit_ws_d133f46.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = (
        "Use of Internal Auditor's Work Results (d133f46) " "- Checklist Item"
    )

    code = fields.Char(
        default="/",
        help="Short code or identifier for the checklist item. Defaults to '/'.",
    )
    communication_type = fields.Selection(
        string="Type of Communication",
        selection=[
            ("objectivity", "Objectivity of the Internal Audit Function"),
            ("technical", "Technical Competence"),
            ("professional", "Professional Due Care"),
        ],
        required=True,
        help=(
            "Classifies the item by the evaluation aspect "
            "for using internal auditors' work results. "
            "Use to group items and support reporting and filtering."
        ),
    )
