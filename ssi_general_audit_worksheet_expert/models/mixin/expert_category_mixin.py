# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class MixinExpertCategory(models.AbstractModel):
    """
    Abstract base class for Expert Evaluation Factor Categories.

    Provides a categorisation layer for expert evaluation factors.  Each
    concrete ``*.category`` model (e.g., ``general_audit_ws_bab9d32.category``
    for Auditor's Expert and ``general_audit_ws_cda3a68.category`` for
    Management's Expert) inherits this mixin.  Categories group evaluation
    factors into logical themes such as competence, capabilities, or
    objectivity, which correspond to the ISA 620 / SA 620 and ISA 500 / SA 500
    evaluation criteria.
    """

    _name = "mixin.expert.category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Abstract Base for Expert Categories"

    code = fields.Char(
        default="/",
        help="Unique code for the option set. Use '/' to auto-generate.",
    )
