# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from .import_client_account import MAX_ACCOUNT_CODE_LENGTH


class AddClientAccount(models.TransientModel):
    """
    Add one or more client accounts straight from an open mapping.

    The user types code, name and type of every missing account. All
    rows are validated before anything is created; then each row
    becomes a ``client_account`` of the mapping's client plus a
    ``client_account_mapping.detail`` row, in one transaction. The
    client is taken from the mapping and cannot be changed.
    """

    _name = "add_client_account"
    _description = "Add Client Account"

    @api.model
    def _default_mapping_id(self):
        """Return the mapping the wizard was opened from.

        :return: id of the active ``client_account_mapping``, or False
        """
        return self.env.context.get("active_id", False)

    mapping_id = fields.Many2one(
        string="# Client Account Mapping",
        comodel_name="client_account_mapping",
        default=lambda self: self._default_mapping_id(),
        required=True,
        help="Mapping that receives the new accounts.",
    )
    partner_id = fields.Many2one(
        string="Client",
        comodel_name="res.partner",
        related="mapping_id.partner_id",
        readonly=True,
        help="Client that owns the new accounts. Taken from the mapping.",
    )
    line_ids = fields.One2many(
        string="Accounts",
        comodel_name="add_client_account_line",
        inverse_name="wizard_id",
        help="Accounts to create and map.",
    )

    def _collect_problems(self):
        """Validate every line without creating anything.

        Checks for a missing line, an empty or over-length code, a code
        repeated inside the wizard, and a code already used by the
        client.

        :return: list of problem sentences, empty when all is valid
        """
        self.ensure_one()
        problems = []
        if not self.line_ids:
            problems.append(_("No account line to add"))
            return problems
        existing = set(
            self.env["client_account"]
            .search([("partner_id", "=", self.mapping_id.partner_id.id)])
            .mapped("code")
        )
        seen = set()
        for line in self.line_ids:
            code = (line.code or "").strip()
            if not code:
                problems.append(_("Empty code (name: %s)") % (line.name or "-"))
            elif len(code) > MAX_ACCOUNT_CODE_LENGTH:
                problems.append(
                    _("Code %(code)s is longer than %(max)s characters")
                    % {"code": code, "max": MAX_ACCOUNT_CODE_LENGTH}
                )
            elif code in seen:
                problems.append(_("Code %s is used twice in the wizard") % code)
            elif code in existing:
                problems.append(_("Code %s already exists for this client") % code)
            seen.add(code)
        return problems

    def _get_duplicate_name_warnings(self):
        """List new accounts whose name matches another client account.

        The comparison ignores case and surrounding spaces and only
        considers accounts with a different code. It never blocks.

        :return: list of ``(code, name)`` pairs
        """
        self.ensure_one()
        warnings = []
        existing = self.env["client_account"].search(
            [("partner_id", "=", self.mapping_id.partner_id.id)]
        )
        for line in self.line_ids:
            name = (line.name or "").strip().casefold()
            code = line.code.strip()
            for account in existing:
                if (
                    account.code != code
                    and account.name
                    and account.name.strip().casefold() == name
                ):
                    warnings.append((code, line.name))
                    break
        return warnings

    def _prepare_account_vals(self, line):
        """Build the ``client_account`` values for one line.

        :param line: an ``add_client_account_line`` record
        :return: dict of values for ``client_account.create``
        """
        self.ensure_one()
        return {
            "partner_id": self.mapping_id.partner_id.id,
            "code": line.code.strip(),
            "name": line.name,
            "type_id": line.type_id.id,
        }

    def action_add(self):
        """Create the accounts and their mapping rows.

        :return: an ``ir.actions.client`` displaying the result
        """
        for record in self.sudo():
            result = record._add_accounts()
        return result

    def _add_accounts(self):
        """Validate every line, then create accounts and mapping rows.

        Any problem aborts the whole action with a single structured
        ``UserError`` listing them, before anything is created.

        :return: an ``ir.actions.client`` displaying the result
        """
        self.ensure_one()
        problems = self._collect_problems()
        if problems:
            error_message = (
                _(
                    """
Context: Add Client Account
Database ID: %(id)s
Problem: %(problems)s
Solution: Correct the lines and try again, nothing was created
"""
                )
                % {"id": self.id, "problems": "; ".join(problems)}
            )
            raise UserError(error_message)
        warnings = self._get_duplicate_name_warnings()
        for line in self.line_ids:
            account = self.env["client_account"].create(
                self._prepare_account_vals(line)
            )
            self.env["client_account_mapping.detail"].create(
                {"mapping_id": self.mapping_id.id, "account_id": account.id}
            )
        return self._prepare_notification(len(self.line_ids), warnings)

    def _prepare_notification(self, count, warnings):
        """Build the ``display_notification`` action that closes the wizard.

        :param count: number of accounts (and mapping rows) created
        :param warnings: list of ``(code, name)`` duplicate-name pairs
        :return: an ``ir.actions.client`` dict of type
            ``display_notification``
        """
        self.ensure_one()
        lines = [
            _("%(accounts)s accounts and %(details)s mapping rows created.")
            % {"accounts": count, "details": count}
        ]
        if warnings:
            pairs = ", ".join("%s/%s" % (code, name) for code, name in warnings[:5])
            lines.append(_("Duplicate name warning for: %s") % pairs)
            remaining = len(warnings) - 5
            if remaining > 0:
                lines.append(_("...and %s more.") % remaining)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "warning" if warnings else "success",
                "title": _("Add Client Account"),
                "message": "\n".join(lines),
                "sticky": True,
                # Close the dialog once the notification is shown.
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
