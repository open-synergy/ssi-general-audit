# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc40cfd9RelatedParty(models.Model):
    _name = "general_audit_ws_c40cfd9.related_party"
    _description = "Related Party Transaction (c40cfd9) - Related Party"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_c40cfd9",
        string="Worksheet",
        required=True,
        ondelete="cascade",
    )
    name = fields.Char(
        required=True,
        help="Related party name.",
    )
    initial_relation = fields.Char(
        required=True,
        help=(
            "Nature of relationship with the entity (e.g., subsidiary, shareholder, "
            "key management) (initial)."
        ),
        readonly=True,
    )
    initial_related_account_type_ids = fields.Many2many(
        string="Initial Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_ws_c40cfd9_related_party_2_initial_account_type",
        column1="detail_id",
        column2="type_id",
        required=True,
        help=(
            "Standard account types impacted by transactions with this related party (initial)."
        ),
        readonly=True,
    )
    final_relation = fields.Char(
        required=True,
        help=(
            "Nature of relationship with the entity (e.g., subsidiary, shareholder, "
            "key management) (final)."
        ),
    )
    final_related_account_type_ids = fields.Many2many(
        string="Final Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_ws_c40cfd9_related_party_2_final_account_type",
        column1="detail_id",
        column2="type_id",
        required=True,
        help=(
            "Standard account types impacted by transactions with this related party (final)."
        ),
    )
    conclusion = fields.Text(
        string="Conclusion",
        help="Conclusion regarding transactions with this related party.",
    )
