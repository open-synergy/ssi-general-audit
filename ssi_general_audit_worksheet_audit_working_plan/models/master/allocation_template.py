# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AllocationTemplate(models.Model):
    """Master data — man-hour allocation template for audit engagements.

    Defines the percentage split of total budgeted man-hours across four
    audit phases:
    * ``pe_percentage``  — Pre-Engagement (%)
    * ``ra_percentage``  — Risk Assessment (%)
    * ``rr_percentage``  — Risk Response / Fieldwork (%)
    * ``wr_percentage``  — Reporting (%)

    A constraint ensures the four percentages always sum to 100 %.  A default
    template can be configured at the company level (``res.company.
    allocation_template_id``) and applied automatically when new Audit Working
    Plan worksheets are created.
    """

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
                total_str = "{:.2f}".format(total)
                raise ValidationError(
                    _(
                        "The total allocation of Pre-Engagement, Risk Assessment, "
                        "Risk Response, and Reporting must be exactly 100%%. "
                        "Currently: %s%%"
                    )
                    % total_str
                )
