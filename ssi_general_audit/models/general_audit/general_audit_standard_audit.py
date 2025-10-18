# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import models


class GeneralAuditStandardAudit(models.Model):
    _name = "general_audit_standard_audit"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Standard Audit"
    # No field updates required
