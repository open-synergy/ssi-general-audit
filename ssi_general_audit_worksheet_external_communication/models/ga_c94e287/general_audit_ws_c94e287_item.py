# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc94e287Item(models.Model):
    """
    Communication With TCWG — Checklist Item Master (c94e287)

    Master-data model for the checklist items used in the Communication
    With TCWG worksheet (WS.050.3).  Each item carries a
    ``communication_type`` selection that classifies it into one of the
    four ISA 260 / SA 260 TCWG-communication categories:
    understanding, audit info, expected info, or significant findings.
    """

    _name = "general_audit_ws_c94e287.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Communication With TCWG (c94e287) - " "Checklist Item"

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
            ("audit_info", "Relevant Audit Plan Information Communicated to TCGW"),
            ("expected_info", "Information Expected to Be Obtained from TCGW"),
            ("significant_findings", "Significant Findings"),
        ],
        required=True,
        help=(
            "Classifies the item by the nature of communication "
            "with those charged with governance (TCWG). "
            "Use to group items and support reporting and filtering."
        ),
    )
