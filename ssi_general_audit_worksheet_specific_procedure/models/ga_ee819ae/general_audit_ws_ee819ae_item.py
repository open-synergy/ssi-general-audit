# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSee819aeItem(models.Model):
    """Checklist item master for the Commitment and Contingent worksheet (ee819ae).

    Defines the set of standard checklist items/questions used across all
    Commitment and Contingent worksheets. Each item has a code, description,
    and checklist type, providing a reusable framework for the commitment and
    contingent liability assessment under ISA 501.
    """

    _name = "general_audit_ws_ee819ae.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Commitment and Contingent (ee819ae) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="""Internal code for the checklist item.
Defaults to '/'; may be replaced by a generated sequence depending on configuration.""",
    )
