# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSc2375d8(models.Model):
    """
    WS.080.2 — Final Analytical Procedures — Checklist (c2375d8)

    Contains a structured **checklist** for the final analytical
    procedures performed at the end of fieldwork as required by
    ISA 520 / SA 520 (Analytical Procedures).  Near the end of the
    audit the auditor must apply analytical procedures that assist in
    forming an overall conclusion on the financial statements.

    Checklist items are classified by analysis type:

    - *vertical_horizontal* — Balance sheet / income statement
      vertical (common-size) and horizontal (trend) comparisons.
    - *ratio* — Financial ratio analysis (liquidity, profitability,
      leverage, etc.).

    The checklist tracks completion of each analytical procedure,
    supplementing the quantitative worksheets WS.080.3 (Vertical and
    Horizontal Analysis) and WS.080.4 (Ratio Analysis).

    **ISA / SA references:** ISA 520 / SA 520 — Analytical Procedures;
    ISA 315 / SA 315 — Identifying and Assessing the Risks of Material
    Misstatement
    """

    _name = "general_audit_ws_c2375d8"
    _description = "Final Analytical Procedures (c2375d8)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_final_materiality." "worksheet_type_c2375d8"
    )
    _checklist_model_name = "general_audit_ws_c2375d8.checklist"
    _item_model_name = "general_audit_ws_c2375d8.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_c2375d8.checklist",
        help="""Checklist lines linked to this Final Analytical Procedures worksheet.
Each line records the response/assessment for a specific checklist item.""",
    )
