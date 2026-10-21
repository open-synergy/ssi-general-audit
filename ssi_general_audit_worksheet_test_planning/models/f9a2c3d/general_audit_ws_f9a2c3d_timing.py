# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsF9a2c3dTiming(models.Model):
    """Test of Detail Timing master (f9a2c3d).

    Reference list of the moments a Test of Detail may be performed, used in the
    Test of Detail Planning worksheet.
    """

    _name = "general_audit_ws_f9a2c3d_timing"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Test of Detail Timing (f9a2c3d)"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Display order of the timings.",
    )
