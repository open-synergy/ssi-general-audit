# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditITControlCategory(models.Model):
    """Master data — category for grouping IT General Controls (ITGC).

    Organises IT control items into logical groups (e.g., Logical Access,
    Change Management, IT Operations, Data Backup) for structured
    presentation in the IT Control Evaluation.
    """

    _name = "general_audit_it_control_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit IT Control Category"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Ordering of IT control categories.",
    )
