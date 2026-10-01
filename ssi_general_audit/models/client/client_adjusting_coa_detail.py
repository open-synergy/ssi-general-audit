# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ClientAdjustingCoaDetail(models.Model):
    """Line of an Adjusting CoA document.

    Describes one account that does not exist yet in the client's chart
    of accounts. ``account_id`` stays empty until the parent document
    reaches ``done``, when the account is created and stored here.
    """

    _name = "client_adjusting_coa.detail"
    _description = "Accountant Client Adjusting CoA Detail"
    _order = "coa_id, code, id"

    coa_id = fields.Many2one(
        string="# Adjusting CoA",
        comodel_name="client_adjusting_coa",
        required=True,
        ondelete="cascade",
        help="Parent Adjusting CoA document this line belongs to.",
    )
    code = fields.Char(
        string="Code",
        required=True,
        help="Code of the new account. Must be unique for the client.",
    )
    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the new account.",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="client_account_type",
        required=True,
        ondelete="restrict",
        help="Account type of the new account. Must belong to the account "
        "type set of the audit.",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="client_account",
        readonly=True,
        copy=False,
        ondelete="restrict",
        help="Client account created when the document is done.",
    )

    def _prepare_account_data(self):
        """Build the ``client_account`` values for this line.

        Extension point: override in a glue module to add fields.

        :return: dict of ``client_account`` values
        """
        self.ensure_one()
        return {
            "partner_id": self.coa_id.partner_id.id,
            "code": self.code,
            "name": self.name,
            "type_id": self.type_id.id,
        }
