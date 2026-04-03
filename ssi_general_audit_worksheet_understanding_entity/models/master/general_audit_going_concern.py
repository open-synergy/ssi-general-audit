# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditGoingConcern(models.Model):
    """Master: Going Concern Indicator.

    Defines the going concern indicators to be assessed in the preliminary
    going concern worksheet (c0d0898). Each indicator belongs to a category
    (financial, operational, or other) per ISA 570 (Revised) / SA 570. The
    master list is automatically loaded into each worksheet when the worksheet
    is opened, ensuring all standard indicators are evaluated for every audit.
    """

    _name = "general_audit_going_concern"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Going Concern"
    _order = "category_id, sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_going_concern_category",
        ondelete="restrict",
        required=True,
    )
