# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb26d482(models.Model):
    _name = "general_audit_ws_b26d482"
    _description = "Worksheet (b26d482)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_lead_schedule." "worksheet_type_b26d482"

    balance_type = fields.Selection(
        selection=[
            ("end_period", "End Period Balance"),
            ("interim", "Interim Balance"),
        ],
        string="Balance Type",
        required=False,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Type of balance to consider for the accounts.",
    )

    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_b26d482.detail",
        inverse_name="worksheet_id",
        string="Details",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
    )

    def action_load_detail(self):
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        self.ensure_one()
        detail_model = self.env["general_audit_ws_b26d482.detail"]

        all_accounts = self.general_audit_id.mapped("detail_ids.account_id")
        existing_accounts = self.detail_ids.mapped("account_id")

        accounts_to_add = all_accounts - existing_accounts
        accounts_to_remove = existing_accounts - all_accounts

        # Add detail
        for account in accounts_to_add:
            detail_record = self.general_audit_id.detail_ids.filtered(
                lambda d: d.account_id == account
            )
            detail_model.create(
                {
                    "worksheet_id": self.id,
                    "detail_id": detail_record.id,
                }
            )

        # Remove detail
        details_to_remove = self.detail_ids.filtered(
            lambda d: d.account_id in accounts_to_remove
        )
        if details_to_remove:
            details_to_remove.unlink()
