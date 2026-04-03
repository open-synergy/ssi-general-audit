# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSdae9f3cItem(models.Model):
    """
    Checklist item master for the Audit Evidence Evaluation Checklist (dae9f3c).

    Each item defines a **quality assurance procedure step** related to audit
    evidence evaluation, such as confirming that sufficient appropriate
    evidence has been obtained or that misstatements have been evaluated
    against materiality.  Items are managed via the master data interface and
    applied consistently across all engagements.
    """

    _name = "general_audit_ws_dae9f3c.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Audit Evidence Evaluation (dae9f3c) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="Item code or number. Use '/' to auto-generate the code.",
    )
