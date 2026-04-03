# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSff42fdc(models.Model):
    """Worksheet — Audit Result / Opinion Formalisation (ff42fdc).

    Records and formalises the final audit opinion for the engagement:
    * ``financial_statement_opinion_id`` — the type of opinion issued
      (e.g., Unmodified, Qualified, Adverse, Disclaimer), linked to and
      stored back on the General Audit record.
    * ``financial_statement_opinion_date`` — the date of the opinion,
      also synchronised with the General Audit record.

    This worksheet provides the definitive audit-file record of the opinion
    and serves as evidence that the engagement-level decision was made and
    documented in accordance with ISA 700 / SA 700.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 700/SA 700 (Forming an Opinion);
    ISA 705/SA 705 (Modifications to the Opinion).
    """

    _name = "general_audit_ws_ff42fdc"
    _description = "Audit Result (ff42fdc)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_draft_reporting." "worksheet_type_ff42fdc"
    )

    financial_statement_opinion_id = fields.Many2one(
        comodel_name="accountant.opinion",
        string="Opinion on Financial Statement",
        related="general_audit_id.opinion_id",
        store=True,
        readonly=False,
        states={
            "open": [("readonly", False)],
        },
    )
    financial_statement_opinion_date = fields.Date(
        string="Date of Opinion on Financial Statement",
        related="general_audit_id.opinion_date",
        store=True,
        readonly=False,
        states={
            "open": [("readonly", False)],
        },
    )
