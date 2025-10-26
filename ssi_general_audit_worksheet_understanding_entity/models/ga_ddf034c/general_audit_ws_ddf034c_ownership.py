# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSddf034cOwnership(models.Model):
    _name = "general_audit_ws_ddf034c.ownership"
    _description = "General Information and Legal Aspec (ddf034c) - " "Ownership"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ddf034c",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the ddf034c worksheet this ownership record belongs to. "
            "If the worksheet is deleted, related ownership records are removed (cascade)."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help=(
            "Controls the display order of ownership entries. "
            "Lower values appear first."
        ),
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help=(
            "Status of the parent worksheet. "
            "Read-only and synchronized from the worksheet."
        ),
    )
    ownership_location_id = fields.Many2one(
        string="Ownership Location",
        comodel_name="ownership_location",
        ondelete="restrict",
        help=(
            "Location/site for which the ownership status "
            "is recorded (e.g., head office, branch, facility)."
        ),
    )
    ownership_state = fields.Selection(
        string="Status",
        selection=[
            ("owned", "Owned"),
            ("leased", "Leased"),
            ("other", "Others"),
        ],
        help=(
            "Ownership status of the specified location: Owned, Leased, or Others. "
            "Use 'Others' for cases not covered by the predefined options."
        ),
    )
