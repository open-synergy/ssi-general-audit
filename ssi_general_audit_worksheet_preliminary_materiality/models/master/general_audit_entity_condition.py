# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditEntityCondition(models.Model):
    """
    Entity condition master used as the basis for materiality judgement.

    Describes which financial statement element (profit before tax,
    EBITDA, assets/liabilities, net assets, ...) best represents the
    audited entity's business, so the auditor can justify the benchmark
    selected for materiality computation (ISA 320 / SA 320).
    """

    _name = "general_audit_entity_condition"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Entity Condition"
