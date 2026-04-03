# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWScda3a68Category(models.Model):
    """
    Management's Expert Worksheet — Evaluation Factor Category (cda3a68)

    Groups the evaluation factors used in the Management's Expert
    worksheet (WS.040.2).  Typical categories correspond to main
    ISA 500 / SA 500 considerations: competence, capability, and
    objectivity of the management-engaged expert.
    """

    _name = "general_audit_ws_cda3a68.category"
    _inherit = [
        "mixin.expert.category",
    ]
    _description = "Management Expert (cda3a68) - Category"

    code = fields.Char(
        default="/",
        help="Internal code/identifier for the Expert Category. Defaults to '/'.",
    )
