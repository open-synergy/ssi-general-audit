# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GeneralAuditDataCollection(models.Model):
    """Master: Data Collection.

    Defines an item of data that the engagement team collects from the
    client. An item of type Account Type belongs to one client account type
    and fills the Details tab of the Data Collection worksheet; an item of
    type Others is not tied to an account type and fills the Others tab.
    """

    _name = "general_audit_data_collection"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Data Collection"

    type = fields.Selection(
        string="Type",
        selection=[
            ("account_type", "Account Type"),
            ("others", "Others"),
        ],
        required=True,
        default="account_type",
        help=(
            "Account Type: the item belongs to one client account type. "
            "Others: the item is not tied to an account type."
        ),
    )
    account_type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        ondelete="restrict",
        help=(
            "Client account type this item belongs to. Required when the "
            "type is Account Type; not used when the type is Others."
        ),
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_data_collection_category",
        required=True,
        ondelete="restrict",
        help="Category used to classify this data collection item.",
    )

    @api.constrains("type", "account_type_id")
    def _check_account_type_required(self):
        """Require an account type on items of type Account Type.

        :raises ValidationError: if an item of type Account Type has no
            account type.
        """
        for record in self:
            if record.type == "account_type" and not record.account_type_id:
                raise ValidationError(
                    _("Account Type is required when the type is Account Type.")
                )

    @api.onchange("type")
    def onchange_account_type_id(self):
        """Clear the account type when the type is not Account Type."""
        if self.type != "account_type":
            self.account_type_id = False
