# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSBA9B2F0(models.Model):
    """
    Significant Account Internal Control (ba9b2f0) — ROMM Extension

    Adds a "Medium" option to the existing ``risk`` field so it can also
    serve as the auditor's Control Risk conclusion for this significant
    account, consumed by the Account Level ROMM Matrix A ("Audit Risk"),
    which needs a Low/Medium/High scale rather than the original Low/High.
    Takes precedence over ``general_audit_ws_eabdaad.risk`` when both are
    available for the same account (more specific).
    """

    _name = "general_audit_ws_ba9b2f0"
    _inherit = ["general_audit_ws_ba9b2f0"]

    risk = fields.Selection(
        selection_add=[("medium", "Medium"), ("high",)],
    )
