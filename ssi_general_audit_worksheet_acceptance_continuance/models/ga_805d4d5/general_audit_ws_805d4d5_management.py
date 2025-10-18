# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS805d4d5Management(models.Model):
    _name = "general_audit_ws_805d4d5.management"
    _description = "Know Your Customer Principles (805d4d5)"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_805d4d5",
        required=True,
        ondelete="cascade",
        help="Reference to the parent Know Your Customer (KYC) worksheet.",
    )
    name = fields.Char(
        string="Name",
        help="Full name of the management person authorized to represent the entity.",
    )
    position = fields.Char(
        string="Position",
        help="Official position/title of the management person within the entity.",
    )
    identity_no = fields.Char(
        string="Identity Number",
        help="Government-issued identity/document number of the management person.",
    )
    identity_type = fields.Selection(
        string="Type of Identity",
        selection=[
            ("ktp", "KTP"),
            ("passport", "Passport"),
            ("lainnya", "Lainnya"),
        ],
        help="Type of identity document presented (e.g., KTP, Passport, Others).",
    )
