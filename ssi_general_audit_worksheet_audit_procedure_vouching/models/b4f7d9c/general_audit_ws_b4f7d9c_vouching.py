# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io
from decimal import Decimal, InvalidOperation

from odoo import api, fields, models


class GeneralAuditWSb4f7d9cVouching(models.Model):
    _name = "general_audit_ws_b4f7d9c.vouching"
    _description = "Vouching Comparison Line"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_b4f7d9c",
        string="# Worksheet",
        required=True,
        ondelete="cascade",
        index=True,
        help="Parent vouching worksheet.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Determines the display order of vouching lines.",
    )
    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store=True,
        compute_sudo=True,
        help="Name derived from the selected data comparison source.",
    )
    data_comparison_id = fields.Many2one(
        comodel_name="general_audit_ws_b4f7d9c.data_comparison",
        string="Data Comparison",
        required=True,
        domain="[('worksheet_id', '=', worksheet_id)]",
        help="The data comparison source to compare against the header " "raw data.",
    )
    comparison_mode = fields.Selection(
        string="Comparison Mode",
        selection=[
            ("count", "Count"),
            ("sum", "Sum"),
            ("avg", "AVG"),
        ],
        required=True,
        help="The aggregation method used when comparing values: "
        "Count counts matching rows, Sum totals monetary values, "
        "AVG calculates the average.",
    )
    reference_amount_col = fields.Integer(
        string="Reference Amount Column",
        help="The column number (1-based) in the header raw data (sampling "
        "data) that contains the monetary amount to compare.",
    )
    comparison_amount_col = fields.Integer(
        string="Comparison Amount Column",
        help="The column number (1-based) in the data comparison raw data "
        "that contains the monetary amount to compare against.",
    )
    vouching_data = fields.Text(
        string="Vouching Data",
        help="CSV result of the vouching comparison: Ref, Amount Reference, "
        "Amount Comparison, Diff, Result.",
    )

    @api.depends("data_comparison_id", "data_comparison_id.name")
    def _compute_name(self):
        for record in self:
            record.name = record.data_comparison_id.name or False

    def action_compute_vouching_data(self):
        for record in self:
            record._do_compute_vouching_data()

    def _parse_ref_values(self, sampling):
        rows = list(csv.reader(io.StringIO(sampling)))
        ref_values = []
        seen = set()
        for idx, row in enumerate(rows):
            if idx == 0:
                continue
            if len(row) >= 2 and row[-1].strip() != "Candidate":
                val = row[1].strip()
                if val and val not in seen:
                    ref_values.append(val)
                    seen.add(val)
        return ref_values

    def _build_raw_index(self, raw_str, col):
        if not col:
            return {}
        rows = list(csv.reader(io.StringIO(raw_str)))
        index = {}
        for idx, row in enumerate(rows):
            if idx == 0:
                continue
            if len(row) >= col:
                key = row[col - 1].strip()
                index.setdefault(key, []).append(row)
        return index

    def _aggregate_values(self, rows, col, mode):
        if not col or not rows:
            return Decimal("0")
        values = []
        for row in rows:
            if len(row) >= col:
                try:
                    values.append(Decimal(row[col - 1].strip()))
                except InvalidOperation:
                    pass
        if mode == "count":
            return Decimal(len(rows))
        if mode == "sum":
            return sum(values, Decimal("0"))
        if mode == "avg" and values:
            return sum(values, Decimal("0")) / len(values)
        return Decimal("0")

    def _build_vouching_rows(self, ref_values, ref_index, cmp_index):
        rows = [["Ref", "Amount Reference", "Amount Comparison", "Diff", "Result"]]
        ref_amt_col = self.reference_amount_col
        cmp_amt_col = self.comparison_amount_col
        mode = self.comparison_mode
        for ref in ref_values:
            amt_ref = self._aggregate_values(ref_index.get(ref, []), ref_amt_col, mode)
            amt_cmp = self._aggregate_values(cmp_index.get(ref, []), cmp_amt_col, mode)
            diff = amt_ref - amt_cmp
            result = "True" if diff == 0 else "False"
            rows.append([ref, str(amt_ref), str(amt_cmp), str(diff), result])
        return rows

    def _do_compute_vouching_data(self):
        self.ensure_one()
        ws = self.worksheet_id
        dc = self.data_comparison_id
        sampling = ws.sampling_data
        ref_raw = ws.raw_data
        cmp_raw = dc.raw_data if dc else False
        ref_col = ws.reference_col_number
        cmp_ref_col = dc.reference_col_number if dc else 0

        if not sampling or not ref_raw or not cmp_raw or not ref_col:
            self.vouching_data = False
            return

        try:
            ref_values = self._parse_ref_values(sampling)
            ref_index = self._build_raw_index(ref_raw, ref_col)
            cmp_index = self._build_raw_index(cmp_raw, cmp_ref_col)
            result_rows = self._build_vouching_rows(ref_values, ref_index, cmp_index)
            output = io.StringIO()
            csv.writer(output).writerows(result_rows)
            self.vouching_data = output.getvalue()
        except Exception:
            self.vouching_data = False
