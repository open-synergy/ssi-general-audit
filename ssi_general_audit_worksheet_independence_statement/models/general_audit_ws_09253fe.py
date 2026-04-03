# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS09253fe(models.Model):
    """
    WS.020.1 — Independence Statement (09253fe)

    Documents the **independence assessment and confirmation checklist**
    for the engagement team as required by ISA 200 / SA 200
    (Overall Objectives of the Independent Auditor) and the
    International Ethics Standards Board for Accountants (IESBA) Code
    of Ethics (as adopted in Indonesian audit standards).

    Professional independence is a fundamental requirement for all audit
    engagements.  Before commencing work, each engagement team member
    must evaluate and confirm the absence of:

    - Financial or business relationships with the client.
    - Family or personal relationships that impair independence.
    - Non-audit services that threaten independence.
    - Advocacy, intimidation, self-review, or other identified threats.

    This checklist worksheet systematically captures Yes / No / N-A
    responses for each independence requirement, ensuring that the
    engagement team's independence is formally assessed and documented
    before and during the engagement.

    **ISA / SA references:** ISA 200 / SA 200 — Overall Objectives of
    the Independent Auditor and the Conduct of an Audit in Accordance
    with International Standards on Auditing; IESBA Code of Ethics
    """

    _name = "general_audit_ws_09253fe"
    _description = "Independence Letter (09253fe)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_independence_statement." "worksheet_type_09253fe"
    )
    _checklist_model_name = "general_audit_ws_09253fe.checklist"
    _item_model_name = "general_audit_ws_09253fe.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_09253fe.checklist",
        help="""Checklist lines associated with this worksheet.
Each line captures the assessment/answer for a specific independence
statement checklist item.""",
    )
