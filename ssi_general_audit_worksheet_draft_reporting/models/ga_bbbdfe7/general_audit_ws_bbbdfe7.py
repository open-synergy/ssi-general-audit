# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbbbdfe7(models.Model):
    """Worksheet — Management Representation (bbbdfe7).

    A checklist-based worksheet for obtaining and documenting management's
    written representations under ISA 580 / SA 580.  The auditor goes through
    each required representation item (``checklist_ids``), records whether
    management has confirmed it, adds any clarifying comments, and attaches
    the signed representation letter.

    Written representations are required as audit evidence for matters that
    the auditor cannot otherwise obtain sufficient appropriate evidence, and
    as corroboration of oral representations made during the audit.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 580/SA 580 (Written Representations).
    """

    _name = "general_audit_ws_bbbdfe7"
    _description = "Management Representation (bbbdfe7)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_draft_reporting." "worksheet_type_bbbdfe7"
    )
    _checklist_model_name = "general_audit_ws_bbbdfe7.checklist"
    _item_model_name = "general_audit_ws_bbbdfe7.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_bbbdfe7.checklist",
        help="Checklist lines for this worksheet.",
    )
