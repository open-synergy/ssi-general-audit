# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditInherentRiskFactor(models.Model):
    """
    General Audit Inherent Risk Factor — Master Data

    Master-data model for the **inherent risk factors** used across
    account-level inherent risk assessments.  Factors are referenced by
    the detail lines in the Account Level Inherent Risk worksheet
    (WS.060.2, ``general_audit_ws_a418d89.detail``) where they are
    selected as contributing factors to the risk assessment.

    Each factor is classified as either:

    - *With direct impact* (``direct_impact = True``) — the presence of
      this factor directly elevates the assessed risk level and may trigger
      a ``significant_risk`` flag on the account.
    - *Without direct impact* (``direct_impact = False``) — a contextual
      factor that informs but does not automatically change the risk level.

    **ISA / SA references:** ISA 315 / SA 315 — Identifying and Assessing
    the Risks of Material Misstatement through Understanding the Entity
    and Its Environment
    """

    _name = "general_audit_inherent_risk_factor"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Inherent Risk Factor"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Display order of the inherent risk factor in lists and reports.",
    )
    direct_impact = fields.Boolean(
        string="Direct Impact to Risk",
        default=False,
        help="""If enabled, this factor directly affects the inherent risk assessment.
Used to separate factors with and without direct impact in worksheets.""",
    )
