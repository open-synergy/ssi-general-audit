# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSb555edd(models.Model):
    """Worksheet — Report Formatting Control (b555edd).

    A quality-control worksheet for reviewing the formatting, grammar,
    consistency, and presentation quality of the draft auditor's report
    before partner sign-off and issuance.  Ensures the report meets the
    firm's style and quality standards.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 700/SA 700 (Forming an Opinion and Reporting).
    """

    _name = "general_audit_ws_b555edd"
    _description = "Report Formatting Control (b555edd)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_draft_reporting." "worksheet_type_b555edd"
    )

    #: ``client_account_group.code`` values shown on the Statement of
    #: Financial Position tab (T001-T008) and on the Statement of
    #: Comprehensive Income tab (T009-T015).
    _SFP_GROUP_CODES = [f"T{number:03d}" for number in range(1, 9)]
    _SOCI_GROUP_CODES = [f"T{number:03d}" for number in range(9, 16)]

    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_b555edd.detail",
        inverse_name="worksheet_id",
        string="Details",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
        help="One line per standard account type of the General Audit.",
    )
    sfp_detail_ids = fields.One2many(
        comodel_name="general_audit_ws_b555edd.detail",
        inverse_name="worksheet_id",
        string="Statement of Financial Position",
        domain=[("group_id.code", "in", _SFP_GROUP_CODES)],
        readonly=True,
        help=(
            "Detail lines whose account group is T001-T008 "
            "(assets, liabilities and equity)."
        ),
    )
    soci_detail_ids = fields.One2many(
        comodel_name="general_audit_ws_b555edd.detail",
        inverse_name="worksheet_id",
        string="Statement of Comprehensive Income",
        domain=[("group_id.code", "in", _SOCI_GROUP_CODES)],
        readonly=True,
        help=(
            "Detail lines whose account group is T009-T015 "
            "(revenue, expenses and other comprehensive income)."
        ),
    )

    equity_line_ids = fields.One2many(
        comodel_name="general_audit_ws_b555edd.equity_line",
        inverse_name="worksheet_id",
        string="Equity Lines",
        readonly=True,
        help="One line per equity component and period.",
    )
    equity_current_ids = fields.One2many(
        comodel_name="general_audit_ws_b555edd.equity_line",
        inverse_name="worksheet_id",
        string="Changes in Equity - Current Period",
        domain=[("period", "=", "current")],
        help="Equity lines of the current period.",
    )
    equity_previous_ids = fields.One2many(
        comodel_name="general_audit_ws_b555edd.equity_line",
        inverse_name="worksheet_id",
        string="Changes in Equity - Previous Period",
        domain=[("period", "=", "previous")],
        help="Equity lines of the previous period.",
    )
    cashflow_line_ids = fields.One2many(
        comodel_name="general_audit_ws_b555edd.cashflow_line",
        inverse_name="worksheet_id",
        string="Cash Flow Lines",
        readonly=True,
        help="One line per cash flow item and period.",
    )
    cashflow_current_ids = fields.One2many(
        comodel_name="general_audit_ws_b555edd.cashflow_line",
        inverse_name="worksheet_id",
        string="Cash Flows - Current Period",
        domain=[("period", "=", "current")],
        help="Cash flow lines of the current period.",
    )
    cashflow_previous_ids = fields.One2many(
        comodel_name="general_audit_ws_b555edd.cashflow_line",
        inverse_name="worksheet_id",
        string="Cash Flows - Previous Period",
        domain=[("period", "=", "previous")],
        help="Cash flow lines of the previous period.",
    )
    cashflow_has_manual = fields.Boolean(
        string="Has Manual Cash Flow Input",
        compute="_compute_cashflow_has_manual",
        help="True when a manual cash flow amount has been typed in.",
    )
    reload_needs_confirm = fields.Boolean(
        string="Reload Needs Confirmation",
        compute="_compute_reload_needs_confirm",
        help="True when Reload would discard figures typed in by the user.",
    )
    equity_has_manual = fields.Boolean(
        string="Has Manual Equity Input",
        compute="_compute_equity_has_manual",
        help="True when an owner transaction has been typed in.",
    )

    @api.depends(
        "equity_line_ids.issuance",
        "equity_line_ids.treasury",
        "equity_line_ids.reserve",
        "equity_line_ids.dividend",
    )
    def _compute_equity_has_manual(self):
        """Flag worksheets whose owner transactions are filled in.

        :return: None
        """
        for record in self:
            record.equity_has_manual = any(
                line.issuance or line.treasury or line.reserve or line.dividend
                for line in record.equity_line_ids
            )

    @api.depends("cashflow_line_ids.amount", "cashflow_line_ids.calc_type")
    def _compute_cashflow_has_manual(self):
        """Flag worksheets with a manual cash flow amount typed in.

        :return: None
        """
        for record in self:
            record.cashflow_has_manual = any(
                line.calc_type == "manual" and line.amount
                for line in record.cashflow_line_ids
            )

    @api.depends("equity_has_manual", "cashflow_has_manual")
    def _compute_reload_needs_confirm(self):
        """Flag worksheets whose typed-in figures Reload would discard.

        :return: None
        """
        for record in self:
            record.reload_needs_confirm = (
                record.equity_has_manual or record.cashflow_has_manual
            )

    def action_reload_account(self):
        """Refill the detail lines from the General Audit standard details.

        :return: None
        """
        for record in self.sudo():
            record._reload_account()

    def _reload_account(self):
        """Replace the detail, equity and cash flow lines with fresh ones.

        Every standard account type of the General Audit gets a line,
        whether it belongs to the financial position or to the
        comprehensive income statement. Existing lines are removed
        first, so clicking Reload again never duplicates lines. The
        equity and cash flow lines are rebuilt as well, see
        ``_reload_equity()`` and ``_reload_cashflow()``.

        :return: None
        """
        self.ensure_one()
        self.detail_ids.unlink()
        Detail = self.env["general_audit_ws_b555edd.detail"]
        for standard_detail in self.general_audit_id.standard_detail_ids:
            type_ = standard_detail.type_id
            Detail.create(
                {
                    "worksheet_id": self.id,
                    "standard_detail_id": standard_detail.id,
                    "sequence": type_.group_id.sequence * 1000 + type_.sequence,
                }
            )
        self._reload_equity()
        self._reload_cashflow()

    def _get_period_fields(self, period):
        """Return the standard detail fields holding a period's balances.

        :param period: ``current`` or ``previous``
        :type period: str
        :return: ``(opening balance field, closing balance field)``
        :rtype: tuple
        """
        if period == "current":
            return "home_statement_opening_balance", "audited_balance"
        return "previous_opening_balance", "previous_balance"

    def _get_formula_total(self, total_type, field, details):
        """Sum a signed ``total_formula`` total over the given details.

        :param str total_type: ``total_type`` of the formula, for example
            ``profit_after_tax``
        :param str field: balance field of the standard detail to sum
        :param details: standard details (anything with ``type_id`` and
            the balance fields)
        :return: the signed total
        :rtype: float
        """
        formula_model = self.env["general_audit_ws_ff42fdc.total_formula"].sudo()
        amount = 0.0
        for formula in formula_model.search([("total_type", "=", total_type)]):
            sign = 1 if formula.sign == "add" else -1
            amount += sign * sum(
                detail[field]
                for detail in details
                if detail.type_id.group_id == formula.group_id
            )
        return amount

    def _get_equity_source(self, period):
        """Read the equity figures of one period from the standard details.

        Balances are taken with the sign of each account type's normal
        balance side, so equity reads as a positive amount. Profit is
        the ``profit_after_tax`` total and OCI the ``comprehensive_
        profit`` total minus it, both from the signed groups of
        ``general_audit_ws_ff42fdc.total_formula``.

        :param period: ``current`` or ``previous``
        :type period: str
        :return: ``{"profit": float, "oci": float, "components":
            {component id: (opening, closing before profit and OCI)}}``
        :rtype: dict
        """
        self.ensure_one()
        opening_field, closing_field = self._get_period_fields(period)
        details = self.general_audit_id.standard_detail_ids

        def signed(detail, field):
            """Return ``field`` of ``detail`` on the normal balance side."""
            sign = 1 if detail.type_id.normal_balance == "cr" else -1
            return sign * detail[field]

        def total(total_type):
            """Return the signed total of a ``total_formula`` total type."""
            return self._get_formula_total(total_type, closing_field, details)

        profit = total("profit_after_tax")
        oci = total("comprehensive_profit") - profit
        components = {}
        for component in self.env["general_audit_ws_b555edd.equity_component"].search(
            []
        ):
            matched = details.filtered(lambda d, c=component: d.type_id in c.type_ids)
            components[component.id] = (
                sum(signed(d, opening_field) for d in matched),
                sum(signed(d, closing_field) for d in matched),
            )
        return {"profit": profit, "oci": oci, "components": components}

    def _reload_equity(self):
        """Replace the equity lines with a fresh snapshot.

        One line per equity component for the current period, plus one
        per component for the previous period when the General Audit
        keeps a previous period. Owner transactions typed in before are
        lost, as the lines are created again.

        :return: None
        """
        self.ensure_one()
        self.equity_line_ids.unlink()
        periods = ["current"]
        if self.general_audit_id.need_previous:
            periods.append("previous")
        Line = self.env["general_audit_ws_b555edd.equity_line"]
        Component = self.env["general_audit_ws_b555edd.equity_component"]
        for period in periods:
            source = self._get_equity_source(period)
            for component in Component.search([]):
                opening, closing = source["components"].get(component.id, (0.0, 0.0))
                profit = source["profit"] if component.receive_profit else 0.0
                oci = source["oci"] if component.receive_oci else 0.0
                Line.create(
                    {
                        "worksheet_id": self.id,
                        "component_id": component.id,
                        "period": period,
                        "sequence": component.sequence,
                        "opening_balance": opening,
                        "profit": profit,
                        "oci": oci,
                        "closing_balance": closing + profit + oci,
                    }
                )

    _CASHFLOW_OPERATING_SECTIONS = (
        "operating_adjustment",
        "working_capital",
        "operating_other",
    )

    def _compute_cashflow_amounts(self, items, details, period):
        """Compute the amount of every calculated cash flow item.

        Balances are on the normal balance side of their account type,
        so a rise of an asset (debit normal) is a cash outflow and a
        rise of a liability or equity (credit normal) is a cash inflow.
        Manual and summary items are not computed here.

        :param items: ``general_audit_ws_b555edd.cashflow_item`` records
        :param details: standard details (anything with ``type_id`` and
            the balance fields)
        :param period: ``current`` or ``previous``
        :type period: str
        :return: ``{item id: amount}`` for the computed items
        :rtype: dict
        """
        self.ensure_one()
        opening_field, closing_field = self._get_period_fields(period)

        def closing(types):
            """Return the closing balance of the given account types."""
            return sum(d[closing_field] for d in details if d.type_id in types)

        def change(types):
            """Return the cash effect of the balance change of the types."""
            result = 0.0
            for detail in details:
                if detail.type_id in types:
                    delta = detail[closing_field] - detail[opening_field]
                    result += -delta if detail.type_id.normal_balance == "dr" else delta
            return result

        amounts = {}
        for item in items:
            sign = 1 if item.sign == "add" else -1
            if item.calc_type == "profit_before_tax":
                amount = self._get_formula_total(
                    "profit_before_tax", closing_field, details
                )
            elif item.calc_type == "pl_amount":
                amount = sign * closing(item.type_ids)
            elif item.calc_type == "balance_change":
                amount = sign * change(item.type_ids)
            elif item.calc_type == "capex":
                amount = sign * (
                    change(item.type_ids) - closing(item.reference_type_ids)
                )
            elif item.calc_type == "cash_opening":
                amount = sum(
                    d[opening_field] for d in details if d.type_id in item.type_ids
                )
            elif item.calc_type == "cash_closing_tb":
                amount = closing(item.type_ids)
            else:
                continue
            amounts[item.id] = amount
        return amounts

    def _get_cashflow_source(self, period):
        """Read the calculated cash flow amounts of one period.

        :param period: ``current`` or ``previous``
        :type period: str
        :return: ``{item id: amount}``, see ``_compute_cashflow_amounts``
        :rtype: dict
        """
        self.ensure_one()
        items = self.env["general_audit_ws_b555edd.cashflow_item"].search([])
        return self._compute_cashflow_amounts(
            items, self.general_audit_id.standard_detail_ids, period
        )

    def _reload_cashflow(self):
        """Replace the cash flow lines with a fresh snapshot.

        One line per cash flow item for the current period, plus one per
        item for the previous period when the General Audit keeps a
        previous period. Manual amounts typed in before are lost, as the
        lines are created again.

        :return: None
        """
        self.ensure_one()
        self.cashflow_line_ids.unlink()
        periods = ["current"]
        if self.general_audit_id.need_previous:
            periods.append("previous")
        Line = self.env["general_audit_ws_b555edd.cashflow_line"]
        items = self.env["general_audit_ws_b555edd.cashflow_item"].search([])
        for period in periods:
            amounts = self._get_cashflow_source(period)
            for item in items:
                Line.create(
                    {
                        "worksheet_id": self.id,
                        "item_id": item.id,
                        "period": period,
                        "sequence": item.sequence,
                        "amount": amounts.get(item.id, 0.0),
                    }
                )
        self._refresh_cashflow_totals()

    def _refresh_cashflow_totals(self):
        """Recompute the summary lines from the other lines of each period.

        Totals of the operating, investing and financing sections, the
        net change, the computed closing cash and the difference with
        the closing cash of the trial balance.

        :return: None
        """
        self.ensure_one()
        for period in ("current", "previous"):
            lines = self.cashflow_line_ids.filtered(lambda r, p=period: r.period == p)
            if not lines:
                continue

            def section_sum(sections, lines=lines):
                """Return the total of the lines of the given sections."""
                return sum(
                    line.amount
                    for line in lines
                    if line.section in sections and line.calc_type != "cash_opening"
                )

            by_type = {line.calc_type: line for line in lines}
            operating = section_sum(self._CASHFLOW_OPERATING_SECTIONS)
            investing = section_sum(("investing",))
            financing = section_sum(("financing",))
            net = operating + investing + financing
            opening = (
                by_type["cash_opening"].amount if "cash_opening" in by_type else 0.0
            )
            closing_tb = (
                by_type["cash_closing_tb"].amount
                if "cash_closing_tb" in by_type
                else 0.0
            )
            computed = opening + net
            values = {
                "operating_total": operating,
                "investing_total": investing,
                "financing_total": financing,
                "net_change": net,
                "cash_closing_computed": computed,
                "cash_difference": computed - closing_tb,
            }
            for calc_type, amount in values.items():
                if calc_type in by_type:
                    by_type[calc_type].amount = amount
