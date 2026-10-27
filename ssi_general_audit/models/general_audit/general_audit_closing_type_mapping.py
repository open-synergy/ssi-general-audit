# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditClosingTypeMapping(models.Model):
    """General Audit Closing Type Mapping.

    One mapping produces a closing journal: every source account is
    closed on the opposite side and the net amount of the audited
    balances goes to the destination account type.
    """

    _name = "general_audit_closing_type.mapping"
    _description = "General Audit Closing Type Mapping"
    _order = "sequence, id"

    closing_type_id = fields.Many2one(
        string="Closing Type",
        comodel_name="general_audit_closing_type",
        required=True,
        ondelete="cascade",
        help="Closing type that owns this mapping.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        required=True,
        help="Ordering of the mapping and of the closing line it creates.",
    )
    name = fields.Char(
        string="Description",
        required=True,
        help="Description of the mapping. Used as the closing line label.",
    )
    source_type_ids = fields.Many2many(
        string="Source Account Type(s)",
        comodel_name="client_account_type",
        relation="rel_ga_closing_mapping_2_account_type",
        column1="mapping_id",
        column2="type_id",
        required=True,
        help="Account types whose audited balances are closed.",
    )
    account_type_id = fields.Many2one(
        string="Destination Account Type",
        comodel_name="client_account_type",
        required=True,
        ondelete="restrict",
        help="Account type that receives the closing amount.",
    )

    def _get_closing_details(self, general_audit):
        """Get the audit account lines covered by the source types.

        :param general_audit: ``general_audit`` record being closed
        :return: ``general_audit.detail`` records whose account type is
            one of the source account types
        :rtype: recordset
        """
        self.ensure_one()
        return general_audit.detail_ids.filtered(
            lambda d: d.type_id in self.source_type_ids
        )

    def _get_closing_balance(self, detail):
        """Get the audited balance of an account in credit-positive sign.

        :param detail: ``general_audit.detail`` record of the account
        :return: audited balance, positive for credit and negative for
            debit
        :rtype: float
        """
        if detail.account_id.normal_balance == "cr":
            return detail.audited_balance
        return -detail.audited_balance

    def _compute_closing_amount(self, general_audit):
        """Compute the closing amount of this mapping for an audit.

        Sums the audited balance of the audit accounts whose type is
        one of the source types. An account with credit normal balance adds
        its balance, an account with debit normal balance subtracts it.

        :param general_audit: ``general_audit`` record being closed
        :return: net amount, positive for credit and negative for debit
        :rtype: float
        """
        self.ensure_one()
        return sum(
            self._get_closing_balance(detail)
            for detail in self._get_closing_details(general_audit)
        )
