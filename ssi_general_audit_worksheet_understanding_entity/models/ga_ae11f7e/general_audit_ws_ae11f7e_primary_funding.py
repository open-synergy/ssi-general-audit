# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSAE11F7EPrimaryFunding(models.Model):
    """Primary funding source entry within the Main Business Activity worksheet.

    Records the entity's primary external funding arrangements (bank loans,
    bonds, credit facilities, equity funding). Understanding the entity's
    capital structure and financing sources is required by ISA 315 (Revised)
    and supports the going concern assessment (ISA 570) and the audit of
    interest-bearing liabilities.
    """

    _name = "general_audit_ws_ae11f7e.primary_funding"
    _description = "Worksheet ae11f7e - Primary Fundings"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae11f7e",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This funding entry will be removed if the worksheet is deleted."
        ),
    )
    name = fields.Char(
        required=True,
        help="Funding source name (e.g., bank name, facility).",
    )
    type = fields.Char(
        required=True,
        help="Type of funding (e.g., loan, bond, equity).",
    )
    balance = fields.Float(
        required=True,
        help="Outstanding balance or amount.",
    )
