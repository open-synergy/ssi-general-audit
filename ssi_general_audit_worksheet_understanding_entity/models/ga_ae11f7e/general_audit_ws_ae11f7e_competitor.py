# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSAE11F7ECompetitor(models.Model):
    """Competitor entry within the Main Business Activity worksheet.

    Records key competitors of the audit client and their relative market
    position. Understanding competitive pressures helps the auditor assess
    industry-related risks (ISA 315) and evaluate management's business
    assumptions in areas such as revenue recognition and asset impairment.
    """

    _name = "general_audit_ws_ae11f7e.competitor"
    _description = "Worksheet ae11f7e - Competitor"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae11f7e",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This competitor entry will be removed if the worksheet is deleted."
        ),
    )
    name = fields.Char(
        string="Competitor",
        required=True,
        help="Competitor name.",
    )
    size = fields.Float(
        required=True,
        help=(
            "Relative size or market share of the competitor "
            "(e.g., percentage of market or qualitative size)."
        ),
    )
