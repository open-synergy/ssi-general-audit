# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io

from tabulate import tabulate

from odoo import api, fields, models


class GeneralAuditWSa01723b(models.Model):
    _name = "general_audit_ws_a01723b"
    _description = "Population (a01723b)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_population." "worksheet_type_a01723b"

    population_type_id = fields.Many2one(
        comodel_name="general_audit_population_type",
        string="Population Type",
        required=True,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    raw_data = fields.Text(
        string="Raw Data",
        help="Raw data in CSV format",
        required=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    raw_data_preview = fields.Text(
        string="Raw Data Preview",
        help="Preview of raw data",
        compute="_compute_raw_data_preview",
        store=False,
        compute_sudo=True,
    )

    raw_data_count = fields.Integer(
        string="Data Count",
        help="Number of data rows (excluding header)",
        compute="_compute_raw_data_count",
        store=True,
        compute_sudo=True,
    )

    @api.depends("raw_data")
    def _compute_raw_data_count(self):
        for rec in self:
            count = 0
            try:
                if rec.raw_data:
                    reader = csv.reader(io.StringIO(rec.raw_data))
                    rows = list(reader)
                    # Subtract 1 to exclude header row
                    count = max(0, len(rows) - 1)
            except Exception:
                count = 0
            rec.raw_data_count = count

    @api.depends("raw_data")
    def _compute_raw_data_preview(self):
        limit_rows = 50
        for rec in self:
            text_out = False
            try:
                if not rec.raw_data:
                    text_out = "(No data available)"
                else:
                    # Parse CSV from raw_data field
                    reader = csv.reader(io.StringIO(rec.raw_data))
                    rows = list(reader)

                    if not rows:
                        text_out = "(Empty CSV)"
                    else:
                        header = rows[0]
                        data = rows[1 : 1 + limit_rows]
                        table = tabulate(data, headers=header, tablefmt="github")

                        if len(rows) - 1 > limit_rows:
                            total_rows = len(rows) - 1
                            table += (
                                f"\n\n(Note: showing first {limit_rows} rows "
                                f"out of {total_rows} rows)"
                            )

                        text_out = table

            except Exception as e:
                text_out = f"(Failed to parse CSV: {e})"

            rec.raw_data_preview = text_out
