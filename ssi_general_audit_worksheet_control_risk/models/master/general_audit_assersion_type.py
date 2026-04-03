# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditAssersionType(models.Model):
    """Master data — financial-statement assertion type.

    Defines the audit assertion categories used in control evaluation and risk
    identification, typically: Completeness, Accuracy, Valuation, Existence,
    Rights & Obligations, Presentation & Disclosure, and Cut-off.

    Used to link key internal controls and WCGW scenarios to the specific
    assertion(s) they address, supporting the ISA 315 / SA 315 requirement to
    identify risks at the assertion level.
    """

    _name = "general_audit_assersion_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Assersion Type"
