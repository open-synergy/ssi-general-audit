# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSC0E0EECDetail(models.Model):
    _name = "general_audit_ws_c0e0eec.detail"
    _description = "Worksheet c0e0eec - Detail"
    _order = "worksheet_id, category_id, factor_id, indicator_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_c0e0eec",
        required=True,
        ondelete="cascade",
    )
    indicator_id = fields.Many2one(
        string="Indicator",
        comodel_name="general_audit_fraud_factor_indicator",
        required=True,
    )
    factor_id = fields.Many2one(
        related="indicator_id.factor_id",
        store=True,
    )
    category_id = fields.Many2one(
        related="indicator_id.factor_id.category_id",
        store=True,
    )
    tcgw = fields.Text(
        string="TCGW",
    )
    management = fields.Text(
        string="Management",
    )
    other = fields.Text(
        string="Other",
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_c0e0eec_detail_2_account_type",
        column1="detail_id",
        column2="type_id",
        required=True,
    )
