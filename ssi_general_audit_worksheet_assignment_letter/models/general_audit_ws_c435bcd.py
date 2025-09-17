# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc435bcd(models.Model):
    _name = "general_audit_ws_c435bcd"
    _description = "Assignment Letter (c435bcd)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_assignment_letter." "worksheet_type_c435bcd"
    )

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_c435bcd.checklist",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
