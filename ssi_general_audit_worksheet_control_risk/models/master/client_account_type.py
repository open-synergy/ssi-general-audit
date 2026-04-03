# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ClientAccountType(models.Model):
    """Extension of the Client Account Type model for Control Risk data.

    Adds ``account_key_internal_control_ids`` to the standard account type,
    linking the account type to its applicable key internal controls for
    significant accounts.  Used in the Significant Account Internal Control
    worksheet (ba9b2f0) to filter controls relevant to the selected account.
    """

    _name = "client_account_type"
    _inherit = ["client_account_type"]

    account_key_internal_control_ids = fields.Many2many(
        string="Significant Account Key Internal COntrols",
        comodel_name="general_audit_account_key_internal_control",
        relation="rel_account_key_internal_control_2_standard_account",
        column1="standard_account_id",
        column2="key_internal_control_id",
        help=(
            "Key internal controls applicable to this standard account type for "
            "significant accounts."
        ),
    )
