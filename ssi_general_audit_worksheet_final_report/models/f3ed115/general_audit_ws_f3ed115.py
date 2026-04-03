# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditWSf3ed115(models.Model):
    """
    WS.090.3 — Audit Report (f3ed115)

    Represents the internal **audit report** document used within the
    audit firm to record the complete audit opinion and supporting
    narrative before the final independent auditor's report is issued
    to the client.  This worksheet acts as the engagement-level
    repository for the opinion type, the basis for the opinion, and
    all additional paragraphs (key audit matters, emphasis of matter,
    other matter) that will appear in the final report.

    The distinction from WS.090.2 (Independent Auditor's Report) is
    that this record represents the internal draft/sign-off view,
    while WS.090.2 represents the final client-facing document.

    **ISA / SA references:** ISA 700 / SA 700 — Forming an Opinion and
    Reporting on Financial Statements; ISA 705 / SA 705 — Modifications
    to the Opinion in the Independent Auditor's Report
    """

    _name = "general_audit_ws_f3ed115"
    _description = "Audit Report (f3ed115)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_final_report." "worksheet_type_f3ed115"
