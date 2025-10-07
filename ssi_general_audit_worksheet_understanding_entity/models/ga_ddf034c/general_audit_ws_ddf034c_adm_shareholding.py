# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSddf034cAdmShareholding(models.Model):
    _name = "general_audit_ws_ddf034c.adm_shareholding"
    _description = (
        "General Information and Legal Aspec (ddf034c) - "
        "Shareholding Structure (Amendment)"
    )
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
    shareholder_name = fields.Char(
        string="Name",
    )
    shareholder_number = fields.Integer(
        string="Number",
    )
