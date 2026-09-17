# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsB66777dProperty(models.Model):
    """Master data: one configurable row of the "Details" tab (b66777d).

    Defines a Property/Python Code pair that
    ``general_audit_ws_b66777d.action_populate_detail()`` snapshots into
    a ``general_audit_ws_b66777d.detail`` row for every worksheet it is
    run on. Same shape as ``trial_balance_computation_item`` (also
    ``mixin.master_data`` + ``sequence`` + ``python_code``) -- editable
    through the Configuration menu, not hardcoded in Python, so the 11
    Details rows can be added to/edited/deactivated without a code
    change.
    """

    _name = "general_audit_ws_b66777d.property"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Independent Auditor Report (b66777d) - Detail Property"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Ordering number for this property in the Details tab.",
    )
    python_code = fields.Text(
        string="Python Code",
        required=True,
        default='result = ""',
        help=(
            "Python snippet evaluated on every Populate click to "
            "derive this property's Value. Must assign its result to "
            "a variable named 'result'. Available names: 'env' and "
            "'document' (the general_audit_ws_b66777d.detail row being "
            "filled)."
        ),
    )
