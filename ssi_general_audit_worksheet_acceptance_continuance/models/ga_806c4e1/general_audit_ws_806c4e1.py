# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWS806C4E1(models.Model):
    _name = "general_audit_ws_806c4e1"
    _description = (
        "Acceptance and Continuance of " "Client Relationships Analysis (806c4e1)"
    )
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_806c4e1"
    )
    _checklist_model_name = "general_audit_ws_806c4e1.checklist"
    _item_model_name = "general_audit_ws_806c4e1.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_806c4e1.checklist",
    )
    risk = fields.Selection(
        string="Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
    )
    client_relationship = fields.Selection(
        string="Continue the Cient Relationship",
        selection=[
            ("ya", "Ya"),
            ("tidak", "Tidak"),
        ],
    )

    # LINK - 1 (PE.110.1)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_1_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_369c5a5"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_1_ids = obj.search(criteria).ids

    allowed_link_1_ids = fields.Many2many(
        string="Allowed Link 1",
        comodel_name="general_audit_ws_369c5a5",
        compute="_compute_allowed_link_1_ids",
        store=False,
    )

    link_1 = fields.Many2one(
        string="PE.110.1",
        comodel_name="general_audit_ws_369c5a5",
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_1(self):
        self.link_1 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_369c5a5"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria)
            if result:
                self.link_1 = result.id

    # LINK - 2 (PE.110.2)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_2_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_f5e7049"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_2_ids = obj.search(criteria).ids

    allowed_link_2_ids = fields.Many2many(
        string="Allowed Link 2",
        comodel_name="general_audit_ws_f5e7049",
        compute="_compute_allowed_link_2_ids",
        store=False,
    )

    link_2 = fields.Many2one(
        string="PE.110.2",
        comodel_name="general_audit_ws_f5e7049",
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_2(self):
        self.link_2 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_f5e7049"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria)
            if result:
                self.link_2 = result.id

    # LINK - 3 (PE.110.3)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_3_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_b9d8a5c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_3_ids = obj.search(criteria).ids

    allowed_link_3_ids = fields.Many2many(
        string="Allowed Link 3",
        comodel_name="general_audit_ws_b9d8a5c",
        compute="_compute_allowed_link_3_ids",
        store=False,
    )

    link_3 = fields.Many2one(
        string="PE.110.3",
        comodel_name="general_audit_ws_b9d8a5c",
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_3(self):
        self.link_3 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_b9d8a5c"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria)
            if result:
                self.link_3 = result.id

    # LINK - 4 (PE.110.4)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_4_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_0427d28"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_4_ids = obj.search(criteria).ids

    allowed_link_4_ids = fields.Many2many(
        string="Allowed Link 4",
        comodel_name="general_audit_ws_0427d28",
        compute="_compute_allowed_link_4_ids",
        store=False,
    )

    link_4 = fields.Many2one(
        string="PE.110.4",
        comodel_name="general_audit_ws_0427d28",
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_4(self):
        self.link_4 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_0427d28"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria)
            if result:
                self.link_4 = result.id
