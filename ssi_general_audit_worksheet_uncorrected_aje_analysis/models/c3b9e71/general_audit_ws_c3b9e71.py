# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWsC3b9e71(models.Model):
    """Worksheet CAJE/PAJE - Uncorrected AJE Analysis.

    Compares the misstatements the client chose not to correct (adjustment
    entries with ``corrected`` unchecked) with the audited balance of each
    account group and with the materiality of the audit, then records the
    quantitative and qualitative analysis of the auditor, per account group
    and in aggregate.

    Overall Materiality, Performance Materiality and Clearly Trivial are
    read from the Final Materiality worksheet of the same audit; the
    audited balance of each group is the sum of the ``balance`` of its
    Specific Materiality mapping lines. The tax rate is entered by the
    auditor.
    """

    _name = "general_audit_ws_c3b9e71"
    _description = "Uncorrected AJE Analysis (c3b9e71)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_uncorrected_aje_analysis." "worksheet_type_c3b9e71"
    )

    final_materiality_id = fields.Many2one(
        string="# Final Materiality",
        comodel_name="general_audit_ws_bb33b94",
        compute="_compute_final_materiality_id",
        store=True,
        compute_sudo=True,
        help="Latest non-cancelled Final Materiality worksheet of this "
        "audit. Empty when the audit has no such worksheet.",
    )
    overall_materiality = fields.Monetary(
        string="Overall Materiality",
        currency_field="currency_id",
        compute="_compute_materiality",
        store=True,
        compute_sudo=True,
        help="Overall Materiality of the Final Materiality worksheet. "
        "Zero when the audit has no such worksheet.",
    )
    performance_materiality = fields.Monetary(
        string="Performance Materiality",
        currency_field="currency_id",
        compute="_compute_materiality",
        store=True,
        compute_sudo=True,
        help="Performance Materiality of the Final Materiality worksheet. "
        "Zero when the audit has no such worksheet.",
    )
    clearly_trivial = fields.Monetary(
        string="Clearly Trivial",
        currency_field="currency_id",
        compute="_compute_materiality",
        store=True,
        compute_sudo=True,
        help="Clearly Trivial threshold of the Final Materiality "
        "worksheet. Zero when the audit has no such worksheet.",
    )
    tax_rate = fields.Float(
        string="Tax Rate (%)",
        default=0.0,
        required=True,
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Income tax rate in percent, entered by the auditor. Used to "
        "compute the after-tax effect of the uncorrected misstatements in "
        "the aggregate analysis.",
    )
    group_line_ids = fields.One2many(
        string="Account Groups",
        comodel_name="general_audit_ws_c3b9e71.group_line",
        inverse_name="worksheet_id",
        readonly=True,
        help="Uncorrected misstatement analysis per account group.",
    )
    uncorrected_group_ids = fields.Many2many(
        string="Groups With Uncorrected Misstatement",
        comodel_name="client_account_group",
        compute="_compute_uncorrected_group_ids",
        store=False,
        compute_sudo=True,
        help="Account groups whose uncorrected misstatement is not zero. "
        "Only these groups can be analysed individually.",
    )
    individual_line_ids = fields.One2many(
        string="Individual Analysis",
        comodel_name="general_audit_ws_c3b9e71.individual_line",
        inverse_name="worksheet_id",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Quantitative and qualitative analysis per account group that "
        "has uncorrected misstatements.",
    )
    aggregate_pl_misstatement = fields.Monetary(
        string="Uncorrected Misstatement (Profit or Loss)",
        currency_field="currency_id",
        compute="_compute_aggregate",
        store=True,
        compute_sudo=True,
        help="Net effect of the uncorrected misstatements on profit or "
        "loss (revenue less expense): credit-normal profit and loss groups "
        "add, debit-normal ones subtract.",
    )
    aggregate_pl_net_after_tax = fields.Monetary(
        string="Net Impact After Tax",
        currency_field="currency_id",
        compute="_compute_aggregate",
        store=True,
        compute_sudo=True,
        help="Uncorrected misstatement on profit or loss multiplied by one "
        "minus the tax rate.",
    )
    aggregate_pl_pct_of_pm = fields.Float(
        string="% of Performance Materiality (Profit or Loss)",
        compute="_compute_aggregate",
        store=True,
        compute_sudo=True,
        help="Net impact after tax divided by Performance Materiality. "
        "Zero when Performance Materiality is zero.",
    )
    aggregate_fp_misstatement = fields.Monetary(
        string="Uncorrected Misstatement (Financial Position)",
        currency_field="currency_id",
        compute="_compute_aggregate",
        store=True,
        compute_sudo=True,
        help="Gross total of the uncorrected adjustment entries: total "
        "debit plus total credit of their lines, divided by two. A "
        "balanced entry has equal debit and credit, so this is the total "
        "of one side; netting both sides would give zero.",
    )
    aggregate_fp_pct_of_pm = fields.Float(
        string="% of Performance Materiality (Financial Position)",
        compute="_compute_aggregate",
        store=True,
        compute_sudo=True,
        help="Gross uncorrected misstatement of the financial position "
        "divided by Performance Materiality. Zero when Performance "
        "Materiality is zero.",
    )
    aggregate_qual_profit_loss = fields.Text(
        string="Impact on Profit or Loss",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Qualitative assessment of the aggregate effect on profit or " "loss.",
    )
    aggregate_qual_financial_position = fields.Text(
        string="Impact on the Statement of Financial Position",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Qualitative assessment of the aggregate effect on the "
        "statement of financial position.",
    )
    aggregate_qual_users = fields.Text(
        string="Impact on Users of Financial Statements",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Qualitative assessment of the aggregate effect on the users "
        "of the financial statements.",
    )
    aggregate_qual_other = fields.Text(
        string="Other Qualitative Factor",
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Any other qualitative factor of the aggregate analysis.",
    )
    audit_opinion_impact = fields.Selection(
        string="Impact on the Audit Opinion",
        selection=[
            ("immaterial", "Immaterial misstatement"),
            (
                "material_not_pervasive",
                "Material misstatement, but not pervasive",
            ),
            ("material_pervasive", "Material and pervasive misstatement"),
        ],
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Conclusion of the auditor on the effect of the uncorrected "
        "misstatements on the audit opinion.",
    )

    uncorrected_entry_ids = fields.Many2many(
        string="Uncorrected AJE",
        comodel_name="client_adjustment_entry",
        compute="_compute_uncorrected_entry_ids",
        store=False,
        compute_sudo=True,
        help="Done adjustment entries of this audit that the client did not "
        "correct. These are the entries analysed by this worksheet.",
    )

    def _get_uncorrected_entry_domain(self):
        """Return the domain of the uncorrected adjustment entries.

        :return: search domain on ``client_adjustment_entry``
        :rtype: list
        """
        self.ensure_one()
        return [
            ("general_audit_id", "=", self.general_audit_id.id),
            ("state", "=", "done"),
            ("corrected", "=", False),
        ]

    @api.depends(
        "general_audit_id",
    )
    def _compute_uncorrected_entry_ids(self):
        """Collect the done, uncorrected adjustment entries of the audit.

        :return: ``None``
        """
        Entry = self.env["client_adjustment_entry"]  # pylint: disable=C0103
        for record in self:
            result = Entry.browse()
            if record.general_audit_id:
                result = Entry.search(record._get_uncorrected_entry_domain())
            record.uncorrected_entry_ids = result

    def action_view_uncorrected_entry(self):
        """Open the uncorrected adjustment entries of the audit read-only.

        The list and form views used here forbid create, edit, delete and
        duplicate, whatever the access rights of the user.

        :return: window action on ``client_adjustment_entry``
        :rtype: dict
        """
        self.ensure_one()
        module = "ssi_general_audit_worksheet_uncorrected_aje_analysis"
        tree = self.env.ref(module + ".client_adjustment_entry_readonly_view_tree")
        form = self.env.ref(module + ".client_adjustment_entry_readonly_view_form")
        return {
            "type": "ir.actions.act_window",
            "name": "Uncorrected AJE",
            "res_model": "client_adjustment_entry",
            "view_mode": "tree,form",
            "views": [(tree.id, "tree"), (form.id, "form")],
            "domain": self._get_uncorrected_entry_domain(),
        }

    @api.depends(
        "general_audit_id",
    )
    def _compute_final_materiality_id(self):
        """Find the latest non-cancelled Final Materiality of the audit.

        :return: ``None``
        """
        Final = self.env["general_audit_ws_bb33b94"]  # pylint: disable=C0103
        for record in self:
            result = Final.browse()
            if record.general_audit_id:
                result = Final.search(
                    [
                        ("general_audit_id", "=", record.general_audit_id.id),
                        ("state", "!=", "cancel"),
                    ],
                    order="id desc",
                    limit=1,
                )
            record.final_materiality_id = result

    @api.depends(
        "group_line_ids.group_id",
        "group_line_ids.uncorrected_amount",
    )
    def _compute_uncorrected_group_ids(self):
        """Collect the account groups with a non-zero uncorrected amount.

        :return: ``None``
        """
        for record in self:
            lines = record.group_line_ids.filtered(lambda x: x.uncorrected_amount)
            record.uncorrected_group_ids = lines.mapped("group_id")

    @api.depends(
        "final_materiality_id",
        "final_materiality_id.overall_materiality",
        "final_materiality_id.performance_materiality",
        "final_materiality_id.tolerable_misstatement",
    )
    def _compute_materiality(self):
        """Read the three materiality amounts from the Final Materiality.

        The Final Materiality calls Clearly Trivial what its field
        ``tolerable_misstatement`` holds.

        :return: ``None``
        """
        for record in self:
            final = record.final_materiality_id
            record.overall_materiality = final.overall_materiality
            record.performance_materiality = final.performance_materiality
            record.clearly_trivial = final.tolerable_misstatement

    @api.depends(
        "general_audit_id",
        "group_line_ids.uncorrected_amount",
        "group_line_ids.group_id.report_category",
        "group_line_ids.group_id.normal_balance",
        "tax_rate",
        "performance_materiality",
    )
    def _compute_aggregate(self):
        """Derive the aggregate quantitative figures of the analysis.

        The profit and loss figure nets the profit and loss account
        groups: credit-normal groups add their uncorrected amount and
        debit-normal groups subtract it. The financial position figure is
        the total of one side of the uncorrected adjustment entries: debit
        plus credit of every line, divided by two. Percentages are zero
        when Performance Materiality is zero.

        :return: ``None``
        """
        for record in self:
            pl_amount = 0.0
            for line in record.group_line_ids:
                if line.group_id.report_category != "profit_loss":
                    continue
                if line.group_id.normal_balance == "cr":
                    pl_amount += line.uncorrected_amount
                else:
                    pl_amount -= line.uncorrected_amount
            fp_amount = 0.0
            if record.general_audit_id:
                lines = record._get_uncorrected_lines()
                fp_amount = (
                    sum(lines.mapped("debit")) + sum(lines.mapped("credit"))
                ) / 2.0
            net_after_tax = pl_amount * (1.0 - record.tax_rate / 100.0)
            pm = record.performance_materiality
            record.aggregate_pl_misstatement = pl_amount
            record.aggregate_pl_net_after_tax = net_after_tax
            record.aggregate_pl_pct_of_pm = net_after_tax / pm if pm else 0.0
            record.aggregate_fp_misstatement = fp_amount
            record.aggregate_fp_pct_of_pm = fp_amount / pm if pm else 0.0

    def _get_balance_per_group(self):
        """Sum the Specific Materiality mapping balances per account group.

        :return: mapping of ``client_account_group`` id to balance
        :rtype: dict
        """
        self.ensure_one()
        result = {}
        specific = self.env["general_audit_ws_6dcda0e"].search(
            [
                ("general_audit_id", "=", self.general_audit_id.id),
                ("materiality_type", "=", "pm"),
            ],
            limit=1,
        )
        for mapping in self.env["general_audit_ws_6dcda0e_materiality_mapping"].search(
            [("worksheet_id", "=", specific.id)]
        ):
            group = mapping.type_id.group_id
            result[group.id] = result.get(group.id, 0.0) + mapping.balance
        return result

    def _get_uncorrected_lines(self):
        """Return the lines of the done, uncorrected adjustment entries.

        :return: lines of the entries of the audit that the client did
            not correct
        :rtype: recordset of ``client_adjustment_entry.detail``
        """
        self.ensure_one()
        return self.env["client_adjustment_entry.detail"].search(
            [
                ("entry_id.general_audit_id", "=", self.general_audit_id.id),
                ("entry_id.state", "=", "done"),
                ("entry_id.corrected", "=", False),
            ]
        )

    def _get_uncorrected_per_group(self):
        """Sum uncorrected done adjustment lines per account group.

        The amount follows the normal balance of the group: debit minus
        credit for debit-normal groups, credit minus debit otherwise.

        :return: mapping of ``client_account_group`` id to amount
        :rtype: dict
        """
        self.ensure_one()
        result = {}
        lines = self._get_uncorrected_lines()
        for line in lines:
            group = line.account_id.type_id.group_id
            if group.normal_balance == "dr":
                amount = line.debit - line.credit
            else:
                amount = line.credit - line.debit
            result[group.id] = result.get(group.id, 0.0) + amount
        return result

    def action_reload_group(self):
        """Rebuild the account group lines from the current audit data.

        :return: ``None``
        """
        for record in self:
            record._compute_final_materiality_id()
            record._compute_materiality()
            record.group_line_ids.unlink()
            balances = record._get_balance_per_group()
            uncorrected = record._get_uncorrected_per_group()
            for detail in record.general_audit_id.group_detail_ids:
                group = detail.group_id
                self.env["general_audit_ws_c3b9e71.group_line"].create(
                    {
                        "worksheet_id": record.id,
                        "group_id": group.id,
                        "balance": balances.get(group.id, 0.0),
                        "uncorrected_amount": uncorrected.get(group.id, 0.0),
                    }
                )

    @ssi_decorator.post_open_action()
    def _10_reload_group(self):
        """Build the account group lines when the worksheet is opened.

        :return: ``None``
        """
        self.ensure_one()
        self.action_reload_group()
