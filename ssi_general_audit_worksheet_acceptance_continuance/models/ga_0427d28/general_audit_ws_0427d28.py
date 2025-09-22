# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWS0427d28(models.Model):
    _name = "general_audit_ws_0427d28"
    _description = "Communication With Previous Auditor (0427d28)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_0427d28"
    )
    _checklist_model_name = "general_audit_ws_0427d28.checklist"
    _item_model_name = "general_audit_ws_0427d28.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_0427d28.checklist",
    )
    risk = fields.Selection(
        string="Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("tidak_relevan", "Tidak Relevan"),
        ],
    )

    @api.depends("general_audit_id", "general_audit_id.num_of_consecutive_audit_firm")
    def _compute_engagemet(self):
        for record in self:
            record.engagemet = "Initial Engagement"
            record.engagemet_ok = False
            if (record.general_audit_id.num_of_consecutive_audit_firm) >= 1:
                record.engagemet = "Recurring Engagement"
                record.engagemet_ok = True

    engagemet = fields.Char(
        string="Engagement",
        compute="_compute_engagemet",
        store=True,
    )
    engagemet_ok = fields.Boolean(
        string="Engagement Type",
        compute="_compute_engagemet",
        store=True,
    )
