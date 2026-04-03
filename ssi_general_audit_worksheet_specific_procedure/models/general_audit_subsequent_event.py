# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditSubsequentEvent(models.Model):
    """Master: Subsequent Event Type.

    Defines a catalog of subsequent events to be assessed by the auditor under
    ISA 560, categorized by whether the event requires adjustment (Type 1) or
    only disclosure (Type 2) to the financial statements. Used to populate the
    event lines in the Subsequent Event worksheet (cb82c5f).
    """

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
