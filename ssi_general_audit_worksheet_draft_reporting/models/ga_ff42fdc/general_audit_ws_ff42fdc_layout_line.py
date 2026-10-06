# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GeneralAuditWsFf42fdcLayoutLine(models.Model):
    """Worksheet (ff42fdc) - Posture Report Layout Line.

    Configurable master data that fixes the display order of the
    Posture Report. Each record names one row of the report, either an
    Account Group row or one of the fixed Total rows, and its position
    through ``sequence``. ``_resequence_posture_lines`` on the
    worksheet reads these records, so adding a group or moving a Total
    row needs no code change. Scope is global: one layout applies to
    every General Audit engagement. Account groups that are not listed
    here are still shown, after every listed row.
    """

    _name = "general_audit_ws_ff42fdc.layout_line"
    _description = "Worksheet (ff42fdc) - Posture Report Layout Line"
    _order = "sequence, id"

    line_type = fields.Selection(
        string="Line Type",
        selection=[
            ("group", "Account Group"),
            ("total", "Total"),
        ],
        required=True,
        default="group",
        help="Whether this row of the report is an Account Group row or "
        "one of the fixed Total rows.",
    )
    group_id = fields.Many2one(
        comodel_name="client_account_group",
        string="Account Group",
        ondelete="restrict",
        help="Account group shown by this row. Required for Account "
        "Group rows; left empty for Total rows.",
    )
    total_type = fields.Selection(
        string="Total Type",
        selection=[
            ("total_asset", "Total Asset"),
            ("total_liability", "Total Liability"),
            ("total_equity", "Total Equity"),
            ("total_liability_equity", "Total Liability and Equity"),
            ("gross_profit", "Gross Profit"),
            ("operating_profit", "Operating Profit"),
            ("profit_before_tax", "Profit Before Tax"),
            ("profit_after_tax", "Profit After Tax"),
            ("comprehensive_profit", "Comprehensive Income"),
        ],
        help="Total row shown by this row. Required for Total rows; "
        "left empty for Account Group rows.",
    )
    show_adjustment = fields.Boolean(
        string="Show Adjustment",
        default=True,
        help="Whether a Total row shows its Adjustment (Debit) and "
        "Adjustment (Credit) columns. Untick it for rows whose signed "
        "subtotals make the adjustment columns meaningless, such as the "
        "profit and loss subtotals. Ignored for Account Group rows.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Display order of the row in the Posture Report. Applied "
        "to a worksheet when its posture is reloaded.",
    )

    def _layout_key(self):
        """Return the key matching this row against a posture line.

        Mirrors ``general_audit_ws_ff42fdc.posture._posture_line_order_key``.

        :return: a ``(line_type, code)`` tuple, where ``code`` is
            ``group_id.code`` for Account Group rows and ``total_type``
            for Total rows
        """
        self.ensure_one()
        if self.line_type == "group":
            return ("group", self.group_id.code)
        return ("total", self.total_type)

    @api.constrains("line_type", "group_id", "total_type")
    def _check_line_type_consistency(self):
        """Ensure the companion field matches this row's ``line_type``.

        :raises ValidationError: when an Account Group row has no
            account group, or a Total row has no total type
        """
        for record in self:
            if record.line_type == "group" and not record.group_id:
                error_message = _(
                    """
Context: Set layout line type
Database ID: %s
Problem: Account Group layout lines require an Account Group
Solution: Set the Account Group, or change the line to Total
"""
                    % (record.id,)
                )
                raise ValidationError(error_message)
            if record.line_type == "total" and not record.total_type:
                error_message = _(
                    """
Context: Set layout line type
Database ID: %s
Problem: Total layout lines require a Total Type
Solution: Set the Total Type, or change the line to Account Group
"""
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("line_type", "group_id", "total_type")
    def _check_unique_line(self):
        """Ensure each Account Group or Total appears once in the layout.

        :raises ValidationError: when another row already shows the same
            account group or total type
        """
        for record in self:
            if record.line_type == "group":
                criteria = [
                    ("line_type", "=", "group"),
                    ("group_id", "=", record.group_id.id),
                ]
            else:
                criteria = [
                    ("line_type", "=", "total"),
                    ("total_type", "=", record.total_type),
                ]
            duplicates = self.search(criteria + [("id", "!=", record.id)], limit=1)
            if duplicates:
                error_message = _(
                    """
Context: Configure the Posture Report layout
Database ID: %s
Problem: The layout already has a line for this Account Group or Total Type
Solution: Edit the existing line instead of adding another one
"""
                    % (record.id,)
                )
                raise ValidationError(error_message)
