# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc40cfd9ConfirmationProcedure(models.Model):
    """Confirmation procedure line for the Related Party Transaction worksheet (c40cfd9).

    Each line represents one confirmation procedure from the master list of
    related party confirmation procedures, recording whether it was performed
    and any relevant notes. Supports completeness documentation for related
    party audit procedures under ISA 550.
    """

    _name = "general_audit_ws_c40cfd9.confirmation_procedure"
    _description = "Related Party Transaction (c40cfd9) - Confirmation Procedure"
    _order = "worksheet_id, confirmation_procedure_id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_c40cfd9",
        string="Worksheet",
        required=True,
        ondelete="cascade",
        help="Parent Related Party Transaction worksheet for this confirmation line.",
    )
    confirmation_procedure_id = fields.Many2one(
        comodel_name="general_audit_related_party_confirmation_procedure",
        string="Confirmation Procedure",
        required=True,
        ondelete="restrict",
        help="The confirmation procedure to be performed.",
    )
    performed = fields.Selection(
        selection=[
            ("performed", "Performed"),
            ("not_performed", "Not Performed"),
            ("na", "Not Applicable"),
        ],
        string="Performed",
        default="not_performed",
        required=True,
        help="Indicates whether the procedure has been performed.",
    )
    reference = fields.Char(
        string="Reference",
        help="Reference for the procedure performed.",
    )
