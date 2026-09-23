# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWorksheet(models.Model):
    """Adds ``category_id`` so the "Sumber" drill-down can group by it.

    ``general_audit_worksheet`` only carries ``parent_type_id`` (the
    specific worksheet type); its audit-phase category lives one hop
    further, on ``parent_type_id.category_id``. Odoo's list view
    ``group_by`` cannot target a dotted relation, so this related
    field re-exposes it directly on this model -- used by
    ``general_audit_ws_b66777d.team_allocation.action_view_source_
    worksheets()`` to group the drill-down by PE/RA/RR/Windup &
    Reporting.
    """

    _inherit = "general_audit_worksheet"

    category_id = fields.Many2one(
        string="Category",
        related="parent_type_id.category_id",
        store=True,
        help=(
            "Audit phase category of this worksheet's type (PE/RA/RR/"
            "Windup & Reporting), mirrored from parent_type_id."
            "category_id. Stored so it can be grouped by in list "
            "views."
        ),
    )
