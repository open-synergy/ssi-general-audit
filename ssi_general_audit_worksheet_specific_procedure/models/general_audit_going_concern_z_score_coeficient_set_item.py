# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditGoingConcernZScoreCoefficientSetItem(models.Model):
    """Master: Going Concern Z-Score Coefficient Set Item.

    Defines one coefficient within a Z-Score coefficient set, linking a
    trial balance computation item (e.g., Working Capital / Total Assets)
    to its corresponding weighting coefficient in the Altman Z-Score formula.
    Used to drive the automatic computation lines in the Going Concern
    worksheet (fbf57ee) under ISA 570.
    """

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
        ondelete="restrict",
        help="Trial balance computation item associated with this coefficient.",
    )
    coefficient = fields.Float(
        string="Coefficient",
        digits=(16, 6),
        required=True,
        help="Weight/Coefficient applied to the computation item within the set.",
    )
