# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSf9f3299(models.Model):
    _name = "general_audit_ws_f9f3299"
    _description = "Lead Schedule - Account (f9f3299)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_lead_schedule." "worksheet_type_f9f3299"

    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Standard Account Type",
        required=True,
        states={
            "draft": [("readonly", False)],
        },
        readonly=True,
        ondelete="restrict",
    )
    allowed_account_type_ids = fields.Many2many(
        comodel_name="client_account_type",
        string="Allowed Account Types",
        help="Account types that can be selected",
        compute="_compute_allowed_account_type_ids",
        store=False,
    )

    balance_type = fields.Selection(
        selection=[
            ("end_period", "End Period Balance"),
            ("interim", "Interim Balance"),
        ],
        string="Balance Type",
        required=True,
        default="end_period",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
        help="Type of balance to consider for the accounts.",
    )
    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_f9f3299.detail",
        inverse_name="worksheet_id",
        string="Details",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
        help="Detailed lines for each account in the lead schedule.",
    )

    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_account_type_ids(self):
        for record in self:
            record.allowed_account_type_ids = self.env["client_account_type"]
            if record.general_audit_id:
                record.allowed_account_type_ids = record.general_audit_id.mapped(
                    "standard_detail_ids.type_id"
                )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_account_type_id(self):
        self.account_type_id = False

    def action_reload_account(self):
        for record in self.sudo():
            record._reload_account()

    def _reload_account(self):
        self.ensure_one()
        self.detail_ids.unlink()
        for detail in self.general_audit_id.detail_id:
            data = {
                "worksheet_id": self.id,
                "detail_id": detail.id,
                "account_id": detail.account_id.id,
            }
            self.env["general_audit_ws_f9f3299.detail"].create(data)
