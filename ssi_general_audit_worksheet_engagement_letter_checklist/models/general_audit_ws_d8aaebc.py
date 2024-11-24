# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSD8AAEBC(models.Model):
    _name = "general_audit_ws_d8aaebc"
    _description = "Engagement Letter Checklist (d8aaebc)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_engagement_letter_checklist."
        "worksheet_type_d8aaebc"
    )

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_d8aaebc.checklist",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
