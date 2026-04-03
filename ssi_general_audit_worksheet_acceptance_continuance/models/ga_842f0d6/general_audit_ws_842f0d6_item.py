# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS842f0d6Item(models.Model):
    """Master data: Checklist item template for Money Laundering Issues worksheet.

    Defines the predefined risk criteria used in the checklist of the
    ``general_audit_ws_842f0d6`` worksheet. Inherits ``mixin.checklist.item``
    providing item title, option set, and scoring.

    Each item belongs to one of four risk categories (``categ``):
    - ``profile``: Client identity / ownership risk factors
    - ``country``: Jurisdictional / geographic risk factors
    - ``business``: Industry / business sector risk factors
    - ``product``: Product or service-related risk factors

    The category is used to filter the applicable ``item_categ`` records
    in the checklist line.

    Model: ``general_audit_ws_842f0d6.item``
    """

    _name = "general_audit_ws_842f0d6.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Money Laudring Issues (842f0d6) - " "Checklist Item"

    code = fields.Char(
        default="/",
        help="Internal code/identifier for the checklist item. Defaults to '/'.",
    )
    categ = fields.Selection(
        string="Category",
        selection=[
            ("profile", "Profile"),
            ("country", "Country"),
            ("business", "Business"),
            ("product", "Product/Service"),
        ],
        help="""Category under which the checklist item falls
(Profile, Country, Business, Product/Service).""",
    )
