# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


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

    closing_line_ids = fields.One2many(
        string="Closing Line(s)",
        comodel_name="general_audit.closing_line",
        related="general_audit_id.closing_line_ids",
        readonly=True,
        help="Closing journal lines of the General Audit.",
    )
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

    def action_reload_account(self):
        """Refill the detail lines from the General Audit standard details.

        :return: None
        """
        for record in self.sudo():
            record._reload_account()

    def _reload_account(self):
        """Synchronise the detail, equity and cash flow lines.

        Every standard account type of the General Audit gets a line,
        whether it belongs to the financial position or to the
        comprehensive income statement. Lines are matched on
        ``standard_detail_id``: missing ones are created, ones whose
        standard detail is gone are removed and the others only get
        their ``sequence`` refreshed, so clicking Reload again never
        duplicates lines. The equity and cash flow lines are
        synchronised as well, see ``_reload_equity()`` and
        ``_reload_cashflow()``.

        :return: None
        """
        self.ensure_one()
        standard_details = self.general_audit_id.standard_detail_ids
        existing = self._index_lines(
            self.detail_ids, lambda line: line.standard_detail_id.id
        )
        self.detail_ids.filtered(
            lambda line: line.standard_detail_id not in standard_details
        ).unlink()
        Detail = self.env["general_audit_ws_b555edd.detail"]
        for standard_detail in standard_details:
            type_ = standard_detail.type_id
            sequence = type_.group_id.sequence * 1000 + type_.sequence
            line = existing.get(standard_detail.id)
            if line:
                line.sequence = sequence
            else:
                Detail.create(
                    {
                        "worksheet_id": self.id,
                        "standard_detail_id": standard_detail.id,
                        "sequence": sequence,
                    }
                )
        self._reload_equity()
        self._reload_cashflow()

    def _index_lines(self, lines, key):
        """Index lines by a key, removing the duplicates of a key.

        Only the first line of each key is kept, so a worksheet that
        somehow holds two lines for the same key is repaired by Reload.

        :param lines: lines of this worksheet
        :param key: function returning the matching key of a line
        :return: ``{key: first line with that key}``
        :rtype: dict
        """
        indexed = {}
        duplicates = lines.browse()
        for line in lines:
            if key(line) in indexed:
                duplicates |= line
            else:
                indexed[key(line)] = line
        duplicates.unlink()
        return indexed

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

    def _get_lead_schedule_worksheet(self):
        """Find the Worksheet (b26d482) the equity closing is read from.

        It is the newest Worksheet of the same General Audit that is
        neither cancelled nor rejected and has detail lines.

        :return: ``general_audit_ws_b26d482`` record, empty when the
            audit has no usable Worksheet
        :rtype: recordset
        """
        self.ensure_one()
        return self.env[
            "general_audit_ws_ff42fdc.posture"
        ]._get_lead_schedule_worksheet(self.general_audit_id)

    def _get_worksheet_equity_closing(self, worksheet):
        """Read the closing balance of every equity component.

        The balance of a component is the Balance Sheet column of the
        Worksheet lines whose account has one of the component's types,
        plus the closing of those types that no account receives. The
        Worksheet shows an amount positive on the normal balance side of
        its account, so a debit-normal type (for example treasury
        shares) counts negative, like the other equity figures.

        :param worksheet: ``general_audit_ws_b26d482`` record
        :return: ``{component id: closing balance}``
        :rtype: dict
        """
        receivers, amounts = worksheet._get_closing_allocation()
        type_model = self.env["client_account_type"]
        result = {}
        for component in self.env["general_audit_ws_b555edd.equity_component"].search(
            []
        ):
            total = 0.0
            for detail in worksheet.detail_ids:
                account = detail.account_id
                if account.type_id in component.type_ids:
                    sign = 1 if account.normal_balance == "cr" else -1
                    total += sign * detail.balance_sheet
            for type_id, amount in amounts.items():
                account_type = type_model.browse(type_id)
                if type_id not in receivers and account_type in component.type_ids:
                    sign = 1 if account_type.normal_balance == "cr" else -1
                    total += sign * amount
            result[component.id] = total
        return result

    def _get_equity_source(self, period):
        """Read the equity figures of one period from the standard details.

        Balances are taken with the sign of each account type's normal
        balance side, so equity reads as a positive amount. Profit is
        the ``profit_after_tax`` total and OCI the ``comprehensive_
        profit`` total minus it, both from the signed groups of
        ``general_audit_ws_ff42fdc.total_formula``.

        For the current period, the closing balance of every component
        is read from the Worksheet (b26d482) when the audit has one, see
        ``_get_worksheet_equity_closing()``; the Worksheet already holds
        the profit and OCI closing. The previous period has no Worksheet.

        :param period: ``current`` or ``previous``
        :type period: str
        :return: ``{"profit": float, "oci": float, "components":
            {component id: (opening, closing before profit and OCI)},
            "closing_total": {component id: closing balance}}``; the
            last one is empty without a Worksheet
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
        closing_total = {}
        if period == "current":
            worksheet = self._get_lead_schedule_worksheet()
            if worksheet:
                closing_total = self._get_worksheet_equity_closing(worksheet)
        return {
            "profit": profit,
            "oci": oci,
            "components": components,
            "closing_total": closing_total,
        }

    def _reload_equity(self):
        """Synchronise the equity lines with the General Audit.

        One line per equity component for the current period, plus one
        per component for the previous period when the General Audit
        keeps a previous period. Lines are matched on the component and
        period: missing ones are created and the ones no longer needed
        (for example ``previous`` after ``need_previous`` is switched
        off) are removed. On a kept line only the source columns are
        refreshed; ``issuance``, ``treasury``, ``reserve`` and
        ``dividend`` typed in by the auditor are never written. The
        current closing balance comes from the Worksheet when there is
        one, otherwise it is the standard detail balance plus profit
        and OCI.

        :return: None
        """
        self.ensure_one()
        periods = ["current"]
        if self.general_audit_id.need_previous:
            periods.append("previous")
        Line = self.env["general_audit_ws_b555edd.equity_line"]
        components = self.env["general_audit_ws_b555edd.equity_component"].search([])
        existing = self._index_lines(
            self.equity_line_ids, lambda line: (line.component_id.id, line.period)
        )
        self.equity_line_ids.filtered(
            lambda line: line.period not in periods
            or line.component_id not in components
        ).unlink()
        for period in periods:
            source = self._get_equity_source(period)
            for component in components:
                opening, closing = source["components"].get(component.id, (0.0, 0.0))
                profit = source["profit"] if component.receive_profit else 0.0
                oci = source["oci"] if component.receive_oci else 0.0
                closing_total = source.get("closing_total", {})
                if component.id in closing_total:
                    closing_balance = closing_total[component.id]
                else:
                    closing_balance = closing + profit + oci
                values = {
                    "sequence": component.sequence,
                    "opening_balance": opening,
                    "profit": profit,
                    "oci": oci,
                    "closing_balance": closing_balance,
                }
                line = existing.get((component.id, period))
                if line:
                    line.write(values)
                else:
                    values.update(
                        {
                            "worksheet_id": self.id,
                            "component_id": component.id,
                            "period": period,
                        }
                    )
                    Line.create(values)

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
        """Synchronise the cash flow lines with the General Audit.

        One line per cash flow item for the current period, plus one per
        item for the previous period when the General Audit keeps a
        previous period. Lines are matched on the item and period:
        missing ones are created and the ones no longer needed are
        removed. On a kept line the ``amount`` is refreshed from the
        source, except for ``manual`` and ``fx_effect`` items, whose
        typed-in amount is never written. The summary lines are
        recomputed at the end.

        :return: None
        """
        self.ensure_one()
        periods = ["current"]
        if self.general_audit_id.need_previous:
            periods.append("previous")
        Line = self.env["general_audit_ws_b555edd.cashflow_line"]
        items = self.env["general_audit_ws_b555edd.cashflow_item"].search([])
        existing = self._index_lines(
            self.cashflow_line_ids, lambda line: (line.item_id.id, line.period)
        )
        self.cashflow_line_ids.filtered(
            lambda line: line.period not in periods or line.item_id not in items
        ).unlink()
        for period in periods:
            amounts = self._get_cashflow_source(period)
            for item in items:
                values = {"sequence": item.sequence}
                line = existing.get((item.id, period))
                if line:
                    if item.calc_type not in ("manual", "fx_effect"):
                        values["amount"] = amounts.get(item.id, 0.0)
                    line.write(values)
                else:
                    values.update(
                        {
                            "worksheet_id": self.id,
                            "item_id": item.id,
                            "period": period,
                            "amount": amounts.get(item.id, 0.0),
                        }
                    )
                    Line.create(values)
        self._refresh_cashflow_totals()

    def _refresh_cashflow_totals(self):
        """Recompute the summary lines from the other lines of each period.

        Totals of the operating, investing and financing sections, the
        net change, the computed closing cash and the difference with
        the closing cash of the trial balance. The typed-in exchange
        rate effect is added to the computed closing cash but is not
        part of the net change.

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
            fx_effect = by_type["fx_effect"].amount if "fx_effect" in by_type else 0.0
            computed = opening + net + fx_effect
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
