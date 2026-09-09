# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsFf42fdcTotalFormula(models.Model):
    """Worksheet (ff42fdc) - Total Formula.

    Configurable master data replacing the Python-hardcoded
    ``_TOTAL_TYPE_FORMULA`` dictionary previously used by
    ``general_audit_ws_ff42fdc.posture`` to compute its nine Total
    rows. Each record contributes one ``client_account_group``
    (referenced by relation, never by its ``code`` string) to one
    ``total_type``, with a sign. ``_compute_amounts`` on the posture
    line sums the matching ``general_audit.detail`` amounts of every
    contributing group. Scope is global: one set of formulas applies
    to every General Audit engagement.
    """

    _name = "general_audit_ws_ff42fdc.total_formula"
    _description = "Worksheet (ff42fdc) - Total Formula"
    _order = "total_type, sequence, id"

    total_type = fields.Selection(
        string="Total Type",
        selection=[
            ("total_asset", "Total Asset"),
            ("total_liability", "Total Liability"),
            ("total_equity", "Total Equity"),
            ("total_liability_equity", "Total Liability and Equity"),
            ("gross_profit", "Gross Profit"),
            ("operating_profit", "Operating Profit"),
            ("profit_before_tax", "Profit Before Tax"),
            ("profit_after_tax", "Profit After Tax"),
            ("comprehensive_profit", "Comprehensive Profit"),
        ],
        required=True,
        help="Which fixed Total/Subtotal row this component " "contributes to.",
    )
    group_id = fields.Many2one(
        comodel_name="client_account_group",
        string="Account Group",
        required=True,
        ondelete="restrict",
        help="Client account group contributing to the Total row. "
        "Referenced by relation, so renaming the group's code or "
        "name never breaks the formula.",
    )
    sign = fields.Selection(
        string="Sign",
        selection=[
            ("add", "+"),
            ("subtract", "-"),
        ],
        required=True,
        default="add",
        help="Whether this group's amount is added to or subtracted "
        "from the Total row.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Display order of this component within its Total "
        "Type's configuration screen. Unrelated to the ``sequence`` "
        "field on ``general_audit_ws_ff42fdc.posture``.",
    )
