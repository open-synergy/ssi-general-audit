# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWsFf42fdcPosture(models.Model):
    """Worksheet (ff42fdc) - Posture Line.

    One record is created per ``client_account_group`` that has accounts
    used on the parent General Audit, aggregating the Unaudited,
    Adjustment (Debit/Credit), and Audited amounts of every
    ``general_audit.detail`` line whose account belongs to that group.

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
    group_id = fields.Many2one(
        comodel_name="client_account_group",
        string="Account Group",
        required=True,
        ondelete="restrict",
        help="Client account group summarised by this posture line.",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="group_id.sequence",
        store=True,
        help="Ordering inherited from the client account group.",
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
        help="Sum of End Period Balance for every account under this " "group.",
    )
    adjustment_debit = fields.Monetary(
        string="Adjustment (Debit)",
        currency_field="currency_id",
        compute="_compute_amounts",
        store=True,
        help="Sum of Adjustment Debit for every account under this " "group.",
    )
    adjustment_credit = fields.Monetary(
        string="Adjustment (Credit)",
        currency_field="currency_id",
        compute="_compute_amounts",
        store=True,
        help="Sum of Adjustment Credit for every account under this " "group.",
    )
    audited = fields.Monetary(
        string="Audited",
        currency_field="currency_id",
        compute="_compute_amounts",
        store=True,
        help="Sum of Audited Balance for every account under this " "group.",
    )

    @api.depends(
        "worksheet_id",
        "worksheet_id.general_audit_id.detail_ids.home_statement_balance",
        "worksheet_id.general_audit_id.detail_ids.adjustment_debit",
        "worksheet_id.general_audit_id.detail_ids.adjustment_credit",
        "worksheet_id.general_audit_id.detail_ids.audited_balance",
        "group_id",
    )
    def _compute_amounts(self):
        """Aggregate audit detail amounts for this line's account group.

        Filters the parent General Audit's ``detail_ids`` down to the
        lines whose ``account_id.group_id`` matches this line's
        ``group_id``, then sums their ``home_statement_balance``,
        ``adjustment_debit``, ``adjustment_credit``, and
        ``audited_balance`` into ``unaudited``, ``adjustment_debit``,
        ``adjustment_credit``, and ``audited`` respectively. The
        per-row ``audited_balance`` already accounts for the account's
        normal balance side, so it is summed directly without being
        recomputed here.
        """
        for record in self:
            record.unaudited = 0.0
            record.adjustment_debit = 0.0
            record.adjustment_credit = 0.0
            record.audited = 0.0
            if record.group_id:
                details = record.worksheet_id.general_audit_id.detail_ids.filtered(
                    lambda d: d.account_id.group_id == record.group_id
                )
                record.unaudited = sum(details.mapped("home_statement_balance"))
                record.adjustment_debit = sum(details.mapped("adjustment_debit"))
                record.adjustment_credit = sum(details.mapped("adjustment_credit"))
                record.audited = sum(details.mapped("audited_balance"))
