# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models


class GeneralAuditWSf5e7049(models.Model):
    _name = "general_audit_ws_f5e7049"
    _description = "Management Integrity (f5e7049)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_f5e7049"
    )
    _checklist_model_name = "general_audit_ws_f5e7049.checklist"
    _item_model_name = "general_audit_ws_f5e7049.item"

    risk = fields.Selection(
        string="Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
    )
    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_f5e7049.checklist",
    )

    # LINK - 1 (PE.110.2.1)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_1_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_842f0d6"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_1_ids = obj.search(criteria).ids

    allowed_link_1_ids = fields.Many2many(
        string="Allowed Link 1",
        comodel_name="general_audit_ws_842f0d6",
        compute="_compute_allowed_link_1_ids",
        store=False,
    )

    link_1 = fields.Many2one(
        string="PE.110.2.1",
        ondelete="restrict",
        comodel_name="general_audit_ws_842f0d6",
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_1(self):
        self.link_1 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_842f0d6"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria, limit=1)
            if result:
                self.link_1 = result.id

    def _get_fields_required_before_confirm(self):
        _super = super(GeneralAuditWSf5e7049, self)
        res = _super._get_fields_required_before_confirm()
        res += [
            "link_1",
        ]
        return res

    def _get_custom_field_labels(self):
        return {
            "link_1": _("Money Laundring Issues"),
        }
