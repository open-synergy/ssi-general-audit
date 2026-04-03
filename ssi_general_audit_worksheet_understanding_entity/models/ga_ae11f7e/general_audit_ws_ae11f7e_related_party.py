# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSAE11F7ERelatedParty(models.Model):
    """Related party entry within the Main Business Activity worksheet.

    Identifies related parties of the audit client (subsidiaries, associates,
    key management, shareholding entities) and the nature of their relationship.
    Per ISA 550 / SA 550, auditors must identify related parties and assess
    whether related party transactions are at arm's length and properly
    disclosed in the financial statements.
    """

    _name = "general_audit_ws_ae11f7e.related_party"
    _description = "Worksheet ae11f7e - Related Parties"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae11f7e",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This related party entry will be removed if the worksheet is deleted."
        ),
    )
    name = fields.Char(
        required=True,
        help="Related party name.",
    )
    relation = fields.Char(
        required=True,
        help=(
            "Nature of relationship with the entity (e.g., subsidiary, shareholder, "
            "key management)."
        ),
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_ae11f7e_related_party_2_account_type",
        column1="related_party_id",
        column2="type_id",
        required=True,
        help=(
            "Standard account types impacted by transactions with this related party."
        ),
    )
