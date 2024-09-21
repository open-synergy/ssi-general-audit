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
