# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditWSa8c54f3(models.Model):
    """
    WS.090.1 — Audit Final Memorandum (a8c54f3)

    Documents the **audit final memorandum** — the engagement partner's
    formal summary at the close of fieldwork that brings together all key
    audit conclusions before the auditor's report is issued.  As required
    by ISA 220 / SA 220 (Quality Control for an Audit of Financial
    Statements) and ISA 700 / SA 700 (Forming an Opinion), the engagement
    partner must satisfy themselves that:

    - All significant risks and findings have been addressed.
    - The evidence obtained is sufficient and appropriate.
    - The conclusions on each significant area are reasonable and
      consistent with the financial statement as a whole.
    - The form of the auditor's report is appropriate.

    This worksheet captures the engagement partner's overall conclusion
    narrative and serves as the final sign-off document before issuing
    the auditor's report.

    **ISA / SA references:** ISA 220 / SA 220 — Quality Control for an
    Audit of Financial Statements; ISA 700 / SA 700 — Forming an Opinion
    and Reporting on Financial Statements
    """

    _name = "general_audit_ws_a8c54f3"
    _description = "Audit Final Memorandum (a8c54f3)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_final_report." "worksheet_type_a8c54f3"
