# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsA3c9d2eProcedureItem(models.Model):
    """Analytical procedure item master (a3c9d2e).

    Each record is one specific analytical procedure (e.g. "Trend
    Analysis") that may be selected under a given category
    (``category_id``, e.g. "Analytical Procedures for Sales Revenue"),
    following the reference checklist document. Selected manually per
    worksheet line ("Add Line" — see
    ``general_audit_ws_a3c9d2e.checklist_procedure``), not
    auto-populated: only the items actually performed are added.
    """

    _name = "general_audit_ws_a3c9d2e.procedure_item"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Analytical Procedures – Cycle (a3c9d2e) - Procedure Item"
    _order = "category_id, sequence, id"

    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_ws_a3c9d2e.item",
        required=True,
        ondelete="restrict",
        help="Category this procedure item belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Ordering of the procedure item within its category.",
    )
