# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import api, fields, models


class GeneralAuditStandardDetail(models.Model):
    _name = "general_audit.standard_detail"
    _inherit = ["general_audit.standard_detail"]

    a13a30e_detail_ids = fields.Many2many(
        string="A13A30E Details",
        comodel_name="general_audit_ws_a13a30e.detail",
        relation="rel_general_audit_ws_a13a30e_detail_2_standard_detail",
        column1="standard_detail_id",
        column2="detail_id",
    )
    regulation_impacted = fields.Boolean(
        string="Impacted By Regulation",
        compute="_compute_regulation_impacted",
        store=True,
        compute_sudo=True,
    )
    bdcdfc5_detail_ids = fields.Many2many(
        string="BDCDFC5 Details",
        comodel_name="general_audit_ws_bdcdfc5.detail",
        relation="rel_general_audit_ws_bdcdfc5_detail_2_standard_detail",
        column1="standard_detail_id",
        column2="detail_id",
    )
    business_environmeny_impacted = fields.Boolean(
        string="Impacted By Business Environment",
        compute="_compute_business_environmeny_impacted",
        store=True,
        compute_sudo=True,
    )
    c0e0eec_detail_ids = fields.Many2many(
        string="C0E0EEC Details",
        comodel_name="general_audit_ws_c0e0eec.detail",
        relation="rel_general_audit_ws_c0e0eec_detail_2_standard_detail",
        column1="standard_detail_id",
        column2="detail_id",
    )
    fraud_impacted = fields.Boolean(
        string="Impacted By Fraud",
        compute="_compute_fraud_impacted",
        store=True,
        compute_sudo=True,
    )
    ae11f7e_expert_ids = fields.Many2many(
        string="AE11F7E Experts",
        comodel_name="general_audit_ws_ae11f7e.expert",
        relation="rel_general_audit_ws_ae11f7e_expert_2_standard_detail",
        column1="standard_detail_id",
        column2="expert_id",
    )
    expert_impacted = fields.Boolean(
        string="Impacted By Use of Expert",
        compute="_compute_expert_impacted",
        store=True,
        compute_sudo=True,
    )
    ae11f7e_previous_audit_information_ids = fields.Many2many(
        string="AE11F7E Previous Significant Audit Information",
        comodel_name="general_audit_ws_ae11f7e.previous_audit_information",
        relation="rel_general_audit_ws_ae11f7e_prev_audit_2_standard_detail",
        column1="standard_detail_id",
        column2="prev_audit_id",
    )
    previous_audit_information_impacted = fields.Boolean(
        string="Impacted By Previous Audit Information",
        compute="_compute_previous_audit_information_impacted",
        store=True,
        compute_sudo=True,
    )
    ae11f7e_previous_other_information_ids = fields.Many2many(
        string="AE11F7E Previous Significant Other Information",
        comodel_name="general_audit_ws_ae11f7e.previous_other_information",
        relation="rel_general_audit_ws_ae11f7e_prev_other_2_standard_detail",
        column1="standard_detail_id",
        column2="prev_other_id",
    )
    previous_other_information_impacted = fields.Boolean(
        string="Impacted By Previous Other Information",
        compute="_compute_previous_other_information_impacted",
        store=True,
        compute_sudo=True,
    )
    ae11f7e_other_information_ids = fields.Many2many(
        string="AE11F7E Other Significant Information",
        comodel_name="general_audit_ws_ae11f7e.other_information",
        relation="rel_general_audit_ws_ae11f7e_other_2_standard_detail",
        column1="standard_detail_id",
        column2="other_id",
    )
    other_information_impacted = fields.Boolean(
        string="Impacted By Other Information",
        compute="_compute_other_information_impacted",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "a13a30e_detail_ids",
    )
    def _compute_regulation_impacted(self):
        for record in self:
            result = False
            if record.a13a30e_detail_ids:
                result = True
            record.regulation_impacted = result

    @api.depends(
        "bdcdfc5_detail_ids",
    )
    def _compute_business_environmeny_impacted(self):
        for record in self:
            result = False
            if record.bdcdfc5_detail_ids:
                result = True
            record.business_environmeny_impacted = result

    @api.depends(
        "c0e0eec_detail_ids",
    )
    def _compute_fraud_impacted(self):
        for record in self:
            result = False
            if record.c0e0eec_detail_ids:
                result = True
            record.fraud_impacted = result

    @api.depends(
        "ae11f7e_expert_ids",
    )
    def _compute_expert_impacted(self):
        for record in self:
            result = False
            if record.ae11f7e_expert_ids:
                result = True
            record.expert_impacted = result

    @api.depends(
        "ae11f7e_previous_audit_information_ids",
    )
    def _compute_previous_audit_information_impacted(self):
        for record in self:
            result = False
            if record.ae11f7e_previous_audit_information_ids:
                result = True
            record.previous_audit_information_impacted = result

    @api.depends(
        "ae11f7e_previous_other_information_ids",
    )
    def _compute_previous_other_information_impacted(self):
        for record in self:
            result = False
            if record.ae11f7e_previous_other_information_ids:
                result = True
            record.previous_other_information_impacted = result

    @api.depends(
        "ae11f7e_other_information_ids",
    )
    def _compute_other_information_impacted(self):
        for record in self:
            result = False
            if record.ae11f7e_other_information_ids:
                result = True
            record.other_information_impacted = result
