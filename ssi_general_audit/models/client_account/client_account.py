# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


class ClientAccount(models.Model):
    """
    Akun Klien (Chart of Accounts Klien).

    Menyimpan daftar akun-akun yang digunakan oleh klien yang diaudit.
    Setiap akun klien dipetakan ke satu tipe akun standar (``client_account_type``)
    sehingga dapat dianalisis dalam konteks audit. Akun-akun ini menjadi dasar
    pengisian neraca saldo klien (``client_trial_balance``) dan jurnal penyesuaian
    audit (``client_adjustment_entry``).

    Proses pemetaan akun klien ke tipe akun standar diformalkan melalui
    dokumen ``client_account_mapping`` yang memerlukan approval.
    """

    _name = "client_account"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Client Account"
    _order = "partner_id, type_id, sequence, code"
    _show_code_on_display_name = True

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Ordering within the client's chart of accounts.",
    )
    partner_id = fields.Many2one(
        string="Client",
        comodel_name="res.partner",
        domain=[
            ("is_company", "=", True),
            ("parent_id", "=", False),
        ],
        required=True,
        ondelete="restrict",
        help="Client that owns this account.",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="client_account_type",
        required=False,
        ondelete="restrict",
        help="Standard account type mapped to this client account.",
    )
    group_id = fields.Many2one(
        string="Account Group",
        related="type_id.group_id",
        compute_sudo=True,
        store=True,
        help="Account group derived from the selected type.",
    )
    normal_balance = fields.Selection(
        related="type_id.normal_balance",
        compute_sudo=True,
        store=True,
        help="Normal balance derived from the selected type.",
    )

    @api.onchange(
        "type_id",
    )
    def onchange_normal_balance(self):
        self.normal_balance = False
        if self.type_id:
            self.normal_balance = self.type_id.normal_balance

    @api.onchange(
        "partner_id",
    )
    def onchange_partner_running_audit_warning(self):
        """Warn when a new account is created for a client with a running audit.

        An account created by hand is not added to the mapping and the
        general audit automatically, so the user is told the next steps.
        Nothing is returned for an existing record, an empty client or a
        client without a running (draft or open) general audit.

        :return: ``warning`` dictionary, or ``None`` when nothing to warn
        """
        self.ensure_one()
        if self._origin.id or not self.partner_id:
            return None
        audits = (
            self.env["general_audit"]
            .sudo()
            .search(
                [
                    ("partner_id", "=", self.partner_id.id),
                    ("state", "in", ("draft", "open")),
                ],
                order="id",
            )
        )
        if not audits:
            return None
        names = ", ".join(audits[:3].mapped("name"))
        if len(audits) > 3:
            names = _("%(names)s and %(count)s more") % {
                "names": names,
                "count": len(audits) - 3,
            }
        message = _(
            "This client has a running General Audit: %(names)s. An account "
            "created here is not added to the audit automatically. Add the "
            "account to the CoA & Mapping of the audit, then press Account "
            "on the audit."
        ) % {"names": names}
        return {
            "warning": {
                "title": _("Running General Audit"),
                "message": message,
            }
        }

    @api.constrains("code")
    def _check_duplicate_code(self):
        error_msg = _("Duplicate code not allowed")
        for record in self:
            criteria = [
                ("code", "=", record.code),
                ("id", "!=", record.id),
                ("partner_id", "=", record.partner_id.id),
            ]
            count_duplicate = self.search_count(criteria)
            if count_duplicate > 0:
                raise UserError(error_msg)

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        """Search client accounts by code as well as by name.

        Used by the autocomplete of every Many2one that points to
        ``client_account``, so typing part of a code finds the account.
        A negative operator or an empty text keeps the default search.

        :param name: text typed by the user
        :param args: extra domain restricting the result
        :param operator: comparison operator applied to code and name
        :param limit: maximum number of records
        :param name_get_uid: user used to read the display names
        :return: list of ids of the matching accounts
        """
        if not name or operator in expression.NEGATIVE_TERM_OPERATORS:
            return super(ClientAccount, self)._name_search(
                name,
                args=args,
                operator=operator,
                limit=limit,
                name_get_uid=name_get_uid,
            )
        domain = ["|", ("code", operator, name), ("name", operator, name)]
        return self._search(
            expression.AND([domain, args or []]),
            limit=limit,
            access_rights_uid=name_get_uid,
        )
