# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS842f0d6Item(models.Model):
    """Master data: Risk indicator category for Money Laundering Issues worksheet.

    Defines the granular risk indicators (sub-items) that can be selected
    against a checklist criterion in the ``general_audit_ws_842f0d6.checklist``
    model. Each category record belongs to one of four risk dimensions
    (``categ``):

    - ``profile``: Client identity / beneficial ownership indicators
    - ``country``: High-risk jurisdiction indicators
    - ``business``: High-risk business sector indicators
    - ``product``: High-risk product or service indicators

    These records are filtered dynamically when evaluating a checklist line
    via the ``allowed_item_ids`` computed field.

    Model: ``general_audit_ws_842f0d6.item_categ``
    """

    _name = "general_audit_ws_842f0d6.item_categ"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Money Laudring Issues (842f0d6) - " "Checklist Item Category"

    code = fields.Char(
        default="/",
        help="Internal code for the item category. Defaults to '/'.",
    )
    categ = fields.Selection(
        string="Category",
        selection=[
            ("profile", "Profile"),
            ("country", "Country"),
            ("business", "Business"),
            ("product", "Product/Service"),
        ],
        help="""Classification/category of the indicator
(Profile, Country, Business, Product/Service).""",
    )
