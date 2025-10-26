# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditCompetencyUpgrade(models.Model):
    _name = "general_audit_competency_upgrade"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Competency Upgrade"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help=(
            "Ordering number to control how records are displayed in lists "
            "and reports. Lower numbers appear first."
        ),
    )
    compentency_item_id = fields.Many2one(
        string="Competency",
        comodel_name="general_audit_ws_b9d8a5c.competency_item",
        required=True,
        ondelete="restrict",
        help=(
            "The competency item that requires an upgrade for the team member. "
            "Sourced from PE.110.3 competency items."
        ),
    )
