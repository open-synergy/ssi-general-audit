# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc94e287(models.Model):
    """
    WS.050.3 — Communication With Those Charged With Governance (c94e287)

    Documents the structured communication between the auditor and
    **those charged with governance (TCWG)** — typically the board of
    directors or audit committee — as required by ISA 260 / SA 260.
    The checklist items are classified by communication type:

    - *Understanding* — Establishing a mutual understanding of a
      supportive working relationship with TCWG.
    - *Audit info* — Relevant audit plan information communicated to
      TCWG.
    - *Expected info* — Information expected to be obtained from TCWG.
    - *Significant findings* — Significant audit findings communicated
      to TCWG before the report is issued.

    **ISA / SA references:** ISA 260 / SA 260 — Communication with
    Those Charged with Governance
    """

    _name = "general_audit_ws_c94e287"
    _description = "Communication With TCWG (c94e287)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_external_communication." "worksheet_type_c94e287"
    )
    _checklist_model_name = "general_audit_ws_c94e287.checklist"
    _item_model_name = "general_audit_ws_c94e287.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_c94e287.checklist",
        help="All checklist line records associated with this worksheet.",
    )
