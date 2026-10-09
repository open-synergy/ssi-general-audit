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

    def action_reload_account(self):
        """Refill the detail lines from the General Audit standard details.

        :return: None
        """
        for record in self.sudo():
            record._reload_account()

    def _reload_account(self):
        """Replace the detail and equity lines with fresh ones.

        Every standard account type of the General Audit gets a line,
        whether it belongs to the financial position or to the
        comprehensive income statement. Existing lines are removed
        first, so clicking Reload again never duplicates lines. The
        equity lines are rebuilt as well, see ``_reload_equity()``.

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
        if period == "current":
            opening_field, closing_field = (
                "home_statement_opening_balance",
                "audited_balance",
            )
        else:
            opening_field, closing_field = (
                "previous_opening_balance",
                "previous_balance",
            )
        details = self.general_audit_id.standard_detail_ids

        def signed(detail, field):
            """Return ``field`` of ``detail`` on the normal balance side."""
            sign = 1 if detail.type_id.normal_balance == "cr" else -1
            return sign * detail[field]

        formula_model = self.env["general_audit_ws_ff42fdc.total_formula"].sudo()

        def total(total_type):
            """Return the signed total of a ``total_formula`` total type."""
            amount = 0.0
            for formula in formula_model.search([("total_type", "=", total_type)]):
                sign = 1 if formula.sign == "add" else -1
                amount += sign * sum(
                    detail[closing_field]
                    for detail in details
                    if detail.type_id.group_id == formula.group_id
                )
            return amount

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
