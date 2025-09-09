# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSba9b2f0RiskIdentification(models.Model):
    _name = "general_audit_ws_ba9b2f0.risk_identification"
    _description = "Worksheet ba9b2f0 - Risk Identification"
    _order = "worksheet_id, detail_id, sequence, id"

    detail_id = fields.Many2one(
        string="Detail",
        comodel_name="general_audit_ws_ba9b2f0.detail",
        required=True,
        ondelete="cascade",
    )
    worksheet_id = fields.Many2one(
        related="detail_id.worksheet_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    name = fields.Char(
        string="Risk Identification",
        required=True,
    )
