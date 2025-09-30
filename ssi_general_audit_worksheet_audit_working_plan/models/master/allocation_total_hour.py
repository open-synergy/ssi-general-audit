# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AllocatioTotalHour(models.Model):
    _name = "allocation_total_hour"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Man Hour Allocation - Total Hour"

    total_hour = fields.Float(
        string="Total Hours",
    )
