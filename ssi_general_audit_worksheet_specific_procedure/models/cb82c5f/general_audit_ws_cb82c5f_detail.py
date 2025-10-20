# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWScb82c5fDetail(models.Model):
    _name = "general_audit_ws_cb82c5f.detail"
    _description = "Subsequent Event (cb82c5f) - Detail"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_cb82c5f",
        string="Worksheet",
        required=True,
        ondelete="cascade",
    )
    subsequent_event_id = fields.Many2one(
        comodel_name="general_audit_subsequent_event",
        string="Subsequent Event",
        required=True,
        help="Subsequent event being evaluated",
    )
    occurance = fields.Boolean(
        default=False,
        string="Occurance",
        help="Indicate whether the subsequent event has occurred or not",
    )
    adjustment_entry_detail_ids = fields.Many2many(
        comodel_name="client_adjustment_entry.detail",
        string="Adjustment Entry Lines",
        relation="rel_cb82c5f_detail_2_adjustment_entry_detail",
        column1="detail_id",
        column2="adjustment_entry_id",
        help="Adjustment entry lines related to the subsequent event",
    )
    adjustment_ids = fields.Many2many(
        comodel_name="client_adjustment_entry",
        string="Adjustments",
        compute="_compute_adjustment_ids",
        help="Adjustments related to the subsequent event",
        compute_sudo=True,
    )
    adjustment_dr = fields.Monetary(
        string="Adjustment DR",
        currency_field="currency_id",
        help="Debit amount of the adjustment related to the subsequent event",
        compute="_compute_adjustment",
        store=True,
        compute_sudo=True,
    )
    adjustment_cr = fields.Monetary(
        string="Adjustment CR",
        currency_field="currency_id",
        help="Credit amount of the adjustment related to the subsequent event",
        compute="_compute_adjustment",
        store=True,
        compute_sudo=True,
    )
    currency_id = fields.Many2one(
        related="worksheet_id.general_audit_id.currency_id",
        string="Currency",
        help="Currency used for the amounts",
        store=True,
    )
    to_disclose = fields.Boolean(
        string="To Disclose",
        default=False,
        help="Indicate whether the subsequent event needs to be disclosed",
    )
    disclosure = fields.Text(
        string="Disclosure",
        help="Details of the disclosure for the subsequent event",
    )
    reference = fields.Char(
        string="Reference",
        help="Reference information related to the subsequent event",
    )

    @api.depends("adjustment_entry_detail_ids")
    def _compute_adjustment_ids(self):
        for record in self:
            record.adjustment_ids = record.adjustment_entry_detail_ids.mapped(
                "entry_id"
            )

    @api.depends(
        "adjustment_entry_detail_ids",
        "adjustment_entry_detail_ids.debit",
        "adjustment_entry_detail_ids.credit",
    )
    def _compute_adjustment(self):
        for record in self:
            record.adjustment_dr = sum(
                record.adjustment_entry_detail_ids.mapped("debit")
            )
            record.adjustment_cr = sum(
                record.adjustment_entry_detail_ids.mapped("credit")
            )
