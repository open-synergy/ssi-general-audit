# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbab9d32(models.Model):
    """
    WS.040.1 — Auditor's Expert (bab9d32)

    Documents the auditor's evaluation of an **auditor's expert** (an
    individual or organisation whose expertise is used by the auditor)
    as required by ISA 620 / SA 620 (Using the Work of an Auditor's
    Expert).  When the auditor plans to use the work of an expert, this
    worksheet records:

    - Identity and field of expertise of the expert.
    - Which significant accounts or disclosures are affected by the
      expert's work.
    - The party contracting with the expert.
    - Evaluation factors such as competence, capabilities, objectivity,
      and the adequacy of the expert's scope.

    The evaluation is structured via ``detail_ids`` lines, each tied to
    a master ``factor`` (e.g., competence, objectivity).  Conclusion and
    review fields on the parent ``general_audit_worksheet`` capture the
    overall assessment.

    **ISA / SA references:** ISA 620 / SA 620 — Using the Work of an
    Auditor's Expert
    """

    _name = "general_audit_ws_bab9d32"
    _description = "Auditor Expert (bab9d32)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.expert",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_expert." "worksheet_type_bab9d32"
    _detail_model_name = "general_audit_ws_bab9d32.detail"
    _factor_model_name = "general_audit_ws_bab9d32.factor"

    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_bab9d32.detail",
        help=(
            "Checklist lines associated with this worksheet "
            "(Previous Financial Reporting Issues)."
        ),
    )
