# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa753ab9(models.Model):
    """
    WS: Audit Planning Memorandum — Checklist (a753ab9) — ISA 300 / SA 300.

    A structured Yes / No / N-A checklist that evaluates whether the auditor
    has adequately addressed all five planning areas prescribed by ISA 300:

    1. **Characteristics of the Engagement** — nature, timing, and reporting
       framework; sector-specific requirements.
    2. **Reporting Objectives** — deadlines, nature of communications expected.
    3. **Important Factors** — materiality, preliminary risk assessments,
       areas requiring special attention.
    4. **Significant Changes and Developments** — changes in the client's
       business or internal control environment since the prior audit.
    5. **Nature, Timing, and Extent of Resources Required** — team
       composition, specialist involvement, timing of interim vs. final work.

    The ``related_field`` attribute on each checkslit item allows the detail
    summary worksheet (``general_audit_ws_fbbe0f8``) to pull field values
    automatically and display dynamic labels in its form view.
    """

    _name = "general_audit_ws_a753ab9"
    _description = "Audit Planning Memorandum (a753ab9)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_planning_memorandum." "worksheet_type_a753ab9"
    )
    _checklist_model_name = "general_audit_ws_a753ab9.checklist"
    _item_model_name = "general_audit_ws_a753ab9.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_a753ab9.checklist",
    )
