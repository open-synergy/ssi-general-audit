# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsB555eddDetail(models.Model):
    """Report Formatting Control (b555edd) - one standard account type line.

    Mirrors one ``general_audit.standard_detail`` of the parent General
    Audit: the account type, its group and the audited balances of the
    current and the previous period. Lines are created by the parent
    worksheet's ``action_reload_account`` and are never typed in.
    """

    _name = "general_audit_ws_b555edd.detail"
    _description = "Report Formatting Control (b555edd) - Detail"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_b555edd",
        string="# Worksheet",
        required=True,
        ondelete="cascade",
        help="Report Formatting Control worksheet this line belongs to.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="worksheet_id.general_audit_id.currency_id",
        store=True,
        help="Currency of the amounts; taken from the General Audit.",
    )
    standard_detail_id = fields.Many2one(
        string="# Standard Detail",
        comodel_name="general_audit.standard_detail",
        required=True,
        ondelete="restrict",
        help="Standard account type line of the General Audit.",
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        related="standard_detail_id.type_id",
        store=True,
        readonly=True,
        help="Standard account type reported on this line.",
    )
    group_id = fields.Many2one(
        string="Account Group",
        comodel_name="client_account_group",
        related="standard_detail_id.type_id.group_id",
        store=True,
        readonly=True,
        help="Account group; decides which statement tab shows this line.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        help="Display order: account group sequence, then type sequence.",
    )
    current_balance = fields.Monetary(
        string="Current Balance",
        related="standard_detail_id.audited_balance",
        store=True,
        readonly=True,
        currency_field="currency_id",
        help="Audited balance of the current period.",
    )
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="standard_detail_id.previous_balance",
        store=True,
        readonly=True,
        currency_field="currency_id",
        help="Balance of the previous period.",
    )
