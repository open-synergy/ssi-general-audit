# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa025441(models.Model):
    _name = "general_audit_ws_a025441"
    _description = "Financial Statement Disclosure (a025441)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_review." "worksheet_type_a025441"
    _checklist_model_name = "general_audit_ws_a025441.checklist"
    _item_model_name = "general_audit_ws_a025441.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_a025441.checklist",
        help="Checklist lines for this worksheet.",
    )

    def _get_checklist_item_domain(self):
        _super = super(GeneralAuditWSa025441, self)
        res = _super._get_checklist_item_domain()
        fa_standard_id = self.general_audit_id.financial_accounting_standard_id
        new_domain = [("financial_accounting_standard_id", "=", fa_standard_id.id)]
        res += new_domain
        return res
