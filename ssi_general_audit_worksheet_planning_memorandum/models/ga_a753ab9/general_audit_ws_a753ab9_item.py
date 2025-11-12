# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSa753ab9Item(models.Model):
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
