# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import csv
import io
from decimal import Decimal, InvalidOperation

from odoo import api, fields, models


class GeneralAuditWsC7d5f2bCheckLine(models.Model):
    """Physical check comparison line of a physical check worksheet.

    Each line compares the parent worksheet's population/sample data
    (``check_data``) against one of its ``data_comparison`` rows, using
    an aggregation method (count/sum/avg) over a chosen amount column
    on each side.
    """

    _name = "general_audit_ws_c7d5f2b.check_line"
    _description = "Physical Check Comparison Line"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_c7d5f2b",
        string="# Worksheet",
        required=True,
        ondelete="cascade",
        index=True,
        help="Parent physical check worksheet.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Determines the display order of check lines.",
    )
    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store=True,
        compute_sudo=True,
        help="Name derived from the selected data comparison source.",
    )
    data_comparison_id = fields.Many2one(
        comodel_name="general_audit_ws_c7d5f2b.data_comparison",
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
    check_data = fields.Text(
        string="Check Data",
        help="CSV result of the physical check comparison: Ref, Amount "
        "Reference, Amount Comparison, Diff, Result.",
    )

    @api.depends("data_comparison_id", "data_comparison_id.name")
    def _compute_name(self):
        """Mirror the name of the selected data comparison source.

        :return: nothing; assigns ``name`` from
            ``data_comparison_id.name``, or ``False`` when unset.
        """
        for record in self:
            record.name = record.data_comparison_id.name or False

    def action_compute_check_data(self):
        """Trigger the physical check computation for each record.

        :return: nothing; delegates to ``_do_compute_check_data`` for
            every record in ``self``.
        """
        for record in self:
            record._do_compute_check_data()

    def _parse_ref_values(self, sampling):
        """Extract the ordered, de-duplicated reference values.

        :param str sampling: CSV sampling data of the parent worksheet.
        :return: list of reference values (column 2), skipping the
            header row and rows marked ``"Candidate"`` in the last
            column.
        :rtype: list
        """
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
        """Index CSV rows by the value of a given reference column.

        :param str raw_str: CSV raw data to index.
        :param int col: 1-based column number holding the reference
            value used as index key.
        :return: mapping of reference value to the list of matching
            rows (excluding the header row).
        :rtype: dict
        """
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
        """Aggregate the amount column of a set of rows.

        :param list rows: rows sharing the same reference value.
        :param int col: 1-based column number holding the amount.
        :param str mode: one of ``"count"``, ``"sum"``, or ``"avg"``.
        :return: the aggregated value; ``Decimal("0")`` when there is
            nothing to aggregate.
        :rtype: Decimal
        """
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

    def _build_check_rows(self, ref_values, ref_index, cmp_index):
        """Build the CSV rows comparing reference vs comparison amounts.

        :param list ref_values: ordered reference values to compare.
        :param dict ref_index: reference-side row index (see
            ``_build_raw_index``).
        :param dict cmp_index: comparison-side row index (see
            ``_build_raw_index``).
        :return: rows including the header, one row per reference
            value with ``Ref``, ``Amount Reference``,
            ``Amount Comparison``, ``Diff``, and ``Result`` columns.
        :rtype: list
        """
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

    def _do_compute_check_data(self):
        """Compute and store ``check_data`` for a single record.

        :return: nothing; assigns ``check_data`` with the CSV
            comparison result, or ``False`` when a required source
            (sampling data, header raw data, comparison raw data, or
            reference column) is missing.
        """
        self.ensure_one()
        ws = self.worksheet_id
        dc = self.data_comparison_id
        sampling = ws.sampling_data
        ref_raw = ws.raw_data
        cmp_raw = dc.raw_data if dc else False
        ref_col = ws.reference_col_number
        cmp_ref_col = dc.reference_col_number if dc else 0

        if not sampling or not ref_raw or not cmp_raw or not ref_col:
            self.check_data = False
            return

        try:
            ref_values = self._parse_ref_values(sampling)
            ref_index = self._build_raw_index(ref_raw, ref_col)
            cmp_index = self._build_raw_index(cmp_raw, cmp_ref_col)
            result_rows = self._build_check_rows(ref_values, ref_index, cmp_index)
            output = io.StringIO()
            csv.writer(output).writerows(result_rows)
            self.check_data = output.getvalue()
        except Exception:
            self.check_data = False
