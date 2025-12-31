# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSddf034cAdmShareholding(models.Model):
    _name = "general_audit_ws_ddf034c.adm_shareholding"
    _description = (
        "General Information and Legal Aspec (ddf034c) - "
        "Shareholding Structure (Amendment)"
    )
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ddf034c",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the ddf034c worksheet that this shareholding line belongs to. "
            "If the worksheet is deleted, related shareholding lines are removed (cascade)."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help=(
            "Controls the display order of shareholding entries. "
            "Lower values appear first."
        ),
    )
    state = fields.Selection(
        related="worksheet_id.state",
        compute_sudo=True,
        help=(
            "Status of the parent worksheet. "
            "This value is read-only and synchronized from the worksheet."
        ),
    )
    shareholder_name = fields.Char(
        string="Name",
        help=(
            "Full name of the shareholder as per the amended shareholding structure."
        ),
    )
    shareholder_number = fields.Integer(
        string="Number",
        help=(
            "Number of shares held by the shareholder according to the latest amendment."
        ),
    )
