# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS09253fe(models.Model):
    _name = "general_audit_ws_09253fe"
    _description = "Independence Letter (09253fe)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_independence_statement." "worksheet_type_09253fe"
    )

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_09253fe.checklist",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
