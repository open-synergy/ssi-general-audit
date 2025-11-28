# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models


class GeneralAuditWS842f0d6(models.Model):
    _name = "general_audit_ws_842f0d6"
    _description = "Money Laudring Issues (842f0d6)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_842f0d6"
    )
    _checklist_model_name = "general_audit_ws_842f0d6.checklist"
    _item_model_name = "general_audit_ws_842f0d6.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_842f0d6.checklist",
        help="Checklist lines belonging to this Money Laundering Issues worksheet.",
    )

    pmpj = fields.Selection(
        string="PMPJ",
        selection=[
            ("simplified", "PMPJ Simplified"),
            ("intermediate", "PMPJ Intermediate"),
            ("enhanced", "PMPJ Enhanced"),
        ],
        help="""Risk categorization level for KYC obligations:
Simplified, Intermediate, or Enhanced.""",
    )

    # LINK - 1 (PE.110.2.2)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_1(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_805d4d5"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_1_ids = obj.search(criteria)
            if link_1_ids:
                result = link_1_ids.id
            record.link_1 = result

    link_1 = fields.Many2one(
        string="PE.110.2.2",
        comodel_name="general_audit_ws_805d4d5",
        compute_sudo=True,
        compute="_compute_link_1",
        store=True,
        help="""Selected worksheet used as a reference
for this analysis.""",
    )

    def action_reload_links(self):
        for record in self.sudo():
            record._reload_links()

    def _reload_links(self):
        self.ensure_one()
        self._compute_link_1()

    def _get_fields_required_before_confirm(self):
        _super = super(GeneralAuditWS842f0d6, self)
        res = _super._get_fields_required_before_confirm()
        res += [
            "link_1",
        ]
        return res

    def _get_custom_field_labels(self):
        return {
            "link_1": _("Know Your Customer Principles"),
        }
