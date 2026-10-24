# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import base64
import csv
import io

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ImportAdjustmentEntryDetail(models.TransientModel):
    """Import CSV lines into a Client Adjustment Entry.

    Opened from the ``client_adjustment_entry`` form (Details page), this
    wizard reads an uploaded CSV file and creates one
    ``client_adjustment_entry.detail`` record per valid row, so auditors
    do not have to type debit/credit lines one by one.
    """

    _name = "import_adjustment_entry_detail"
    _description = "Import Adjustment Entry Detail"

    @api.model
    def _default_entry_id(self):
        """Return the adjustment entry this wizard was opened from.

        :return: ``client_adjustment_entry`` id, or ``False`` when the
            wizard is opened standalone (no ``active_id`` in context)
        """
        return self.env.context.get("active_id", False)

    entry_id = fields.Many2one(
        string="# Adjustment Entry",
        comodel_name="client_adjustment_entry",
        default=lambda self: self._default_entry_id(),
        help="Adjustment entry that will receive the imported lines.",
    )
    data = fields.Binary(
        string="File",
        required=True,
        help="CSV file with a header row and columns: account code, AJE "
        "code, description, debit, credit. Uncheck 'File Has Header "
        "Row' for a file without a header. This column order changed "
        "in open-synergy/ssi-general-audit#365 (AJE code was inserted "
        "before description) -- older 4-column files must be updated.",
    )

    has_header = fields.Boolean(
        string="File Has Header Row",
        default=True,
        help="""File Has Header Row

* When checked (the default), the first row of the uploaded file is
  always skipped without being checked, since it is assumed to be a
  column header.
* When unchecked, every row, including the first, is treated as
  data.""",
    )
    import_summary = fields.Text(
        string="Import Preview",
        readonly=True,
        help="""Import Preview

Preview computed from the uploaded file before the Import button is
pressed: the client name, how many lines will be created and how many
rows carry an account code that is not found (these make the import
fail). No record is created while computing this preview.""",
    )

    @api.onchange(
        "data",
        "has_header",
    )
    def onchange_import_summary(self):
        """Refresh ``import_summary`` from the uploaded file, in memory.

        Parses the CSV held in ``data`` without creating any record, so
        the user can review the client name, the number of lines to be
        created and the number of unknown account codes.
        """
        self.import_summary = False
        if not self.data:
            return
        rows = self._read_csv_rows()
        if self.has_header and rows:
            rows = rows[1:]
        partner = self.entry_id.general_audit_id.partner_id
        accounts = self.env["client_account"].search([("partner_id", "=", partner.id)])
        codes = set(accounts.mapped("code"))
        unknown = len([row for row in rows if not row or row[0] not in codes])
        client_name = partner.display_name if partner else _("(no client)")
        self.import_summary = _(
            "Client: %(client)s\n"
            "Lines to be created: %(lines)s\n"
            "Rows with unknown account code: %(unknown)s"
        ) % {
            "client": client_name,
            "lines": len(rows),
            "unknown": unknown,
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
        """Import every CSV row as a new adjustment entry detail line.

        The first row is skipped when ``has_header`` is set.

        :return: an ``ir.actions.act_window_close`` dict, closing the
            wizard dialog
        """
        self.ensure_one()
        rows = self._read_csv_rows()
        if self.has_header and rows:
            rows = rows[1:]
        for row in rows:
            self._import_adjustment_entry_detail(row)
        return {"type": "ir.actions.act_window_close"}

    def _import_adjustment_entry_detail(self, row):
        """Create one ``client_adjustment_entry.detail`` from a CSV row.

        Column order (the header row is optional, see ``has_header``):
        account code (``client_account.code``, looked up within the
        entry's client partner), AJE code, description, debit, credit.
        A new detail line is always created — existing lines are never
        updated, since this model has no pre-loaded rows to match
        against.

        :param row: one CSV row, e.g.
            ``["101", "AJE-001", "Cash", "100", "0"]``
        :raises UserError: when the account code is not found in the
            client's chart of accounts
        """
        self.ensure_one()
        criteria = [
            ("code", "=", row[0]),
            (
                "partner_id",
                "=",
                self.entry_id.general_audit_id.partner_id.id,
            ),
        ]
        account = self.env["client_account"].search(criteria, limit=1)
        if not account:
            error_message = _(
                """
Context: Import Adjustment Entry Detail
Database ID: %s
Problem: Account code %s is not found in the client's chart of
    accounts
Solution: Fix the account code in the CSV file, or create the
    account first
"""
                % (self.entry_id.id, row[0])
            )
            raise UserError(error_message)
        self.env["client_adjustment_entry.detail"].create(
            {
                "entry_id": self.entry_id.id,
                "account_id": account.id,
                "aje_code": row[1],
                "name": row[2],
                "debit": row[3] or 0.0,
                "credit": row[4] or 0.0,
            }
        )
