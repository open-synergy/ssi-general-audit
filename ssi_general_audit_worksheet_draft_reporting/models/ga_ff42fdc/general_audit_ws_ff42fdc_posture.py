# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GeneralAuditWsFf42fdcPosture(models.Model):
    """Worksheet (ff42fdc) - Posture Line.

    Two kinds of line share this model, distinguished by ``line_type``:

    * ``"group"`` -- one record per ``client_account_group`` that has
      accounts used on the parent General Audit, aggregating the
      Unaudited, Adjustment (Debit/Credit), Audited, and Previous
      amounts of every ``general_audit.detail`` line whose account
      belongs to that group.
    * ``"total"`` -- one record per ``total_type`` (nine fixed
      subtotal/total rows, e.g. Total Asset, Gross Profit), computed
      by applying the signed ``client_account_group.code`` formula of
      ``_TOTAL_TYPE_FORMULA`` directly against the parent General
      Audit's ``detail_ids``. Total lines always exist, regardless of
      whether their component groups have any data.

    Populated/synchronised via ``action_load_posture`` on the parent
    ``general_audit_ws_ff42fdc`` worksheet, mirroring the diff-based
    sync pattern used by ``general_audit_ws_b26d482._load_detail``.
    """

    _name = "general_audit_ws_ff42fdc.posture"
    _description = "Worksheet (ff42fdc) - Posture Line"
    _order = "sequence, id"

    _TOTAL_TYPE_FORMULA = {
        "total_asset": (("T001", 1), ("T002", 1)),
        "total_liability": (("T003", 1), ("T004", 1)),
        "total_equity": (("T005", 1), ("T007", 1)),
        "total_liability_equity": (
            ("T003", 1),
            ("T004", 1),
            ("T005", 1),
            ("T007", 1),
        ),
        "gross_profit": (("T009", 1), ("T011", -1)),
        "operating_profit": (("T009", 1), ("T011", -1), ("T012", -1)),
        "profit_before_tax": (
            ("T009", 1),
            ("T011", -1),
            ("T012", -1),
            ("T010", 1),
            ("T013", -1),
        ),
        "profit_after_tax": (
            ("T009", 1),
            ("T011", -1),
            ("T012", -1),
            ("T010", 1),
            ("T013", -1),
            ("T014", -1),
        ),
        "comprehensive_profit": (
            ("T009", 1),
            ("T011", -1),
            ("T012", -1),
            ("T010", 1),
            ("T013", -1),
            ("T014", -1),
            ("T015", 1),
        ),
    }

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_ff42fdc",
        string="Worksheet",
        required=True,
        ondelete="cascade",
        help="Audit Result worksheet that owns this posture line.",
    )
    line_type = fields.Selection(
        string="Line Type",
        selection=[
            ("group", "Account Group"),
            ("total", "Total"),
        ],
        required=True,
        default="group",
        help="Whether this line summarises one account group, or is "
        "one of the nine fixed Total/Subtotal rows.",
    )
    group_id = fields.Many2one(
        comodel_name="client_account_group",
        string="Account Group",
        ondelete="restrict",
        help="Client account group summarised by this posture line. "
        "Required for Account Group lines; left empty for Total "
        "lines.",
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
            ("comprehensive_profit", "Comprehensive Profit"),
        ],
        help="Which fixed Total/Subtotal row this line represents. "
        "Only set for Total lines.",
    )
    sequence = fields.Integer(
        string="Sequence",
        store=True,
        help="Display order, assigned by ``_load_posture`` so Total "
        "rows are interleaved right after their component groups.",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="worksheet_id.general_audit_id.currency_id",
        store=False,
        help="Currency used for amounts; inherited from the General " "Audit.",
    )
    unaudited = fields.Monetary(
        string="Unaudited",
        currency_field="currency_id",
        compute="_compute_amounts",
        store=True,
        compute_sudo=True,
        help="Sum of End Period Balance for every account under this " "group.",
    )
    adjustment_debit = fields.Monetary(
        string="Adjustment (Debit)",
        currency_field="currency_id",
        compute="_compute_amounts",
        store=True,
        compute_sudo=True,
        help="Sum of Adjustment Debit for every account under this " "group.",
    )
    adjustment_credit = fields.Monetary(
        string="Adjustment (Credit)",
        currency_field="currency_id",
        compute="_compute_amounts",
        store=True,
        compute_sudo=True,
        help="Sum of Adjustment Credit for every account under this " "group.",
    )
    audited = fields.Monetary(
        string="Audited",
        currency_field="currency_id",
        compute="_compute_amounts",
        store=True,
        compute_sudo=True,
        help="Sum of Audited Balance for every account under this " "group.",
    )
    previous = fields.Monetary(
        string="Previous",
        currency_field="currency_id",
        compute="_compute_amounts",
        store=True,
        compute_sudo=True,
        help="Sum of Previous Period Balance for every account under " "this group.",
    )

    @api.depends(
        "line_type",
        "group_id",
        "total_type",
        "worksheet_id",
        "worksheet_id.general_audit_id.detail_ids.home_statement_balance",
        "worksheet_id.general_audit_id.detail_ids.adjustment_debit",
        "worksheet_id.general_audit_id.detail_ids.adjustment_credit",
        "worksheet_id.general_audit_id.detail_ids.audited_balance",
        "worksheet_id.general_audit_id.detail_ids.previous_balance",
    )
    def _compute_amounts(self):
        """Aggregate audit detail amounts for this posture line.

        Account Group lines (``line_type == "group"``) sum every
        column from the parent General Audit's ``detail_ids`` whose
        ``account_id.group_id`` matches ``group_id``. Total lines
        (``line_type == "total"``) apply the signed
        ``client_account_group.code`` formula of
        ``_TOTAL_TYPE_FORMULA`` directly against ``detail_ids`` --
        never against other Total lines -- so the result does not
        depend on compute order. The per-row ``audited_balance``
        already accounts for the account's normal balance side, so it
        is summed directly without being recomputed here.

        :return: nothing; assigns ``unaudited``, ``adjustment_debit``,
            ``adjustment_credit``, ``audited``, and ``previous``
        """
        for record in self:
            result_unaudited = 0.0
            result_adjustment_debit = 0.0
            result_adjustment_credit = 0.0
            result_audited = 0.0
            result_previous = 0.0
            all_details = record.worksheet_id.general_audit_id.detail_ids
            if record.line_type == "group" and record.group_id:
                details = all_details.filtered(
                    lambda d: d.account_id.group_id == record.group_id
                )
                result_unaudited = sum(details.mapped("home_statement_balance"))
                result_adjustment_debit = sum(details.mapped("adjustment_debit"))
                result_adjustment_credit = sum(details.mapped("adjustment_credit"))
                result_audited = sum(details.mapped("audited_balance"))
                result_previous = sum(details.mapped("previous_balance"))
            elif record.line_type == "total" and record.total_type:
                for code, sign in record._get_total_type_formula():
                    code_details = all_details.filtered(
                        lambda d, code=code: d.account_id.group_id.code == code
                    )
                    result_unaudited += sign * sum(
                        code_details.mapped("home_statement_balance")
                    )
                    result_adjustment_debit += sign * sum(
                        code_details.mapped("adjustment_debit")
                    )
                    result_adjustment_credit += sign * sum(
                        code_details.mapped("adjustment_credit")
                    )
                    result_audited += sign * sum(code_details.mapped("audited_balance"))
                    result_previous += sign * sum(
                        code_details.mapped("previous_balance")
                    )
            record.unaudited = result_unaudited
            record.adjustment_debit = result_adjustment_debit
            record.adjustment_credit = result_adjustment_credit
            record.audited = result_audited
            record.previous = result_previous

    def _posture_line_order_key(self):
        """Return the key this line is looked up by in the layout table.

        Used by ``general_audit_ws_ff42fdc._resequence_posture_lines``
        to match this line against ``_POSTURE_LINE_ORDER``.

        :return: a ``(line_type, code)`` tuple, where ``code`` is
            ``group_id.code`` for Account Group lines and
            ``total_type`` for Total lines
        """
        self.ensure_one()
        if self.line_type == "group":
            return ("group", self.group_id.code)
        return ("total", self.total_type)

    def _get_total_type_formula(self):
        """Return the ``(code, sign)`` pairs for this line's total type.

        :return: a tuple of ``(client_account_group.code, sign)``
            pairs, or an empty tuple when ``total_type`` is not set
        """
        self.ensure_one()
        return self._TOTAL_TYPE_FORMULA.get(self.total_type, ())

    @api.constrains("line_type", "group_id", "total_type")
    def _check_line_type_consistency(self):
        """Ensure the companion field matches this line's ``line_type``.

        An Account Group line must carry ``group_id``; a Total line
        must carry ``total_type``.

        :raises ValidationError: when the companion field required by
            ``line_type`` is missing
        """
        for record in self:
            if record.line_type == "group" and not record.group_id:
                error_message = _(
                    """
Context: Set posture line type
Database ID: %s
Problem: Account Group posture lines require an Account Group
Solution: Set the Account Group, or change the line to Total
"""
                    % (record.id,)
                )
                raise ValidationError(error_message)
            if record.line_type == "total" and not record.total_type:
                error_message = _(
                    """
Context: Set posture line type
Database ID: %s
Problem: Total posture lines require a Total Type
Solution: Set the Total Type, or change the line to Account Group
"""
                    % (record.id,)
                )
                raise ValidationError(error_message)
