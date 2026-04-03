# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSb9d8a5cComptencyItem(models.Model):
    """Master data: Competency criterion for engagement team assessment.

    Defines a specific competency requirement or qualification that a team
    member must satisfy, used in the competency analysis section of the
    ``general_audit_ws_b9d8a5c`` worksheet. Inherits ``mixin.master_data``.

    Examples of items include: industry-specific knowledge, relevant
    certifications (CPA, CA), audit methodology proficiency, or regulatory
    expertise required for the engagement.

    Model: ``general_audit_ws_b9d8a5c.competency_item``
    SA Reference: SA 220, ISQC 1
    """

    _name = "general_audit_ws_b9d8a5c.competency_item"
    _inherit = [
        "mixin.master_data",
    ]
    _description = (
        "Competency, Availability and Independency "
        "Of Assignment Team (b9d8a5c) - Competency Item"
    )

    code = fields.Char(
        default="/",
    )
