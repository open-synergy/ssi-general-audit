# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSAE11F7EOtherEvidence(models.Model):
    """Other audit evidence record within the Main Business Activity worksheet.

    Records additional audit evidence obtained from external sources (e.g.,
    analyst reports, industry studies, third-party confirmations) that support
    the auditor's understanding of the entity. Per ISA 500 / SA 500, auditors
    must gather sufficient appropriate evidence; this model tracks non-standard
    evidence items beyond the primary audit procedures.
    """

    _name = "general_audit_ws_ae11f7e.other_evidence"
    _description = "Worksheet ae11f7e - Other Evidence"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae11f7e",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This entry will be removed if the worksheet is deleted."
        ),
    )
    evidence_id = fields.Many2one(
        string="Evidence",
        comodel_name="general_audit_evidence",
        required=True,
        help=(
            "Reference to the audit evidence that supports this entry. "
            "Select the appropriate evidence record from the repository."
        ),
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        help=(
            "Reference to the business partner associated with this evidence item. "
            "Select the appropriate partner record."
        ),
    )
    partner_name = fields.Char(
        required=True,
        help=(
            "Denormalized name of the associated partner, stored for reporting "
            "and audit trail purposes. Automatically populated when a partner is "
            "selected and may be adjusted if necessary."
        ),
    )
    summary = fields.Text(
        required=True,
        help=(
            "Concise narrative describing the other evidence and its relevance to "
            "the worksheet. Provide sufficient detail to support audit conclusions."
        ),
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_ae11f7e_evidence_2_account_type",
        column1="prev_audit_id",
        column2="type_id",
        required=True,
        help=(
            "Standard account types related to this item. Used to link the entry to "
            "relevant accounts."
        ),
    )

    @api.onchange(
        "partner_id",
    )
    def onchange_partner_name(self):
        self.partner_name = ""
        if self.partner_id:
            self.partner_name = self.partner_id.name
