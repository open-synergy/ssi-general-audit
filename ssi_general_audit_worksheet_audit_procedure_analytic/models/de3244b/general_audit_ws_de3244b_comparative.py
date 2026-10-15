# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWsDe3244bComparative(models.Model):
    """Comparative line for Comparative Audit Procedure (WS-DE3244B).

    Each record compares one realization variable against one or two
    comparative variables defined in the same worksheet, following the
    comparative analytical procedure of SA 520.  For every comparative
    the realization is expressed as a percentage of it.
    """

    _name = "general_audit_ws_de3244b.comparative"
    _description = "Comparative Audit Procedure - Comparative"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_de3244b",
        string="Worksheet",
        required=True,
        ondelete="cascade",
        index=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    name = fields.Char(
        string="Item Name",
        required=True,
        help="Name of the item being compared.",
    )
    realization_variable_id = fields.Many2one(
        comodel_name="general_audit_ws_de3244b.variable",
        string="Realization Variable",
        required=True,
        help="Variable holding the realization (current period) amount.",
    )
    comparative1_variable_id = fields.Many2one(
        comodel_name="general_audit_ws_de3244b.variable",
        string="Comparative 1 Variable",
        required=True,
        help="Variable holding the first comparative amount.",
    )
    comparative2_variable_id = fields.Many2one(
        comodel_name="general_audit_ws_de3244b.variable",
        string="Comparative 2 Variable",
        required=False,
        help="Variable holding the optional second comparative amount.",
    )
    realization_amount = fields.Float(
        string="Realization",
        digits=(16, 2),
        related="realization_variable_id.value",
        store=False,
        compute_sudo=True,
        help="Value of the realization variable.",
    )
    comparative1_amount = fields.Float(
        string="Comparative 1",
        digits=(16, 2),
        related="comparative1_variable_id.value",
        store=False,
        compute_sudo=True,
        help="Value of the first comparative variable.",
    )
    comparative2_amount = fields.Float(
        string="Comparative 2",
        digits=(16, 2),
        related="comparative2_variable_id.value",
        store=False,
        compute_sudo=True,
        help="Value of the second comparative variable.",
    )
    diff1 = fields.Float(
        string="%-tase",
        digits=(16, 2),
        compute="_compute_diff1",
        store=True,
        compute_sudo=True,
        help="Percentage of the realization against the first comparative: "
        "Realization / Comparative 1 * 100. Zero when Comparative 1 is zero.",
    )
    diff2 = fields.Float(
        string="%-tase",
        digits=(16, 2),
        compute="_compute_diff2",
        store=True,
        compute_sudo=True,
        help="Percentage of the realization against the second comparative: "
        "Realization / Comparative 2 * 100. Zero when Comparative 2 is zero "
        "or not selected.",
    )
    result = fields.Text(
        string="Result",
        help="Auditor's conclusion or notes on this comparative line.",
    )

    @api.model
    def _percentage_ratio(self, realization, comparative):
        """Compute the realization as a percentage of a comparative amount.

        :param realization: realization amount.
        :param comparative: comparative amount used as the base.
        :return: ``realization / comparative * 100``, or ``0.0`` when
            ``comparative`` is zero.
        """
        if not comparative:
            return 0.0
        return realization / comparative * 100.0

    @api.depends(
        "realization_variable_id.value",
        "comparative1_variable_id.value",
    )
    def _compute_diff1(self):
        """Compute ``diff1`` from the realization and first comparative.

        :return: sets ``diff1`` on each record.
        """
        for record in self:
            result = 0.0
            if record.realization_variable_id and record.comparative1_variable_id:
                result = record._percentage_ratio(
                    record.realization_variable_id.value,
                    record.comparative1_variable_id.value,
                )
            record.diff1 = result

    @api.depends(
        "realization_variable_id.value",
        "comparative2_variable_id.value",
    )
    def _compute_diff2(self):
        """Compute ``diff2`` from the realization and second comparative.

        :return: sets ``diff2`` on each record, ``0.0`` when the second
            comparative is not selected.
        """
        for record in self:
            result = 0.0
            if record.realization_variable_id and record.comparative2_variable_id:
                result = record._percentage_ratio(
                    record.realization_variable_id.value,
                    record.comparative2_variable_id.value,
                )
            record.diff2 = result
