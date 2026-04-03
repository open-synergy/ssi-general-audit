# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditGoingConcernCategory(models.Model):
    """Master: Going Concern Category.

    Classifies going concern indicators into high-level categories per
    ISA 570 (Revised) / SA 570 (e.g., Financial, Operating, Other). Used
    to organise the preliminary going concern worksheet (c0d0898) display
    and to structure the auditor's assessment of going concern conditions.
    """

    _name = "general_audit_going_concern_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Going Concern Category"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
