# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AddClientAccountLine(models.TransientModel):
    """
    One account row typed in the ``add_client_account`` wizard.

    Holds the code, name and type of an account that does not exist
    yet; it is turned into a ``client_account`` when the wizard runs.
    """

    _name = "add_client_account_line"
    _description = "Add Client Account Line"

    wizard_id = fields.Many2one(
        string="# Wizard",
        comodel_name="add_client_account",
        required=True,
        ondelete="cascade",
        help="Parent wizard.",
    )
    code = fields.Char(
        string="Code",
        required=True,
        help="Account code, unique per client.",
    )
    name = fields.Char(
        string="Name",
        required=True,
        help="Account name.",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="client_account_type",
        required=True,
        help="Standard account type the new account is mapped to.",
    )
