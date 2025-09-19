# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSb9d8a5cAvailabilityItem(models.Model):
    _name = "general_audit_ws_b9d8a5c.availability_item"
    _inherit = [
        "mixin.master_data",
    ]
    _description = (
        "Competency, Availability and Independency "
        "Of Assignment Team (b9d8a5c) - Availability Item"
    )

    code = fields.Char(
        default="/",
    )
