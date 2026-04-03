# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditWSb555edd(models.Model):
    """Worksheet — Report Formatting Control (b555edd).

    A quality-control worksheet for reviewing the formatting, grammar,
    consistency, and presentation quality of the draft auditor's report
    before partner sign-off and issuance.  Ensures the report meets the
    firm's style and quality standards.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 700/SA 700 (Forming an Opinion and Reporting).
    """

    _name = "general_audit_ws_b555edd"
    _description = "Report Formatting Control (b555edd)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_draft_reporting." "worksheet_type_b555edd"
    )
