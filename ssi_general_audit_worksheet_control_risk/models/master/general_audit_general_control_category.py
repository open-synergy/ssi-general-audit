# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditGeneralControlCategory(models.Model):
    """Master data — category for grouping general controls.

    Organises general control items into logical groups (e.g., Control
    Environment, Risk Assessment, Information & Communication, Monitoring)
    for structured presentation in the General Control Evaluation.
    """

    _name = "general_audit_general_control_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit General Control Category"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Ordering of general control categories.",
    )
