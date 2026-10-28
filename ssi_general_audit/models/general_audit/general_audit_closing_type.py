# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditClosingType(models.Model):
    """General Audit Closing Type.

    Master data that groups the mappings used to generate the closing
    lines of a General Audit, for example closing the profit and loss
    groups into retained earnings and the other comprehensive income
    groups into other equity.
    """

    _name = "general_audit_closing_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Closing Type"

    mapping_ids = fields.One2many(
        string="Mapping(s)",
        comodel_name="general_audit_closing_type.mapping",
        inverse_name="closing_type_id",
        help="Mappings evaluated in sequence order to build closing lines.",
    )
