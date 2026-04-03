# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSfc75636(models.Model):
    """
    WS: Independent Auditor's Report Review Checklist (fc75636) — ISA 700 / SA 700.

    A structured Yes / No / N-A checklist for reviewing the **draft
    independent auditor's report** before it is issued, ensuring compliance
    with the applicable ISA / SA reporting standards.

    Checklist item types (``checklist_type``):

    * ``unmodified``       — Requirements for an unmodified (clean) opinion
      under ISA 700 / SA 700.
    * ``modified``         — Additional requirements when a modified opinion
      (qualified, adverse, disclaimer) is issued per ISA 705 / SA 705.
    * ``emphasis_other``   — Requirements for Emphasis of Matter and Other
      Matter paragraphs per ISA 706 / SA 706.

    Items are further grouped by ``category_id``
    (``general_audit_ws_fc75636.category``) to organise the review by
    report section or paragraph type.
    """

    _name = "general_audit_ws_fc75636"
    _description = "Independen Auditor Report Review(fc75636)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_review." "worksheet_type_fc75636"
    _checklist_model_name = "general_audit_ws_fc75636.checklist"
    _item_model_name = "general_audit_ws_fc75636.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_fc75636.checklist",
        help="Checklist lines for this worksheet.",
    )
