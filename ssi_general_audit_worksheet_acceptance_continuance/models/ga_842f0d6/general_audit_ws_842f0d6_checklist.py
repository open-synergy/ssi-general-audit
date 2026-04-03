# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWS842f0d6Checklist(models.Model):
    """Checklist value line for Money Laundering Issues (PMPJ) worksheet.

    Each record represents one evaluated checklist criterion within a
    ``general_audit_ws_842f0d6`` worksheet. Inherits ``mixin.checklist.value``
    which provides the response fields.

    In addition to the standard checklist fields, each line also contains:
    - ``none_below``: Flag indicating none of the sub-items below apply
    - ``item_ids``: Many2many link to ``general_audit_ws_842f0d6.item_categ``
      records that represent specific risk indicators under the selected item
    - ``allowed_item_ids``: Computed filter limiting available item categories
      to those matching the current checklist item's category

    Model: ``general_audit_ws_842f0d6.checklist``
    Parent worksheet: ``general_audit_ws_842f0d6``
    """

    _name = "general_audit_ws_842f0d6.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Money Laudring Issues (842f0d6) - Checklist"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_842f0d6",
        required=True,
        ondelete="cascade",
        help="""Reference to the parent worksheet (Money Laundering Issues).
Links this checklist line to its worksheet and ensures cascading deletion.""",
    )
    item_id = fields.Many2one(
        string="Checklist Item",
        comodel_name="general_audit_ws_842f0d6.item",
        required=True,
        help="The checklist question/criterion selected for this line.",
    )
    none_below = fields.Boolean(
        string="None of Below",
        default=False,
        help="""Tick if none of the items below apply.
When checked, the 'Items' field will be cleared.""",
    )

    @api.depends(
        "item_id",
    )
    def _compute_allowed_item_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_842f0d6.item_categ"]
            criteria = [
                ("categ", "=", record.item_id.categ),
            ]
            record.allowed_item_ids = obj.search(criteria).ids

    allowed_item_ids = fields.Many2many(
        string="Allowed Items",
        comodel_name="general_audit_ws_842f0d6.item_categ",
        compute="_compute_allowed_item_ids",
        store=False,
        help="""Dynamically computed set of item categories allowed
based on the selected checklist item.""",
    )
    item_ids = fields.Many2many(
        string="Items",
        comodel_name="general_audit_ws_842f0d6.item_categ",
        relation="rel_ga_842f0d6_item_2_item_categ",
        column1="item_id",
        column2="item_categ_id",
        help="Selected item categories evidencing potential money laundering indicators.",
    )
    option_id = fields.Many2one(
        string="Result",
        help="Result/option selected for this checklist line, based on the evaluation.",
    )

    @api.onchange("none_below")
    def onchange_item_ids(self):
        if self.none_below:
            self.item_ids = [(5, 0, 0)]
