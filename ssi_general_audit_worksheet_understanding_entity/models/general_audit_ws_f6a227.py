# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSf6a227(models.Model):
    _name = "general_audit_ws_f6a227"
    _description = "Understanding of Relevant Regulations (f6a227)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_f6a227"
    )

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_f6a227.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
