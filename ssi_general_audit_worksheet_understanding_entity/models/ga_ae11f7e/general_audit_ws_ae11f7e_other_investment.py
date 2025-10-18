# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSAE11F7EOtherInvestment(models.Model):
    _name = "general_audit_ws_ae11f7e.other_investment"
    _description = "Worksheet ae11f7e - Other Investments"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae11f7e",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This investment entry will be removed if the worksheet is deleted."
        ),
    )
    name = fields.Char(
        required=True,
        help="Name/description of the other investment or instrument.",
    )
    percentage = fields.Float(
        required=True,
        help="Ownership percentage or proportion held.",
    )
    value = fields.Float(
        required=True,
        help="Carrying amount or value of the investment.",
    )
