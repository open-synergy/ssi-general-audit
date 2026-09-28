# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import base64
import csv
import io

from odoo import _, api, fields, models

MAX_ACCOUNT_CODE_LENGTH = 32


class ImportClientAccount(models.TransientModel):
    """
    Bulk-import ``client_account`` records from an uploaded CSV file.

    Each row is matched to an existing ``client_account`` of the target
    partner by code (update) or creates a new one (import). Rows that
    are blank, a header, or carry an over-length code are skipped
    instead of being created, and a new account whose name collides
    with another active account of the same partner is still created
    but flagged in the closing notification.
    """

    _name = "import_client_account"
    _description = "Import Client Account"

    @api.model
    def _default_client_account_mapping(self):
        return self.env.context.get("active_id", False)

    mapping_id = fields.Many2one(
        string="# Client Account Mapping",
        comodel_name="client_account_mapping",
        default=lambda self: self._default_client_account_mapping(),
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
  so every row (including the first) is validated and imported.""",
    )
    import_summary = fields.Text(
        string="Import Preview",
        readonly=True,
        help="""Import Preview

Preview computed from the uploaded file before the Import button is
pressed: the client name and how many rows are valid versus will be
skipped (empty/header/over-length code). No record is created while
computing this preview.""",
    )

    @api.onchange(
        "data",
        "has_header",
    )
    def onchange_import_summary(self):
        """Refresh ``import_summary`` from the uploaded file, in memory.

        Parses the CSV currently held in ``data`` without creating any
        record, so the user can review the client name and the row
        counts (valid vs. to-be-skipped) before pressing Import.
        """
        self.import_summary = False
        if not self.data:
            return
        rows = self._read_csv_rows()
        if self.has_header and rows:
            rows = rows[1:]
            header_skipped = 1
        else:
            header_skipped = 0
        valid = len([row for row in rows if self._is_valid_account_row(row)])
        skipped = header_skipped + (len(rows) - valid)
        partner = self.mapping_id.partner_id
        client_name = partner.display_name if partner else _("(no client)")
        self.import_summary = _(
            "Client: %(client)s\n"
            "Valid rows: %(valid)s\n"
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

    @api.model
    def _is_valid_account_row(self, row):
        """Check whether a CSV row can be imported as ``client_account``.

        A row is invalid when its code column (index 0) is missing,
        blank after stripping whitespace, or longer than
        ``MAX_ACCOUNT_CODE_LENGTH`` — typically a header, title, or
        instruction row rather than actual account data.

        :param row: one parsed CSV row (list of column strings)
        :return: ``True`` when the row's code is usable
        """
        if not row or not row[0]:
            return False
        code = row[0].strip()
        return bool(code) and len(code) <= MAX_ACCOUNT_CODE_LENGTH

    def button_import(self):
        """Import/update client accounts from the uploaded CSV file.

        Rows that are empty, have an over-length code, or (when
        ``has_header`` is set) the file's first row are skipped
        without creating anything. Accounts whose name collides with
        another active account of the same partner are still created,
        but flagged in the returned notification.

        Duplicate-name warnings are collected in a local ``warnings``
        list, never on ``self`` — a ``TransientModel`` recordset is
        slotted (``models.py``), so it cannot hold plain instance
        attributes.

        :return: an ``ir.actions.client`` displaying the import result
        """
        self.ensure_one()
        warnings = []
        rows = self._read_csv_rows()
        if self.has_header and rows:
            rows = rows[1:]
        counter = {"imported": 0, "updated": 0, "skipped": 0}
        for row in rows:
            result = self._import_client_account(row, warnings)
            counter[result] += 1
        return self._prepare_import_notification(counter, warnings)

    def _get_type_id(self, row):
        if len(row) < 4 or not row[3]:
            return False
        types = self.env["client_account_type"].search([("code", "=", row[3])], limit=1)
        return types.id if types else False

    def _check_duplicate_name(self, row, warnings):
        """Record a warning when a new account's name collides.

        Appends ``(code, name)`` to the caller's local ``warnings``
        list when an active ``client_account`` already exists for the
        same partner with the same name (case-insensitive) but a
        different code. Does not block creation — the caller still
        creates the new account.

        :param row: CSV row about to be created as a new account
        :param warnings: local list accumulating ``(code, name)``
            duplicate-name pairs, owned by ``button_import``
        """
        self.ensure_one()
        name = row[1] if len(row) > 1 else False
        if not name:
            return
        criteria = [
            ("partner_id", "=", self.mapping_id.partner_id.id),
            ("code", "!=", row[0]),
        ]
        existing = self.env["client_account"].search(criteria)
        for account in existing:
            if (
                account.name
                and account.name.strip().casefold() == name.strip().casefold()
            ):
                warnings.append((row[0], name))
                break

    def _import_client_account(self, row, warnings):
        """Import or update a single CSV row into ``client_account``.

        Skips the row (returns ``"skipped"``) when
        ``_is_valid_account_row`` rejects it. Otherwise updates the
        matching existing account (``"updated"``) or creates a new one
        (``"imported"``), flagging a name collision via
        ``_check_duplicate_name`` without blocking the creation.

        :param row: one parsed CSV row (list of column strings)
        :param warnings: local list accumulating ``(code, name)``
            duplicate-name pairs, owned by ``button_import``
        :return: ``"imported"``, ``"updated"``, or ``"skipped"``
        """
        self.ensure_one()
        if not self._is_valid_account_row(row):
            return "skipped"
        Account = self.env["client_account"]
        type_id = self._get_type_id(row)
        criteria = [
            ("partner_id", "=", self.mapping_id.partner_id.id),
            ("code", "=", row[0]),
        ]
        accounts = Account.search(criteria)
        if len(accounts) > 0:
            account = accounts[0]
            if type_id:
                account.write({"type_id": type_id})
            result = "updated"
        else:
            self._check_duplicate_name(row, warnings)
            account = Account.create(
                {
                    "code": row[0],
                    "name": row[1],
                    "partner_id": self.mapping_id.partner_id.id,
                    "type_id": type_id,
                }
            )
            result = "imported"

        criteria = [
            ("account_id", "=", account.id),
            ("mapping_id", "=", self.mapping_id.id),
        ]
        details = self.env["client_account_mapping.detail"].search(criteria)

        if len(details) == 0:
            self.env["client_account_mapping.detail"].create(
                {
                    "mapping_id": self.mapping_id.id,
                    "account_id": account.id,
                }
            )
        return result

    def _prepare_import_notification(self, counter, warnings):
        """Build the closing ``display_notification`` action.

        :param counter: dict with ``imported``/``updated``/``skipped``
            row counts
        :param warnings: local list of ``(code, name)`` duplicate-name
            pairs collected by ``button_import``
        :return: an ``ir.actions.client`` dict of type
            ``display_notification``
        """
        self.ensure_one()
        lines = [
            _("%(imported)s imported, %(updated)s updated, %(skipped)s skipped.")
            % counter
        ]
        if warnings:
            shown = warnings[:5]
            pairs = ", ".join("%s/%s" % (code, name) for code, name in shown)
            lines.append(_("Duplicate name warning for: %s") % pairs)
            remaining = len(warnings) - len(shown)
            if remaining > 0:
                lines.append(_("...and %s more.") % remaining)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "warning" if warnings else "success",
                "title": _("Import Client Account"),
                "message": "\n".join(lines),
                "sticky": True,
            },
        }
