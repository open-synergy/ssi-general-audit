# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc40cfd9(models.Model):
    """WS: Related Party Transaction (c40cfd9) — ISA 550.

    This worksheet documents the identification and evaluation of related party
    transactions in accordance with ISA 550 (Related Parties). The auditor records
    identified related parties, describes their transactions with the audit client,
    and tracks confirmation procedures performed to obtain sufficient appropriate
    evidence.

    Key components include a related party identification table and a confirmation
    procedure checklist, enabling systematic documentation of the auditor's work
    on related party disclosures and transactions.
    """

    _name = "general_audit_ws_c40cfd9"
    _description = "Related Party Transaction (c40cfd9)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_specific_procedure." "worksheet_type_c40cfd9"
    )

    confirmation_procedure_line_ids = fields.One2many(
        comodel_name="general_audit_ws_c40cfd9.confirmation_procedure",
        inverse_name="worksheet_id",
        string="Confirmation Procedures",
        help="List of confirmation procedures related to this worksheet.",
        readonly=True,
        states={"draft": [("readonly", False)], "open": [("readonly", False)]},
    )
    ws_ae11f7e_id = fields.Many2one(
        comodel_name="general_audit_ws_ae11f7e",
        string="Understanding of the Entity Worksheet",
        help=(
            "Reference to the 'Understanding of the Entity' worksheet "
            "from which related party information is sourced."
        ),
        required=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    related_party_line_ids = fields.One2many(
        comodel_name="general_audit_ws_c40cfd9.related_party",
        inverse_name="worksheet_id",
        string="Related Parties",
        help="List of related parties associated with this worksheet.",
        readonly=True,
        states={"open": [("readonly", False)]},
    )

    def onchange_ws_ae11f7e_id(self):
        self.ws_ae11f7e_id = False

    def action_load_related_party(self):
        for record in self.sudo():
            record._load_related_party()

    def action_load_confirmation_procedure(self):
        for record in self.sudo():
            record._load_confirmation_procedure()

    def _load_related_party(self):
        self.ensure_one()

        self.related_party_line_ids.unlink()

        for related_party in self.ws_ae11f7e_id.related_party_ids:
            self.env["general_audit_ws_c40cfd9.related_party"].create(
                {
                    "worksheet_id": self.id,
                    "name": related_party.name,
                    "initial_relation": related_party.relation,
                    "initial_related_account_type_ids": [
                        (6, 0, related_party.related_account_type_ids.ids)
                    ],
                    "final_relation": related_party.relation,
                    "final_related_account_type_ids": [
                        (6, 0, related_party.related_account_type_ids.ids)
                    ],
                }
            )

    def _load_confirmation_procedure(self):
        self.ensure_one()

        all_procedures = self.env[
            "general_audit_related_party_confirmation_procedure"
        ].search([])
        existing_procedures = self.confirmation_procedure_line_ids.mapped(
            "confirmation_procedure_id"
        )

        to_add = all_procedures - existing_procedures
        to_remove = existing_procedures - all_procedures

        # Add new procedures
        for procedure in to_add:
            self.env["general_audit_ws_c40cfd9.confirmation_procedure"].create(
                {
                    "worksheet_id": self.id,
                    "confirmation_procedure_id": procedure.id,
                }
            )

        # Remove obsolete procedures
        lines_to_remove = self.confirmation_procedure_line_ids.filtered(
            lambda line: line.confirmation_procedure_id in to_remove
        )
        if lines_to_remove:
            lines_to_remove.unlink()
