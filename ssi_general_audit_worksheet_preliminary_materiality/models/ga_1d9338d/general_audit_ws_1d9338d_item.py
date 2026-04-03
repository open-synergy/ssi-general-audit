# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS1d9338dItem(models.Model):
    """
    Checklist item master for the Preliminary Materiality Checklist (1d9338d).

    Each item defines a **single materiality procedure step** that the auditor
    must confirm has been completed.  Items are categorised by ``checklist_type``:

    * ``materiality_comp``  — Steps related to performing and documenting the
      materiality computation (base amount, percentages, OM/PM/TM).
    * ``account_mapping``   — Steps related to mapping account balances against
      materiality thresholds and identifying material accounts.
    """

    _name = "general_audit_ws_1d9338d.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Preliminary Materiality (1d9338d) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help=(
            "Technical code/reference for the checklist item. Use '/' to "
            "let the system generate a code."
        ),
    )
    checklist_type = fields.Selection(
        string="Type of Checklist",
        selection=[
            ("materiality_comp", "Materiality Computation"),
            ("account_mapping", "Material Accounts Mapping"),
        ],
        required=True,
        help="Defines the category of checklist where this item is used.",
    )
