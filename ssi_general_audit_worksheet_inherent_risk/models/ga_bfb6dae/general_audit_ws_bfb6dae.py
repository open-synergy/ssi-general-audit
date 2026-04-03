# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSbfb6dae(models.Model):
    """
    WS.060.1 — Inherent Risk Assessment Checklist (bfb6dae)

    Provides a structured **inherent risk assessment checklist** as part
    of the auditor's risk assessment procedures required by ISA 315 /
    SA 315 (Identifying and Assessing the Risks of Material Misstatement
    through Understanding the Entity and Its Environment).

    Inherent risk is the susceptibility of an assertion to a misstatement
    that could be material, before considering any related controls.  This
    worksheet presents a configurable set of risk factors that the auditor
    evaluates at the financial-statement level, capturing Yes / No / N-A
    responses for each relevant risk indicator.

    This checklist supplements the quantitative worksheets WS.060.2
    (Account Level Inherent Risk) and WS.060.3 (Financial Statement Level
    Inherent Risk).

    **ISA / SA references:** ISA 315 / SA 315 — Identifying and Assessing
    the Risks of Material Misstatement through Understanding the Entity
    and Its Environment
    """

    _name = "general_audit_ws_bfb6dae"
    _description = "Inherent Risk (bfb6dae)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_inherent_risk." "worksheet_type_bfb6dae"
    _checklist_model_name = "general_audit_ws_bfb6dae.checklist"
    _item_model_name = "general_audit_ws_bfb6dae.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_bfb6dae.checklist",
        help="""Checklist lines associated with this Inherent Risk worksheet.
Each line records the assessment/answer for a specific checklist item.""",
    )
