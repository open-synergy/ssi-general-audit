# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc2375d8Item(models.Model):
    """
    Final Analytical Procedures Checklist — Checklist Item Master (c2375d8)

    Master-data model for the checklist items used in the Final Analytical
    Procedures Checklist worksheet (WS.080.2).  Each item carries an
    ``analysis_type`` selection (vertical_horizontal or ratio) that
    classifies the procedure and enables grouped display on the worksheet.
    """

    _name = "general_audit_ws_c2375d8.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Final Analytical Procedures (c2375d8) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="""Internal code for the checklist item.
Defaults to '/'; may be replaced by a generated sequence depending on configuration.""",
    )
    analysis_type = fields.Selection(
        string="Type of Analysis",
        selection=[
            ("vertical_horizontal", "Vertical and Horizontal"),
            ("ratio", "Ratio"),
        ],
        required=True,
        help=(
            "Type of analytical procedure the item refers to "
            "(e.g., vertical/horizontal or ratio analysis)."
        ),
    )
