# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditWSb66777d(models.Model):
    """
    WS.090.2 — Independent Auditor's Report (b66777d)

    Serves as the working-paper record for drafting and reviewing the
    **independent auditor's report** issued to the client's shareholders
    or other intended users.  The report is the primary means by which
    the auditor communicates the results of the engagement.  As required
    by ISA 700 / SA 700, the report must include:

    - A title clearly indicating it is the independent auditor's report.
    - The appropriate opinion (unmodified, qualified, adverse, or
      disclaimer) on the financial statements.
    - Basis for opinion paragraph.
    - Key Audit Matters section (where applicable under ISA 701 / SA 701).
    - Other reporting responsibilities.

    Under ISA 705 / SA 705 the form of the opinion may be modified; under
    ISA 706 / SA 706 emphasis-of-matter or other-matter paragraphs may be
    added.

    **ISA / SA references:** ISA 700 / SA 700 — Forming an Opinion and
    Reporting on Financial Statements; ISA 701 / SA 701 — Key Audit
    Matters; ISA 705 / SA 705 — Modifications to the Opinion;
    ISA 706 / SA 706 — Emphasis-of-Matter and Other-Matter Paragraphs
    """

    _name = "general_audit_ws_b66777d"
    _description = "Independen Auditor Report (b66777d)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_final_report." "worksheet_type_b66777d"
