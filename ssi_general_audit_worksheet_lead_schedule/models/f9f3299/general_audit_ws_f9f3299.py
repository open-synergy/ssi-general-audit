# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSf9f3299(models.Model):
    """
    WS: Lead Schedule – per Account Type (f9f3299) — ISA 230 / SA 230.

    Produces a detailed lead schedule scoped to a **specific account type**
    (e.g., Cash and Cash Equivalents, Receivables, Inventories).  For each
    account within the selected type the worksheet shows:

    * **Current balance** — End Period or Interim depending on
      ``balance_type``.
    * **Supporting schedule** reference — cross-link to the sub-schedule
      where audit work was performed.
    * **Adjustment journal entries** — linked debit/credit adjustment records.
    * **Adjusted balance** — balance after applying adjustments, respecting
      normal balance side.
    * **Previous balance** — prior-year comparative.
    * **Year-on-year difference (%)** — percentage change between adjusted and
      previous balances for preliminary analytical review.

    Account lines are synchronised via ``action_reload_account``: lines
    are added for General Audit details of ``account_type_id`` that have
    none, and removed only when their account left that type. Other
    lines, with their manual input, are never touched.

    Allowed account types are restricted to types registered on the parent
    General Audit standard details.
    """

    _name = "general_audit_ws_f9f3299"
    _description = "Lead Schedule - Account (f9f3299)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_lead_schedule." "worksheet_type_f9f3299"

    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Standard Account Type",
        required=False,
        states={
            "open": [("readonly", False)],
        },
        readonly=True,
        ondelete="restrict",
    )
    allowed_account_type_ids = fields.Many2many(
        comodel_name="client_account_type",
        string="Allowed Account Types",
        help="Account types that can be selected",
        compute="_compute_allowed_account_type_ids",
        store=False,
    )

    balance_type = fields.Selection(
        selection=[
            ("end_period", "End Period Balance"),
            ("interim", "Interim Balance"),
        ],
        string="Balance Type",
        required=False,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Type of balance to consider for the accounts.",
    )
    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_f9f3299.detail",
        inverse_name="worksheet_id",
        string="Details",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
        help="Detailed lines for each account in the lead schedule.",
    )

    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_account_type_ids(self):
        for record in self:
            record.allowed_account_type_ids = self.env["client_account_type"]
            if record.general_audit_id:
                record.allowed_account_type_ids = record.general_audit_id.mapped(
                    "standard_detail_ids.type_id"
                )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_account_type_id(self):
        self.account_type_id = False

    def action_reload_account(self):
        for record in self.sudo():
            record._reload_account()

    def _reload_account(self):
        """Synchronise the lines with the accounts of the account type.

        Compares the General Audit details whose account has type
        ``account_type_id`` with the details already in ``detail_ids``.
        A line is created for each detail that has none, and the lines
        of details that left the type are removed. Other lines are never
        touched, so a second call changes nothing. Without
        ``account_type_id`` nothing is done.

        :return: True
        """
        self.ensure_one()
        if not self.account_type_id:
            return True
        wanted = self.general_audit_id.detail_ids.filtered(
            lambda d: d.account_id.type_id == self.account_type_id
        )
        current = self.detail_ids.mapped("detail_id")
        obsolete = self.detail_ids.filtered(lambda l: l.detail_id not in wanted)
        obsolete.unlink()
        for detail in wanted - current:
            self.env["general_audit_ws_f9f3299.detail"].create(
                {
                    "worksheet_id": self.id,
                    "detail_id": detail.id,
                    "account_id": detail.account_id.id,
                }
            )
        return True

    def _add_accounts_to_worksheet(self, accounts):
        """Load newly added client accounts into this worksheet.

        Delegates to ``_reload_account``, which is incremental: lines
        that already exist are kept as they are.

        :param accounts: ``client_account`` recordset just added to the
            audit
        :return: nothing
        """
        self.ensure_one()
        self._reload_account()
