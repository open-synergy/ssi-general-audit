# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSAE11F7EPreviousAuditEvidence(models.Model):
    """Previous audit evidence carry-forward within the Main Business Activity worksheet.

    Records audit evidence from prior engagement periods that remains relevant
    to the current audit. Per ISA 315 (Revised), prior year information can be
    used as audit evidence if the auditor validates its continued reliability.
    This model links prior evidence records with account types to support
    risk carry-forward assessments.
    """

    _name = "general_audit_ws_ae11f7e.previous_audit_evidence"
    _description = "Worksheet ae11f7e - Previous Audit Evidence"
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
    summary = fields.Text(
        help=(
            "Brief, factual synopsis of the referenced evidence "
            "and its relevance to the current worksheet item. "
            "Include key observations and cross-references, if any."
        ),
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_ga_ws_ae11f7e_prev_audit_evidence_2_account_type",
        column1="prev_audit_id",
        column2="type_id",
        required=True,
        help=(
            "Standard account types related to this item. Used to link the entry to "
            "relevant accounts."
        ),
    )
