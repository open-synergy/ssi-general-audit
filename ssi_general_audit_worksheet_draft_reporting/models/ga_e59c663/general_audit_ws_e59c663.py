# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSe59c663(models.Model):
    """Worksheet — Draft Financial Statements (e59c663).

    Used to review the client's draft financial statements prior to issuing
    the audit opinion.  The auditor confirms the statements are in accordance
    with the applicable financial reporting framework (IFRS, PSAK, etc.) and
    that all audit adjustments have been properly reflected.  It also holds
    a completeness checklist of the financial statement components that must
    be present (cover page, the four primary statements, and the Notes to
    the Financial Statements breakdown -- ``checklist_ids``), populated from
    the ``general_audit_ws_e59c663.item`` master.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 700/SA 700 (Forming an Opinion);
    ISA 450/SA 450 (Evaluation of Misstatements).
    """

    _name = "general_audit_ws_e59c663"
    _description = "Draft Financial Statements (e59c663)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_draft_reporting." "worksheet_type_e59c663"
    )
    _checklist_model_name = "general_audit_ws_e59c663.checklist"
    _item_model_name = "general_audit_ws_e59c663.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_e59c663.checklist",
        help="Checklist lines for this worksheet.",
    )
