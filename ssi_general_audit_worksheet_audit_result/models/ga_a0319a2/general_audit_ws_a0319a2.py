# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSa0319a2(models.Model):
    """Worksheet WR.110.1 — Findings That Influence Opinion.

    Records audit findings (misstatements or conditions) discovered during
    fieldwork that may affect the type of audit opinion to be issued.
    Each finding is documented in the standard 5-C format (Condition, Criteria,
    Cause, Effect, Recommendation) and classified by risk severity (major/minor).

    Under ISA 450 / SA 450, the auditor accumulates identified misstatements —
    factual, judgemental, and projected — and evaluates whether uncorrected
    misstatements, individually or in aggregate, are material to the financial
    statements.  This worksheet is the primary register for such misstatements
    that require management attention and/or disclosure in the auditor's report.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 450/SA 450 (Evaluation of Misstatements);
    ISA 700/SA 700 (Forming an Opinion).
    """

    _name = "general_audit_ws_a0319a2"
    _description = "Findings That Influence Opinion (a0319a2)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_audit_result." "worksheet_type_a0319a2"

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_a0319a2.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help=(
            "List of detail lines that capture findings influencing the audit opinion. "
            "Editable when the worksheet is in the 'Open' state."
        ),
    )
