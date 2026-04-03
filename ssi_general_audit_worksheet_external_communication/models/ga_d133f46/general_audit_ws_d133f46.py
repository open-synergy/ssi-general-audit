# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd133f46(models.Model):
    """
    WS.050.4 — Use of Internal Auditor's Work Results (d133f46)

    Documents the external auditor's evaluation of whether the work
    performed by the client's **internal audit function** can be used
    as audit evidence, as required by ISA 610 / SA 610 (Using the Work
    of Internal Auditors).  The evaluation criteria are:

    - *Objectivity* — Whether the internal audit function operates
      independently and objectively.
    - *Technical competence* — Whether the internal auditors possess
      adequate technical skills and expertise.
    - *Professional due care* — Whether the work has been planned,
      supervised, reviewed, and documented appropriately.

    Only work meeting all three criteria may be used as a substitute
    for or supplement to the external auditor's own procedures.

    **ISA / SA references:** ISA 610 / SA 610 — Using the Work of
    Internal Auditors
    """

    _name = "general_audit_ws_d133f46"
    _description = "Use of Internal Auditor's Work Results (d133f46)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_external_communication." "worksheet_type_d133f46"
    )
    _checklist_model_name = "general_audit_ws_d133f46.checklist"
    _item_model_name = "general_audit_ws_d133f46.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_d133f46.checklist",
        help="All checklist line records associated with this worksheet.",
    )
