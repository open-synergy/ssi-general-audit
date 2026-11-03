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
      by applying the signed ``client_account_group`` formula
      configured on ``general_audit_ws_ff42fdc.total_formula``
      directly against the parent General Audit's ``detail_ids``.
      Total lines always exist, regardless of whether their
      component groups have any data.

    Populated/synchronised via ``action_load_posture`` on the parent
    ``general_audit_ws_ff42fdc`` worksheet, mirroring the diff-based
    sync pattern used by ``general_audit_ws_b26d482._load_detail``.
    """

    _name = "general_audit_ws_ff42fdc.posture"
    _description = "Worksheet (ff42fdc) - Posture Line"
    _order = "sequence, id"

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
            ("comprehensive_profit", "Comprehensive Income"),
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
    adjustment_visible = fields.Boolean(
        string="Adjustment Visible",
        compute="_compute_amounts",
        store=True,
        compute_sudo=True,
        help="False for a Total line whose layout line has Show "
        "Adjustment unticked: its adjustment columns are zero and "
        "hidden.",
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
        "worksheet_id.general_audit_id.closing_line_ids.account_id",
        "worksheet_id.general_audit_id.closing_line_ids.account_group_id",
        "worksheet_id.general_audit_id.closing_line_ids.debit",
        "worksheet_id.general_audit_id.closing_line_ids.credit",
    )
    def _compute_amounts(self):
        """Aggregate audit detail amounts for this posture line.

        Account Group lines (``line_type == "group"``) sum every
        column from the parent General Audit's ``detail_ids`` whose
        ``account_id.group_id`` matches ``group_id``. Total lines
        (``line_type == "total"``) apply the signed
        ``client_account_group`` formula configured on
        ``general_audit_ws_ff42fdc.total_formula`` directly against
        ``detail_ids`` -- never against other Total lines -- so the
        result does not depend on compute order. A ``total_type``
        with no configured formula line yields zero on every column,
        rather than raising. The per-row ``audited_balance`` already
        accounts for the account's normal balance side, so it is
        summed directly without being recomputed here.
        Adjustment columns of a Total line are the plain sums of the
        debit and credit adjustments of its component groups, without
        applying the formula sign, because a debit adjustment on an
        expense group is still a debit to equity. A Total line whose
        layout line has ``show_adjustment`` unticked keeps both columns
        at zero and gets ``adjustment_visible`` False.

        The Audited column of an Account Group line also carries the
        closing amount that the closing lines of the General Audit
        move into the group (see ``_get_closing_amount``). Total lines
        do not add it: their formulas already include the profit and
        loss groups that the closing empties, so adding it would count
        the profit twice. Without closing lines the amount is zero.

        When the General Audit has a usable KKA Worksheet (b26d482), the
        Audited column of the Account Group lines and of the Profit After
        Tax and Comprehensive Profit totals comes from it, see
        ``_get_lead_schedule_group_amount``; the other columns and totals
        stay on the General Audit details. Without a Worksheet the
        computation above applies unchanged.

        Reading the formula table is not itself a reactive dependency
        of this compute: editing
        ``general_audit_ws_ff42fdc.total_formula`` does not
        recompute worksheets that already exist. Applying an edited
        formula to an existing worksheet requires the user to press
        "Reload" (``action_load_posture``), the same way other
        adjustment data already requires a reload.

        :return: nothing; assigns ``unaudited``, ``adjustment_debit``,
            ``adjustment_credit``, ``adjustment_visible``, ``audited``,
            and ``previous``
        """
        formula_model = self.env["general_audit_ws_ff42fdc.total_formula"]
        for record in self:
            result_unaudited = 0.0
            result_adjustment_debit = 0.0
            result_adjustment_credit = 0.0
            result_audited = 0.0
            result_previous = 0.0
            result_adjustment_visible = True
            general_audit = record.worksheet_id.general_audit_id
            all_details = general_audit.detail_ids
            lead_schedule = record._get_lead_schedule_worksheet(general_audit)
            if record.line_type == "group" and record.group_id:
                details = all_details.filtered(
                    lambda d: d.account_id.group_id == record.group_id
                )
                result_unaudited = sum(details.mapped("home_statement_balance"))
                result_adjustment_debit = sum(details.mapped("adjustment_debit"))
                result_adjustment_credit = sum(details.mapped("adjustment_credit"))
                if lead_schedule:
                    result_audited = record._get_lead_schedule_group_amount(
                        lead_schedule, record.group_id
                    )
                else:
                    result_audited = sum(details.mapped("audited_balance"))
                    result_audited += record._get_closing_amount(
                        general_audit, record.group_id
                    )
                result_previous = sum(details.mapped("previous_balance"))
            elif record.line_type == "total" and record.total_type:
                formula_lines = formula_model.search(
                    [("total_type", "=", record.total_type)]
                )
                layout_line = (
                    self.env["general_audit_ws_ff42fdc.layout_line"]
                    .sudo()
                    .search(
                        [
                            ("line_type", "=", "total"),
                            ("total_type", "=", record.total_type),
                        ],
                        limit=1,
                    )
                )
                result_adjustment_visible = (
                    layout_line.show_adjustment if layout_line else True
                )
                for formula_line in formula_lines:
                    sign = 1 if formula_line.sign == "add" else -1
                    group = formula_line.group_id
                    group_details = all_details.filtered(
                        lambda d, group=group: d.account_id.group_id == group
                    )
                    result_unaudited += sign * sum(
                        group_details.mapped("home_statement_balance")
                    )
                    if result_adjustment_visible:
                        result_adjustment_debit += sum(
                            group_details.mapped("adjustment_debit")
                        )
                        result_adjustment_credit += sum(
                            group_details.mapped("adjustment_credit")
                        )
                    result_audited += sign * sum(
                        group_details.mapped("audited_balance")
                    )
                    result_previous += sign * sum(
                        group_details.mapped("previous_balance")
                    )
                if lead_schedule and record.total_type == "profit_after_tax":
                    result_audited = lead_schedule.net_current_profit
                elif lead_schedule and record.total_type == "comprehensive_profit":
                    result_audited = (
                        lead_schedule.net_current_profit + lead_schedule.net_oci
                    )
            record.unaudited = result_unaudited
            record.adjustment_debit = result_adjustment_debit
            record.adjustment_credit = result_adjustment_credit
            record.audited = result_audited
            record.previous = result_previous
            record.adjustment_visible = result_adjustment_visible

    @api.model
    def _get_lead_schedule_worksheet(self, general_audit):
        """Find the KKA Worksheet (b26d482) the Audited column reads from.

        It is the newest Worksheet of the General Audit that is neither
        cancelled nor rejected and has detail lines.

        :param general_audit: ``general_audit`` record being reported
        :return: ``general_audit_ws_b26d482`` record, empty when the
            audit has no usable Worksheet
        :rtype: recordset
        """
        return (
            self.env["general_audit_ws_b26d482"]
            .sudo()
            .search(
                [
                    ("general_audit_id", "=", general_audit.id),
                    ("state", "not in", ("cancel", "reject")),
                    ("detail_ids", "!=", False),
                ],
                order="id desc",
                limit=1,
            )
        )

    @api.model
    def _get_lead_schedule_group_amount(self, worksheet, group):
        """Get the Audited amount of an account group from the Worksheet.

        An Asset, Liability or Equity group sums the Balance Sheet column
        of its Worksheet lines, plus the closing of the types that no
        account receives and that land in the group. A Profit and Loss
        group sums the Current Profit column and an Other Comprehensive
        Income group the OCI column. The Worksheet shows each line
        positive on the normal balance side of its account.

        :param worksheet: ``general_audit_ws_b26d482`` record
        :param group: ``client_account_group`` record of the line
        :return: Audited amount of the group
        :rtype: float
        """
        details = worksheet.detail_ids.filtered(
            lambda d: d.account_id.group_id == group
        )
        category = group.report_category
        if category == "profit_loss":
            return sum(details.mapped("current_profit"))
        if category == "oci":
            return sum(details.mapped("oci"))
        result = sum(details.mapped("balance_sheet"))
        receivers = worksheet._get_closing_allocation()[0]
        lines = worksheet.general_audit_id.closing_line_ids.filtered(
            lambda line: not line.account_id
            and line.account_group_id == group
            and line.account_type_id.id not in receivers
        )
        for line in lines:
            if line.account_type_id.normal_balance == "cr":
                result += line.credit - line.debit
            else:
                result += line.debit - line.credit
        return result

    @api.model
    def _get_closing_amount(self, general_audit, group):
        """Get the closing amount that lands in an account group.

        Only the destination lines of the closing journal count, that
        is the lines without an account. The lines of the closed source
        accounts are left out, so the source groups keep their audited
        balance. Each line is signed on the normal balance side of its
        account type, like ``audited_balance``.

        :param general_audit: ``general_audit`` record being reported
        :param group: ``client_account_group`` record of the line
        :return: closing amount of the group, zero when the closing
            lines were not generated
        :rtype: float
        """
        result = 0.0
        lines = general_audit.closing_line_ids.filtered(
            lambda line: not line.account_id and line.account_group_id == group
        )
        for line in lines:
            if line.account_type_id.normal_balance == "cr":
                result += line.credit - line.debit
            else:
                result += line.debit - line.credit
        return result

    def _posture_line_order_key(self):
        """Return the key this line is looked up by in the layout table.

        Used by ``general_audit_ws_ff42fdc._resequence_posture_lines``
        to match this line against the layout lines.

        :return: a ``(line_type, code)`` tuple, where ``code`` is
            ``group_id.code`` for Account Group lines and
            ``total_type`` for Total lines
        """
        self.ensure_one()
        if self.line_type == "group":
            return ("group", self.group_id.code)
        return ("total", self.total_type)

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
