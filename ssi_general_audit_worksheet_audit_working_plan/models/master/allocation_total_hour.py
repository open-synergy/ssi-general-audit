# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AllocatioTotalHour(models.Model):
    """Master data — predefined total man-hour option for audit engagements.

    Provides a library of commonly used total manhour values (e.g., 500 h,
    1 000 h) that can be selected on the Audit Working Plan worksheet to
    auto-fill the total budget, saving time during engagement planning.
    """

    _name = "allocation_total_hour"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Man Hour Allocation - Total Hour"

    total_hour = fields.Float(
        string="Total Hours",
        help=(
            "Predefined total manhours to be used as a reference for worksheets. "
            "Selecting a record can auto-fill the Total Manhour Allocation."
        ),
    )
