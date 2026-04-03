# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditITControl(models.Model):
    """Master data — IT General Control (ITGC) library item.

    Represents one IT control (e.g., Logical Access Review, Password Policy,
    Change Control Approval) within a given IT control category.  Controls
    are evaluated using the responses defined in ``option_set_id``.

    Grouped into IT control sets (``general_audit_it_control_set``) that are
    assigned to the IT Control Evaluation worksheet (f63f569).
    """

    _name = "general_audit_it_control"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit General Control"
    _order = "category_id, sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Ordering of IT controls within the category.",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_it_control_category",
        required=False,
        help="Category to which this IT control belongs.",
    )
    option_set_id = fields.Many2one(
        string="Option Set",
        comodel_name="checklist.option_set",
        required=True,
        ondelete="restrict",
        help="Option set that defines the allowed options for this item.",
    )
