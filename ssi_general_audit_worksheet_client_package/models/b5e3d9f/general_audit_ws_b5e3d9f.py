# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSb5e3d9f(models.Model):
    _name = "general_audit_ws_b5e3d9f"
    _description = "Subledger (b5e3d9f)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_client_package." "worksheet_type_b5e3d9f"
    )

    account_id = fields.Many2one(
        comodel_name="client_account",
        string="Account",
        required=False,
        ondelete="restrict",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Account related to this subledger entry.",
    )
    allowed_account_ids = fields.Many2many(
        comodel_name="client_account",
        string="Allowed Accounts",
        related="general_audit_id.account_ids",
        compute_sudo=True,
    )
    detail_id = fields.Many2one(
        comodel_name="general_audit.detail",
        string="Detail",
        compute="_compute_detail_id",
        store=True,
        readonly=True,
        compute_sudo=True,
    )
    raw_data = fields.Text(
        string="Raw Data",
        help="Raw data in CSV format",
        required=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    amount_ids = fields.One2many(
        comodel_name="general_audit_ws_b5e3d9f.amount",
        inverse_name="worksheet_id",
        string="Amounts",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    thousand_separator = fields.Char(
        string="Thousand Separator",
        help="Character used as thousand separator in the CSV data",
        required=False,
        default=",",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    decimal_separator = fields.Char(
        string="Decimal Separator",
        help="Character used as decimal separator in the CSV data",
        required=False,
        default=".",
        readonly=True,
        states={"open": [("readonly", False)]},
    )

    @api.depends("general_audit_id", "account_id")
    def _compute_detail_id(self):
        for record in self:
            result = False
            if record.general_audit_id and record.account_id:
                result = self.env["general_audit.detail"].search(
                    [
                        ("general_audit_id", "=", record.general_audit_id.id),
                        ("account_id", "=", record.account_id.id),
                    ],
                    limit=1,
                )
            record.detail_id = result
