# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSdae9f3c(models.Model):
    """
    WS: Audit Evidence Evaluation Checklist (dae9f3c) — ISA 500 / SA 500.

    A structured Yes / No / N-A checklist that provides a systematic
    confirmation that overall audit evidence quality requirements have been
    met before the auditor forms an opinion.  The checklist covers:

    * Confirmation that sufficient appropriate evidence has been obtained
      for all significant assertions.
    * Review of unanswered audit differences and evaluation of their
      cumulative effect against materiality thresholds.
    * Confirmation that all required subsequent-event procedures have been
      completed up to the date of the auditor's report.
    """

    _name = "general_audit_ws_dae9f3c"
    _description = "Audit Evidence Evaluation (dae9f3c)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_review." "worksheet_type_dae9f3c"
    _checklist_model_name = "general_audit_ws_dae9f3c.checklist"
    _item_model_name = "general_audit_ws_dae9f3c.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_dae9f3c.checklist",
        help=(
            "Checklist lines for this worksheet. Items are managed via the related "
            "checklist item model and evaluated within this worksheet."
        ),
    )
