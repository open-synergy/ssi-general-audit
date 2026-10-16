# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GeneralAuditWsC3b9e71IndividualLine(models.Model):
    """Individual analysis line of the Uncorrected AJE Analysis worksheet.

    One line per account group that has uncorrected misstatements. It
    repeats the quantitative factors of the group line and holds the
    qualitative assessment, the preliminary conclusion and the follow-up
    of the auditor for that group.
    """

    _name = "general_audit_ws_c3b9e71.individual_line"
    _description = "Uncorrected AJE Analysis (c3b9e71) - Individual Line"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_c3b9e71",
        required=True,
        ondelete="cascade",
        help="Uncorrected AJE Analysis worksheet that owns this line.",
    )
    group_id = fields.Many2one(
        string="Account Group",
        comodel_name="client_account_group",
        required=True,
        ondelete="restrict",
        help="Account group analysed by this line. Only groups with "
        "uncorrected misstatements are offered.",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="group_id.sequence",
        store=True,
        help="Display order inherited from the account group.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="worksheet_id.currency_id",
        store=True,
        help="Currency of the amounts, inherited from the worksheet.",
    )
    uncorrected_amount = fields.Monetary(
        string="Uncorrected Misstatement",
        currency_field="currency_id",
        compute="_compute_quantitative",
        store=True,
        compute_sudo=True,
        help="Uncorrected misstatement of the account group, read from "
        "the group lines of the worksheet.",
    )
    pct_of_balance = fields.Float(
        string="% of Group Balance",
        compute="_compute_quantitative",
        store=True,
        compute_sudo=True,
        help="Uncorrected misstatement divided by the audited balance of " "the group.",
    )
    pct_of_pm = fields.Float(
        string="% of Performance Materiality",
        compute="_compute_quantitative",
        store=True,
        compute_sudo=True,
        help="Uncorrected misstatement divided by Performance Materiality.",
    )
    qualitative_profit_loss = fields.Text(
        string="Impact on Profit or Loss",
        help="Qualitative assessment of the effect on profit or loss.",
    )
    qualitative_financial_position = fields.Text(
        string="Impact on the Statement of Financial Position",
        help="Qualitative assessment of the effect on the statement of "
        "financial position.",
    )
    qualitative_users = fields.Text(
        string="Impact on Users of Financial Statements",
        help="Qualitative assessment of the effect on the users of the "
        "financial statements.",
    )
    qualitative_other = fields.Text(
        string="Other Qualitative Factor",
        help="Any other qualitative factor to consider.",
    )
    preliminary_conclusion = fields.Text(
        string="Preliminary Conclusion",
        help="Preliminary conclusion of the auditor for this group.",
    )
    follow_up = fields.Text(
        string="Follow-up",
        help="Follow-up the auditor plans for this group.",
    )

    @api.depends(
        "group_id",
        "worksheet_id.group_line_ids.group_id",
        "worksheet_id.group_line_ids.uncorrected_amount",
        "worksheet_id.group_line_ids.pct_of_balance",
        "worksheet_id.group_line_ids.pct_of_pm",
    )
    def _compute_quantitative(self):
        """Copy the quantitative factors from the group line of the group.

        All three factors are zero when the worksheet has no group line
        for the account group.

        :return: ``None``
        """
        for record in self:
            line = record.worksheet_id.group_line_ids.filtered(
                lambda x, group=record.group_id: x.group_id == group
            )[:1]
            record.uncorrected_amount = line.uncorrected_amount
            record.pct_of_balance = line.pct_of_balance
            record.pct_of_pm = line.pct_of_pm

    @api.constrains(
        "worksheet_id",
        "group_id",
    )
    def _check_unique_group(self):
        """Allow at most one individual line per account group.

        :return: ``None``
        :raises ValidationError: when another line of the same worksheet
            already analyses the account group
        """
        for record in self:
            duplicate = self.search_count(
                [
                    ("worksheet_id", "=", record.worksheet_id.id),
                    ("group_id", "=", record.group_id.id),
                    ("id", "!=", record.id),
                ]
            )
            if duplicate:
                msg = _(
                    "Context: Save individual analysis line\n"
                    "Database ID: %s\n"
                    "Problem: Account group '%s' already has an individual "
                    "analysis line in this worksheet\n"
                    "Solution: Edit the existing line instead of adding "
                    "another one"
                ) % (record.id, record.group_id.display_name)
                raise ValidationError(msg)
