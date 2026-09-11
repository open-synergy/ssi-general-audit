# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa025441(models.Model):
    """
    WS: Financial Statement Disclosure Checklist (a025441) — ISA 700 / SA 700.

    The auditor completes the Yes / No / N-A disclosure checklist for the
    applicable financial reporting framework (e.g. IFRS, PSAK Umum, PSAK
    ETAP) outside Odoo (e.g. in a spreadsheet), then pastes the completed
    checklist as CSV into ``raw_data``.  This avoids maintaining master
    data for the thousands of disclosure items that PSAK Umum/IFRS
    (± 4000 items) or PSAK ETAP (± 600 items) require.

    The overall completeness assessment and narrative conclusion are not
    declared here: ``conclusion_id`` and ``conclusion`` are already
    provided generically by ``general_audit_worksheet`` (inherited via
    ``general_audit_worksheet_mixin``), and master data for
    ``conclusion_id`` covering this worksheet type already includes
    Complete/Incomplete-equivalent options.
    """

    _name = "general_audit_ws_a025441"
    _description = "Financial Statement Disclosure (a025441)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_review." "worksheet_type_a025441"

    raw_data = fields.Text(
        string="Raw Data",
        required=False,
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Raw data in CSV format containing the completed financial "
        "statement disclosure checklist (item, source standard, note, "
        "and Yes/No/N-A status per row).",
    )
