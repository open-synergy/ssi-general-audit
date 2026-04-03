# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc8740d4(models.Model):
    """
    WS: Preliminary Analytic Procedure — Summary (c8740d4) — ISA 315 / SA 315.

    The primary worksheet for documenting the results of preliminary analytical
    procedures performed during the audit planning phase.  It combines:

    * A **structured checklist** (``checklist_ids``) where the auditor
      responds Yes / No / N-A to confirm that each prescribed step of the
      preliminary analytical procedure has been performed.
    * **Conclusion narratives** (``conclusion_ids``) where the auditor documents
      the results and inferences drawn from the analyses, organised by
      ``analytic_procedure_conclusion_category``.

    This worksheet serves as the audit team leader's sign-off document that
    preliminary analytical procedures have been completed and that identified
    risks and unusual items have been considered in the audit plan.
    """

    _name = "general_audit_ws_c8740d4"
    _description = "Preliminary Analytic Procedure (c8740d4)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_preliminary_analytic_procedure."
        "worksheet_type_c8740d4"
    )
    _checklist_page_xpath = "//page[@name='preliminary']"
    _checklist_model_name = "general_audit_ws_c8740d4.checklist"
    _item_model_name = "general_audit_ws_c8740d4.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_c8740d4.checklist",
        help="Checklist answers captured for this worksheet.",
    )
    conclusion_ids = fields.One2many(
        string="Conclusion(s)",
        comodel_name="general_audit_ws_c8740d4.analytic_procedure_conclusion",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Conclusion lines summarizing the results of the analytic " "procedures."
        ),
    )
