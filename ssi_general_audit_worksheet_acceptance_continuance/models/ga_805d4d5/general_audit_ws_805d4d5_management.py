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
    )
    name = fields.Char(
        string="Name",
    )
    position = fields.Char(
        string="Position",
    )
    identity_no = fields.Char(
        string="Identity Number",
    )
    identity_type = fields.Selection(
        string="Type of Identity",
        selection=[
            ("ktp", "KTP"),
            ("passport", "Passport"),
            ("lainnya", "Lainnya"),
        ],
    )
