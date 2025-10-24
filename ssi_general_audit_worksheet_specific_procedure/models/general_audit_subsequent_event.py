# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditSubsequentEvent(models.Model):
    _name = "general_audit_subsequent_event"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Subsequent Event"

    code = fields.Char(
        default="/",
        help="Unique short code for the team role. Use '/' to auto-generate.",
    )
    need_adjustment = fields.Boolean(
        string="Need Adjustment",
        help=(
            "Indicates whether the subsequent event requires adjustment "
            "to the financial statements."
        ),
    )
