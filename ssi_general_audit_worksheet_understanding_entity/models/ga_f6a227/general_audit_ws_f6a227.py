# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSf6a227(models.Model):
    """Worksheet: Understanding of Preparation of Financial Statements (f6a227) — RA.150.6.

    Documents the auditor's understanding of how the entity prepares its
    financial statements, in accordance with ISA 315 (Revised) / SA 315 and
    ISA 330 / SA 330 (Auditor's Responses to Assessed Risks).

    This worksheet captures understanding for each key step of the financial
    statement preparation process. For each step the auditor documents:

    - The preparation step (``step_id``) — e.g. journal entry, consolidation,
      period-end close, management override controls
    - Understanding result: key processes, responsible parties, systems used
    - Control activities identified within that step
    - Audit relevancy: how this step affects audit assertions and procedures
    - Potential misstatements: risks arising from the preparation process
    - Related standard account types affected

    Understanding the financial statement preparation process is essential for
    identifying where material misstatements due to error or fraud may occur,
    particularly around journal entries and management estimates.

    Inherits from ``general_audit_worksheet_mixin``.
    """

    _name = "general_audit_ws_f6a227"
    _description = "Understanding of preparation of Financial Statements (f6a227)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_f6a227"
    )

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_f6a227.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Detailed assessment lines related to this worksheet.",
    )
