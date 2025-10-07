# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSddf034cOwnership(models.Model):
    _name = "general_audit_ws_ddf034c.ownership"
    _description = "General Information and Legal Aspec (ddf034c) - " "Ownership"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ddf034c",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
    state = fields.Selection(
        related="worksheet_id.state",
    )
    ownership_location_id = fields.Many2one(
        string="Ownership Location",
        comodel_name="ownership_location",
    )
    ownership_state = fields.Selection(
        string="Status",
        selection=[
            ("owned", "Owned"),
            ("leased", "Leased"),
            ("other", "Others"),
        ],
    )
