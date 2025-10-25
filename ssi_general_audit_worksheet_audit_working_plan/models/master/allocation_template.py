# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AllocationTemplate(models.Model):
    _name = "allocation_template"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Man Hour Allocation - Template"

    pe_percentage = fields.Float(
        string="Pre-Engagement Allocation (%)",
        help=(
            "Percentage of total manhours allocated to the Pre-Engagement phase. "
            "The sum of all phase percentages in this template must be 100%."
        ),
    )
    ra_percentage = fields.Float(
        string="Risk Assessment Allocation (%)",
        help=(
            "Percentage of total manhours allocated to the Risk Assessment phase. "
            "The sum of all phase percentages in this template must be 100%."
        ),
    )
    rr_percentage = fields.Float(
        string="Risk Response Allocation (%)",
        help=(
            "Percentage of total manhours allocated to the Risk Response phase. "
            "The sum of all phase percentages in this template must be 100%."
        ),
    )
    wr_percentage = fields.Float(
        string="Reporting Allocation (%)",
        help=(
            "Percentage of total manhours allocated to the Reporting phase. "
            "The sum of all phase percentages in this template must be 100%."
        ),
    )

    @api.constrains(
        "pe_percentage",
        "ra_percentage",
        "rr_percentage",
        "wr_percentage",
    )
    def _check_percentage_total(self):
        for record in self:
            total = (
                record.pe_percentage
                + record.ra_percentage
                + record.rr_percentage
                + record.wr_percentage
            )
            if round(total, 2) != 100.00:
                raise ValidationError(
                    "The total allocation of Pre-Engagement, Risk Assessment, "
                    "Risk Response, and Reporting must be exactly 100%. "
                    f"Currently: {total:.2f}%"
                )
