# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSddf034cAdmComposition(models.Model):
    _name = "general_audit_ws_ddf034c.adm_composition"
    _description = (
        "General Information and Legal Aspec (ddf034c) - " "Composition (Amendment)"
    )
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ddf034c",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the ddf034c worksheet that this composition line belongs to. "
            "If the worksheet is deleted, related composition lines are removed (cascade)."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help=(
            "Controls the display order of composition entries. "
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
    admin_name = fields.Char(
        string="Name",
        help=("Full name of the person listed in the amended management composition."),
    )
    admin_position = fields.Char(
        string="Position",
        help=(
            "Position/title held in the amended management composition "
            "(e.g., Director, Commissioner)."
        ),
    )
