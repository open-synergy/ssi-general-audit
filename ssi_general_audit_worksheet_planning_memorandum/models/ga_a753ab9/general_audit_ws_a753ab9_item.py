# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSa753ab9Item(models.Model):
    """
    Checklist item master for the Audit Planning Memorandum (a753ab9).

    Each item defines a **single planning consideration** that the auditor must
    address before fieldwork commences.  Items are organised into five planning
    areas via ``checklist_type``:

    * ``characteristic``  — Characteristics of the Engagement
    * ``reporting``       — Reporting Objectives
    * ``important``       — Important Factors
    * ``significant``     — Significant Changes and Developments
    * ``nature``          — Nature, Timing, and Extent of Resources Required

    The optional ``related_field`` stores a dotted-path field reference
    (e.g., ``general_audit_id.partner_id``) that the detail summary worksheet
    (``general_audit_ws_fbbe0f8``) uses to render dynamic labels and pull
    summarised values from upstream worksheets.

    Modifying, creating, or deleting items clears the LRU cache on
    ``general_audit_ws_fbbe0f8.get_dynamic_labels`` so that labels are
    re-computed on the next access.
    """

    _name = "general_audit_ws_a753ab9.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Audit Planning Memorandum (a753ab9) - " "Checklist Item"

    code = fields.Char(
        default="/",
    )
    checklist_type = fields.Selection(
        string="Type of Checklist",
        selection=[
            ("characteristic", "Characteristics of the Engagement"),
            ("reporting", "Reporting Objectives"),
            ("important", "Important Factors"),
            ("significant", "Significant Changes and Developments"),
            ("nature", "Nature, Timing, and Extent of Resources Required"),
        ],
        required=True,
        help="Defines the category of checklist where this item is used.",
    )
    related_field = fields.Char()

    @api.model_create_multi
    def create(self, vals_list):
        _super = super(GeneralAuditWSa753ab9Item, self)
        res = _super.create(vals_list)
        self.env["general_audit_ws_fbbe0f8"].get_dynamic_labels.cache_clear()
        return res

    def write(self, vals):
        _super = super(GeneralAuditWSa753ab9Item, self)
        res = _super.write(vals)
        self.env["general_audit_ws_fbbe0f8"].get_dynamic_labels.cache_clear()
        return res

    def unlink(self):
        _super = super(GeneralAuditWSa753ab9Item, self)
        res = _super.unlink()
        self.env["general_audit_ws_fbbe0f8"].get_dynamic_labels.cache_clear()
        return res
