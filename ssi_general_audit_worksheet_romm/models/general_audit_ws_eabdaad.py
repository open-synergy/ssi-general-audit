# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSEABDAAD(models.Model):
    """
    Business Cycle Internal Control (eabdaad) — ROMM Extension

    Adds a "Medium" option to the existing ``risk`` field so it can also
    serve as the auditor's per-cycle Control Risk conclusion consumed by
    the Account Level ROMM Matrix A ("Audit Risk"), which needs a
    Low/Medium/High scale rather than the original Low/High.
    """

    _name = "general_audit_ws_eabdaad"
    _inherit = ["general_audit_ws_eabdaad"]

    risk = fields.Selection(
        selection_add=[("medium", "Medium"), ("high",)],
    )
