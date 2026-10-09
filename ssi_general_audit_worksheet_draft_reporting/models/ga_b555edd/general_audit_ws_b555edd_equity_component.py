# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsB555eddEquityComponent(models.Model):
    """Report Formatting Control (b555edd) - Equity Component.

    Master data of one row of the Statement of Changes in Equity, for
    example Share Capital or Retained Earnings. Each component lists
    the standard account types whose balances make it up, and says
    whether the profit and the other comprehensive income (OCI) of the
    period are allocated to it. Seeded by ``data/master``; one global
    set serves every General Audit.
    """

    _name = "general_audit_ws_b555edd.equity_component"
    _description = "Report Formatting Control (b555edd) - Equity Component"
    _order = "sequence, id"

    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the equity component shown on the statement.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        help="Display order of the component on the statement.",
    )
    type_ids = fields.Many2many(
        comodel_name="client_account_type",
        relation="ga_b555edd_equity_component_type_rel",
        column1="component_id",
        column2="type_id",
        string="Account Types",
        help="Standard account types whose balances form this component.",
    )
    receive_profit = fields.Boolean(
        string="Receive Profit",
        help=(
            "Profit of the period is allocated to this component. "
            "Flag exactly one component, otherwise the profit is "
            "counted more than once."
        ),
    )
    receive_oci = fields.Boolean(
        string="Receive OCI",
        help=(
            "Other comprehensive income of the period is allocated to "
            "this component. Flag exactly one component."
        ),
    )
