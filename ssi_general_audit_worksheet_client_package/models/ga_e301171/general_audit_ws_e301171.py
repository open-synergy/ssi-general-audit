# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSe301171(models.Model):
    """Worksheet — Journal Entry Testing (e301171).

    A checklist-based worksheet for documenting the auditor's procedures over
    journal entries, addressing the risk of management override of controls
    as required by ISA 240 / SA 240.

    Journal entry testing verifies that all journal entries (including manual
    and non-standard entries) are authorised, supported, and recorded
    correctly.  The worksheet guides the auditor through a structured list of
    testing steps and documents whether each step was performed and the result.

    ISA/SA references: ISA 240/SA 240 (Fraud in an Audit);
    ISA 500/SA 500 (Audit Evidence).
    """

    _name = "general_audit_ws_e301171"
    _description = "Journal Entry Testing (e301171)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_client_package." "worksheet_type_e301171"
    )
    _checklist_model_name = "general_audit_ws_e301171.checklist"
    _item_model_name = "general_audit_ws_e301171.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_e301171.checklist",
        help="List of checklist values recorded for this worksheet.",
    )
