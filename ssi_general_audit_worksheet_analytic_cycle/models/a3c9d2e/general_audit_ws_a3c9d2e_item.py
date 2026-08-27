# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsA3c9d2eItem(models.Model):
    """Analytical procedure category master (a3c9d2e).

    Each record is one mandatory category of the Analytical Procedures –
    Cycle checklist (e.g. "Analytical Procedures for Sales Revenue"),
    scoped to a single ``business_cycle_id``. Loaded onto a worksheet via
    ``action_populate_checklist`` once the worksheet's business cycle is
    selected.
    """

    _name = "general_audit_ws_a3c9d2e.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Analytical Procedures – Cycle (a3c9d2e) - Category"

    code = fields.Char(
        default="/",
        help="""Internal code for the category.
Defaults to '/'; may be replaced by a generated sequence depending on configuration.""",
    )
    business_cycle_id = fields.Many2one(
        string="Business Cycle",
        comodel_name="client_business_process",
        required=True,
        ondelete="restrict",
        help="Business cycle this analytical procedure category belongs to.",
    )
