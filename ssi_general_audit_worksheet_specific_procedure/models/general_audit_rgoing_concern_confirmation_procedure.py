# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditGoingConcernConfirmationProcedure(models.Model):
    """Master: Going Concern Confirmation Procedure.

    Defines standard confirmation procedures used during the going concern
    assessment under ISA 570. These procedures are referenced in the Going
    Concern worksheet (fbf57ee) to systematically document the evidence-gathering
    steps performed to evaluate whether a material uncertainty exists.
    """

    _name = "general_audit_going_concern_confirmation_procedure"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Going Concern Confirmation Procedure"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Gives the sequence order when displaying a list of procedures.",
    )
