# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditClosingLine(models.Model):
    """General Audit Closing Line.

    One line of the closing journal of a General Audit. Lines are
    created by ``general_audit._generate_closing_lines`` from the
    mappings of the audit closing type: one line per closed account
    and one line with the net amount on the destination account type.
    """

    _name = "general_audit.closing_line"
    _description = "General Audit Closing Line"
    _order = "general_audit_id, sequence, id"

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        required=True,
        ondelete="cascade",
        help="General Audit document that owns this closing line.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        required=True,
        help="Ordering number of the closing line.",
    )
    mapping_id = fields.Many2one(
        string="Mapping",
        comodel_name="general_audit_closing_type.mapping",
        ondelete="set null",
        help="Mapping that produced this closing line.",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="client_account",
        ondelete="restrict",
        help="Client account closed by this line. Empty on the line that "
        "receives the net closing amount.",
    )
    account_type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        ondelete="restrict",
        help="Account type of the closed account, or the destination "
        "account type on the line that receives the net amount.",
    )
    account_group_id = fields.Many2one(
        string="Account Group",
        comodel_name="client_account_group",
        related="account_type_id.group_id",
        store=True,
        compute_sudo=True,
        help="Account group of the account type of this line.",
    )
    name = fields.Char(
        string="Label",
        help="Label of the closing line, taken from the mapping description.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="general_audit_id.partner_id",
        store=True,
        compute_sudo=True,
        help="Client of the General Audit.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        store=True,
        compute_sudo=True,
        help="Currency of the General Audit.",
    )
    debit = fields.Monetary(
        string="Debit",
        currency_field="currency_id",
        default=0.0,
        help="Debit amount of the closing line.",
    )
    credit = fields.Monetary(
        string="Credit",
        currency_field="currency_id",
        default=0.0,
        help="Credit amount of the closing line.",
    )
