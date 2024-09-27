# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditAccountKeyInternalControl(models.Model):
    _name = "general_audit_account_key_internal_control"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Standard Account Key Internal Control"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
    account_type_id = fields.Many2one(
        string="Standard Account",
        comodel_name="client_account_type",
        required=True,
        ondelete="restrict",
    )
    control_activity_id = fields.Many2one(
        string="Control Activity",
        comodel_name="general_audit_control_activity",
        required=True,
        ondelete="restrict",
    )
    assersion_type_id = fields.Many2one(
        string="Assersion Type",
        comodel_name="general_audit_assersion_type",
        required=True,
        ondelete="restrict",
    )
