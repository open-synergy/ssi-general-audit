# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb3ff42f(models.Model):
    """
    WS.050.2 — Communication With Management (b3ff42f)

    Documents the structured communication between the auditor and
    **management** as required by ISA 260 / SA 260 and ISA 265 / SA 265.
    The checklist items are classified by communication type:

    - *Understanding* — Establishing a mutual understanding of a
      supportive working relationship.
    - *Audit info* — Relevant audit plan information communicated to
      management.
    - *Expected info* — Information expected to be obtained from
      management.
    - *Significant findings* — Significant audit findings communicated
      to management before the report is issued.

    **ISA / SA references:** ISA 260 / SA 260 — Communication with TCWG;
    ISA 265 / SA 265 — Communicating Deficiencies in Internal Control
    """

    _name = "general_audit_ws_b3ff42f"
    _description = "Communication With Management (b3ff42f)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_external_communication." "worksheet_type_b3ff42f"
    )
    _checklist_model_name = "general_audit_ws_b3ff42f.checklist"
    _item_model_name = "general_audit_ws_b3ff42f.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_b3ff42f.checklist",
        help="All checklist line records associated with this worksheet.",
    )
