# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa13a30e(models.Model):
    """Worksheet: Understanding of Relevant Regulations (a13a30e) — RA.150.7.

    Documents the auditor's identification and assessment of laws and
    regulations applicable to the entity, in accordance with:
    - ISA 315 (Revised) / SA 315 — Understanding the regulatory environment
    - ISA 250 / SA 250 — Consideration of Laws and Regulations

    For each applicable regulation, the auditor captures:
    - The regulation reference and specific item/section being assessed
    - Related standard account types affected by the regulation
    - Whether the regulation has a significant impact on the financial
      statements (``significant_impact``)

    Understanding the regulatory framework enables auditors to:
    - Identify potential non-compliance risks (ISA 250)
    - Assess how regulatory requirements affect accounting treatments
    - Link regulatory impacts to specific account areas for targeted testing

    Inherits from ``general_audit_worksheet_mixin``.
    """

    _name = "general_audit_ws_a13a30e"
    _description = "Understanding of Relevant Regulations (a13a30e)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_a13a30e"
    )

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_a13a30e.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Regulatory items and assessments related to this worksheet.",
    )
