# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWScda3a68(models.Model):
    """
    WS.040.2 — Management's Expert (cda3a68)

    Documents the auditor's evaluation of a **management's expert** —
    an individual or organisation engaged by management to produce
    information that the auditor uses as audit evidence.  Under
    ISA 500 / SA 500 and ISA 315 / SA 315, the auditor must assess
    whether the expert's work can be used as reliable audit evidence,
    considering:

    - The expert's competence, capability, and objectivity.
    - The adequacy of the expert's work relative to the audit purpose.
    - Any significant assumptions or methods used by the expert.

    The evaluation is structured via ``detail_ids`` lines, each tied to
    a master ``factor``.  Conclusion and review fields on the parent
    ``general_audit_worksheet`` capture the overall assessment.

    **ISA / SA references:** ISA 500 / SA 500 — Audit Evidence;
    ISA 315 / SA 315 — Identifying and Assessing the Risks of Material
    Misstatement
    """

    _name = "general_audit_ws_cda3a68"
    _description = "Management Expert (cda3a68)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.expert",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_expert." "worksheet_type_cda3a68"
    _detail_model_name = "general_audit_ws_cda3a68.detail"
    _factor_model_name = "general_audit_ws_cda3a68.factor"

    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_cda3a68.detail",
        help=(
            "Checklist lines associated with this worksheet "
            "(Previous Financial Reporting Issues)."
        ),
    )
