# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditGoingConcernZScoreCoefficientSet(models.Model):
    _name = "general_audit_going_concern_z_score_coeficient_set"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Going Concern Z-Score Coefficient Set"

    item_ids = fields.One2many(
        comodel_name="general_audit_going_concern_z_score_coeficient_set.item",
        inverse_name="set_id",
        string="Computation Items",
    )
