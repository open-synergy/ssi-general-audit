# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbab9d32Category(models.Model):
    """
    Auditor's Expert Worksheet — Evaluation Factor Category (bab9d32)

    Groups the evaluation factors used in the Auditor's Expert worksheet
    (WS.040.1).  Typical categories correspond to the main ISA 620 / SA 620
    considerations: competence, capabilities, and objectivity.
    """

    _name = "general_audit_ws_bab9d32.category"
    _inherit = [
        "mixin.expert.category",
    ]
    _description = "Auditor Expert (bab9d32) - Category"

    code = fields.Char(
        default="/",
        help="Internal code/identifier for the Expert Category. Defaults to '/'.",
    )
