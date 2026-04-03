# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class OwnershipLocation(models.Model):
    """Master: Ownership Location.

    Reference list of location types or specific sites (e.g., Head Office,
    Branch Office, Warehouse, Factory) relevant to the entity's operations.
    Used in the General Information and Legal Aspect worksheet (ddf034c) to
    document the entity's ownership or lease status at each location as part
    of ISA 315 entity understanding.
    """

    _name = "ownership_location"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Ownership Location"

    code = fields.Char(
        default="/",
    )
