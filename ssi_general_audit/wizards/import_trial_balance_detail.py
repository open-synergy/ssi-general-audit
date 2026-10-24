# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import base64
import csv
import io

from odoo import _, api, fields, models


class ImportTrialBalanceDetail(models.TransientModel):
    """Update ``client_trial_balance.detail`` values from a CSV file.

    Each row is matched to an existing detail line of the trial
    balance by account code. Rows whose account code is not found are
    skipped silently, and the first row can be skipped as a header.
    """

    _name = "import_trial_balance_detail"
    _description = "Import Trial Balance Detail"

    @api.model
    def _default_trial_balance_id(self):
        return self.env.context.get("active_id", False)

    trial_balance_id = fields.Many2one(
        string="# Trial Balance",
        comodel_name="client_trial_balance",
        default=lambda self: self._default_trial_balance_id(),
        store=True,
        compute=False,
    )
    data = fields.Binary(string="File", required=True)
    has_header = fields.Boolean(
        string="File Has Header Row",
        default=True,
        help="""File Has Header Row

* When checked (the default), the first row of the uploaded file is
  always skipped without being checked, since it is assumed to be a
  column header.
* Uncheck this if the uploaded file does not start with a header row,
  so every row (including the first) is processed.""",
    )
    import_summary = fields.Text(
        string="Import Preview",
        readonly=True,
        help="""Import Preview

Preview computed from the uploaded file before the Import button is
pressed: the client name, how many rows will be processed and how many
will be skipped (header row, or account code not found in this trial
balance). No record is changed while computing this preview.""",
    )

    @api.onchange(
        "data",
        "has_header",
    )
    def onchange_import_summary(self):
        """Refresh ``import_summary`` from the uploaded file, in memory.

        Parses the CSV held in ``data`` without writing any record, so
        the user can review the client name and the processed versus
        skipped row counts before pressing Import.
        """
        self.import_summary = False
        if not self.data:
            return
        rows = self._read_csv_rows()
        header_skipped = 0
        if self.has_header and rows:
            rows = rows[1:]
            header_skipped = 1
        codes = set(self.trial_balance_id.detail_ids.mapped("account_id.code"))
        valid = len([row for row in rows if len(row) >= 6 and row[0] in codes])
        skipped = header_skipped + (len(rows) - valid)
        partner = self.trial_balance_id.general_audit_id.partner_id
        client_name = partner.display_name if partner else _("(no client)")
        self.import_summary = _(
            "Client: %(client)s\n"
            "Rows to be processed: %(valid)s\n"
            "Rows to be skipped: %(skipped)s"
        ) % {
            "client": client_name,
            "valid": valid,
            "skipped": skipped,
        }

    def _read_csv_rows(self):
        """Decode ``data`` and parse it as CSV rows.

        :return: list of rows, each row a list of column strings
        """
        self.ensure_one()
        csv_data = base64.b64decode(self.data)
        data_file = io.StringIO(csv_data.decode("utf-8"))
        data_file.seek(0)
        reader = csv.reader(data_file, delimiter=",")
        return list(reader)

    def button_import(self):
        """Write the CSV values into the matching trial balance details.

        The first row is skipped when ``has_header`` is set. Rows whose
        account code matches no detail line are ignored.

        :return: an ``ir.actions.act_window_close`` dict, closing the
            wizard dialog
        """
        self.ensure_one()
        rows = self._read_csv_rows()
        if self.has_header and rows:
            rows = rows[1:]
        for row in rows:
            self._update_trial_balance_detail(row)
        return {"type": "ir.actions.act_window_close"}

    def _update_trial_balance_detail(self, row):
        self.ensure_one()
        Detail = self.env["client_trial_balance.detail"]
        criteria = [
            ("trial_balance_id", "=", self.trial_balance_id.id),
            ("account_id.code", "=", row[0]),
        ]
        Detail.search(criteria).write(
            {
                "opening_balance_debit": row[2],
                "opening_balance_credit": row[3],
                "debit": row[4],
                "credit": row[5],
            }
        )
