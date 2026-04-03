# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import fields, models


class GeneralAuditStandardDetail(models.Model):
    """
    General Audit Standard Detail — Inherent Risk Extension

    Extends ``general_audit.standard_detail`` with inherent-risk
    assessment fields set by the Account Level Inherent Risk worksheet
    (WS.060.2).  These fields are:

    - ``inherent_risk`` (low / medium / high) — the auditor's assessed
      level of inherent risk for this account or area.
    - ``significant_risk`` (boolean) — flags whether the assessed risk
      rises to the level of a significant risk that requires special audit
      attention and communication to TCWG (ISA 315 para. 27(e)).

    Both fields are written back by the inverse method on the detail line
    (``general_audit_ws_a418d89.detail._inverse_to_standard_detail``) so
    that the assessed risk is always stored on the canonical standard detail
    and visible across all worksheets that reference it.

    **ISA / SA references:** ISA 315 / SA 315 — Identifying and Assessing
    the Risks of Material Misstatement
    """

    _name = "general_audit.standard_detail"
    _inherit = ["general_audit.standard_detail"]

    inherent_risk = fields.Selection(
        string="Inherent Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        help="Assessed level of inherent risk for this standard detail (low/medium/high).",
    )
    significant_risk = fields.Boolean(
        string="Significant Risk",
        help=(
            "Indicates whether this standard detail is considered a "
            "significant risk for audit planning and procedures."
        ),
    )
