# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSabd82ed(models.Model):
    """Worksheet — Client Assistance Package Checklist (abd82ed).

    A checklist-based worksheet that documents all documents, schedules, and
    data files the client is required to provide to the auditor before or
    during fieldwork.  Items are ticked off as received and verified.

    The ``position`` field distinguishes between worksheets prepared for the
    *current* (year-end) period and those prepared for an *interim* period.

    Completed worksheets serve as evidence that the audit team has obtained
    the minimum client-provided data required to commence substantive testing.

    ISA/SA references: ISA 500/SA 500 (Audit Evidence);
    ISA 315/SA 315 (Identifying and Assessing Risks).
    """

    _name = "general_audit_ws_abd82ed"
    _description = "Client Assistance Package (abd82ed)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_client_package." "worksheet_type_abd82ed"
    )
    _checklist_model_name = "general_audit_ws_abd82ed.checklist"
    _item_model_name = "general_audit_ws_abd82ed.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_abd82ed.checklist",
        help="List of checklist values recorded for this worksheet.",
    )
    position = fields.Selection(
        string="Position",
        selection=[
            ("current", "Current"),
            ("interim", "Interim"),
        ],
        help=(
            "Indicates whether this worksheet relates to the current period "
            "or an interim period."
        ),
    )
