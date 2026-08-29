# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsA3c9d2eChecklistProcedure(models.Model):
    """Specific analytical procedure performed within a category (a3c9d2e).

    Unlike the category itself (mandatory, loaded from master via
    ``action_populate_checklist``), procedure lines are optional and
    added manually by the auditor ("Add a line") — only the items
    actually performed are selected from the category's master list
    (``procedure_item_id``), not auto-populated.
    """

    _name = "general_audit_ws_a3c9d2e.checklist_procedure"
    _description = "Analytical Procedures – Cycle (a3c9d2e) - Procedure"
    _order = "checklist_id, sequence, id"

    checklist_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_ws_a3c9d2e.checklist",
        required=True,
        ondelete="cascade",
        help="Category this procedure was performed under.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help="Ordering number used to sort lines; lower values appear first.",
    )
    procedure_item_id = fields.Many2one(
        string="Item",
        comodel_name="general_audit_ws_a3c9d2e.procedure_item",
        required=True,
        help=(
            "Analytical procedure item selected from the category's "
            "master list (e.g. Trend Analysis, Gross Profit Percentage)."
        ),
    )
    result = fields.Selection(
        string="Result",
        selection=[
            ("high", "High"),
            ("moderate", "Moderate"),
        ],
        help="Result of this specific analytical procedure.",
    )

    def name_get(self):
        """Display the procedure item's name, with its own result
        appended when set (e.g. for the category tree's
        ``many2many_tags`` summary, such as "Trend Analysis (High)").

        :return: list of ``(id, display_name)`` tuples.
        :rtype: list
        """
        result_labels = dict(self._fields["result"].selection)
        names = []
        for record in self:
            name = record.procedure_item_id.display_name
            if record.result:
                name = "%s (%s)" % (name, result_labels[record.result])
            names.append((record.id, name))
        return names
