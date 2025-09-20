# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


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

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_842f0d6.checklist",
    )

    pmpj = fields.Selection(
        string="PMPJ",
        selection=[
            ("sederhana", "PMPJ Sederhana"),
            ("menengah", "PMPJ Menengah"),
            ("mendalam", "PMPJ Mendalam"),
        ],
    )

    # LINK - 1 (PE.110.2.2)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_1_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_805d4d5"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_1_ids = obj.search(criteria).ids

    allowed_link_1_ids = fields.Many2many(
        string="Allowed Link 1",
        comodel_name="general_audit_ws_805d4d5",
        compute="_compute_allowed_link_1_ids",
        store=False,
    )

    link_1 = fields.Many2one(
        string="PE.110.2.2",
        comodel_name="general_audit_ws_805d4d5",
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_1(self):
        self.link_1 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_805d4d5"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria)
            if result:
                self.link_1 = result.id
