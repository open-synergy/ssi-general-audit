# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditRelatedPartyConfirmationProcedure(models.Model):
    """Master: Related Party Confirmation Procedure.

    Defines standard confirmation procedures used when auditing related party
    transactions under ISA 550. These procedure items are referenced in the
    Related Party Transaction worksheet (c40cfd9) to track which confirmation
    steps have been performed for each engagement.
    """

    _name = "general_audit_related_party_confirmation_procedure"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Related Party Confirmation Procedure"
    _order = "sequence, id"

    code = fields.Char(
        default="/",
        help="Unique short code for the team role. Use '/' to auto-generate.",
    )

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Gives the sequence order when displaying a list of procedures.",
    )
