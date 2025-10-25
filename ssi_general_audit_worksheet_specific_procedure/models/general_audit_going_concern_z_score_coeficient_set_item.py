# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditGoingConcernZScoreCoefficientSetItem(models.Model):
    _name = "general_audit_going_concern_z_score_coeficient_set.item"
    _description = "General Audit - Going Concern Z-Score Coefficient Set - Item"

    set_id = fields.Many2one(
        comodel_name="general_audit_going_concern_z_score_coeficient_set",
        string="Z-Score Coefficient Set",
        required=True,
        ondelete="cascade",
        help="Parent Z-Score coefficient set to which this item belongs.",
    )
    computation_item_id = fields.Many2one(
        comodel_name="trial_balance_computation_item",
        string="Computation Item",
        required=True,
        help="Trial balance computation item associated with this coefficient.",
    )
    coefficient = fields.Float(
        string="Coefficient",
        digits=(16, 6),
        required=True,
        help="Weight/Coefficient applied to the computation item within the set.",
    )
