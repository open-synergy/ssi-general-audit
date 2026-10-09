# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWsC3b9e71(models.Model):
    """Worksheet CAJE/PAJE - Uncorrected AJE Analysis.

    Compares the misstatements the client chose not to correct (adjustment
    entries with ``corrected`` unchecked) with the audited balance of each
    account group and with Performance Materiality, then concludes whether
    their after-tax effect on profit is material.

    Performance Materiality is read from the Specific Materiality worksheet
    of the same audit; the audited balance of each group is the sum of the
    ``balance`` of its Specific Materiality mapping lines. The tax rate is
    entered by the auditor.
    """

    _name = "general_audit_ws_c3b9e71"
    _description = "Uncorrected AJE Analysis (c3b9e71)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_uncorrected_aje_analysis." "worksheet_type_c3b9e71"
    )

    performance_materiality = fields.Monetary(
        string="Performance Materiality",
        currency_field="currency_id",
        compute="_compute_performance_materiality",
        store=True,
        compute_sudo=True,
        help="Performance Materiality of the Specific Materiality worksheet "
        "of this audit. Zero when the audit has no such worksheet.",
    )
    tax_rate = fields.Float(
        string="Tax Rate (%)",
        default=0.0,
        required=True,
        readonly=True,
        states={"open": [("readonly", False)]},
        help="Income tax rate in percent, entered by the auditor. Used to "
        "compute the after-tax effect of the uncorrected misstatements.",
    )
    group_line_ids = fields.One2many(
        string="Account Groups",
        comodel_name="general_audit_ws_c3b9e71.group_line",
        inverse_name="worksheet_id",
        readonly=True,
        help="Uncorrected misstatement analysis per account group.",
    )
    pre_tax_impact = fields.Monetary(
        string="Pre-Tax Impact on Profit",
        currency_field="currency_id",
        compute="_compute_impact",
        store=True,
        compute_sudo=True,
        help="Effect of the uncorrected misstatements on profit before tax: "
        "credit-normal profit and loss groups add, debit-normal ones "
        "subtract.",
    )
    post_tax_impact = fields.Monetary(
        string="After-Tax Impact on Profit",
        currency_field="currency_id",
        compute="_compute_impact",
        store=True,
        compute_sudo=True,
        help="Pre-tax impact multiplied by one minus the tax rate.",
    )
    materiality_conclusion = fields.Selection(
        string="Materiality Conclusion",
        selection=[
            ("material", "Material"),
            ("not_material", "Not Material"),
        ],
        compute="_compute_impact",
        store=True,
        compute_sudo=True,
        help="Material when the absolute after-tax impact is greater than "
        "Performance Materiality.",
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
    def _compute_performance_materiality(self):
        """Read Performance Materiality from the Specific Materiality sheet.

        :return: ``None``
        """
        Specific = self.env["general_audit_ws_6dcda0e"]  # pylint: disable=C0103
        for record in self:
            result = 0.0
            if record.general_audit_id:
                specific = Specific.search(
                    [
                        ("general_audit_id", "=", record.general_audit_id.id),
                        ("materiality_type", "=", "pm"),
                    ],
                    limit=1,
                )
                result = specific.base
            record.performance_materiality = result

    @api.depends(
        "group_line_ids.uncorrected_amount",
        "group_line_ids.group_id.report_category",
        "group_line_ids.group_id.normal_balance",
        "tax_rate",
        "performance_materiality",
    )
    def _compute_impact(self):
        """Derive profit impact before and after tax, and the conclusion.

        Only account groups with the Profit & Loss report category count:
        credit-normal groups add their uncorrected amount and debit-normal
        groups subtract it.

        :return: ``None``
        """
        for record in self:
            pre_tax = 0.0
            for line in record.group_line_ids:
                if line.group_id.report_category != "profit_loss":
                    continue
                if line.group_id.normal_balance == "cr":
                    pre_tax += line.uncorrected_amount
                else:
                    pre_tax -= line.uncorrected_amount
            post_tax = pre_tax * (1.0 - record.tax_rate / 100.0)
            conclusion = "not_material"
            if abs(post_tax) > record.performance_materiality:
                conclusion = "material"
            record.pre_tax_impact = pre_tax
            record.post_tax_impact = post_tax
            record.materiality_conclusion = conclusion

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

    def _get_uncorrected_per_group(self):
        """Sum uncorrected done adjustment lines per account group.

        The amount follows the normal balance of the group: debit minus
        credit for debit-normal groups, credit minus debit otherwise.

        :return: mapping of ``client_account_group`` id to amount
        :rtype: dict
        """
        self.ensure_one()
        result = {}
        lines = self.env["client_adjustment_entry.detail"].search(
            [
                ("entry_id.general_audit_id", "=", self.general_audit_id.id),
                ("entry_id.state", "=", "done"),
                ("entry_id.corrected", "=", False),
            ]
        )
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
            record._compute_performance_materiality()
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
