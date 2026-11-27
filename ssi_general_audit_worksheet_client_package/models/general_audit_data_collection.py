# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GeneralAuditDataCollection(models.Model):
    """Master: Data Collection.

    Defines an item of data that the engagement team collects from the
    client. An item of type Account Type belongs to one client account type
    and fills the Details tab of the Data Collection worksheet; an item of
    type Permanent File or Current File is not tied to an account type and
    fills the Permanent/Current tab. An item of type Primary has no account type and
    no category, and fills the Primary tab.
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
            ("permanent_file", "Permanent File"),
            ("current_file", "Current File"),
            ("primary", "Primary"),
        ],
        required=True,
        default="account_type",
        help=(
            "Account Type: the item belongs to one client account type. "
            "Permanent File and Current File: the item is not tied to an "
            "account type. Primary: the item has neither an account type "
            "nor a category."
        ),
    )
    account_type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        index=True,
        ondelete="restrict",
        help=(
            "Client account type this item belongs to. Required when the "
            "type is Account Type; not used for the other types."
        ),
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_data_collection_category",
        ondelete="restrict",
        help=(
            "Category used to classify this data collection item. Required "
            "unless the type is Primary."
        ),
    )

    code_sort = fields.Char(
        string="Code Sort Key",
        compute="_compute_code_sort",
        store=True,
        help=(
            "Type rank followed by the code with every number padded with "
            "zeros, so that the items are sorted by type first (Permanent "
            "File before Current File) and then by their number (AT-2 "
            "before AT-10)."
        ),
    )

    @api.depends("code", "type")
    def _compute_code_sort(self):
        """Prefix the padded code with the rank of the item type.

        Permanent File ranks before Current File. The Account Type and
        Primary ranks are arbitrary: those items never share a list with
        the others.
        """
        type_rank = {
            "account_type": "0",
            "permanent_file": "1",
            "current_file": "2",
            "primary": "3",
        }
        for record in self:
            result = re.sub(
                r"\d+", lambda match: match.group().zfill(8), record.code or ""
            )
            record.code_sort = type_rank.get(record.type, "9") + result

    def name_get(self):
        """Show only the code when the context asks for it.

        :return: list of ``(id, display name)`` pairs
        :rtype: list
        """
        if self.env.context.get("data_collection_code_only"):
            return [(record.id, record.code) for record in self]
        return super().name_get()

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

    @api.constrains("type", "category_id")
    def _check_category_required(self):
        """Require a category on items that are not of type Primary.

        :raises ValidationError: if an item of another type than Primary
            has no category.
        """
        for record in self:
            if record.type != "primary" and not record.category_id:
                raise ValidationError(
                    _("Category is required when the type is not Primary.")
                )

    @api.onchange("type")
    def onchange_account_type_id(self):
        """Clear the account type when the type is not Account Type."""
        if self.type != "account_type":
            self.account_type_id = False

    @api.onchange("type")
    def onchange_category_id(self):
        """Clear the category when the type is Primary."""
        if self.type == "primary":
            self.category_id = False
