# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc8740d4(models.Model):
    _name = "general_audit_ws_c8740d4"
    _description = "Preliminary Analytic Procedure (c8740d4)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_preliminary_analytic_procedure."
        "worksheet_type_c8740d4"
    )

    conclusion_ids = fields.One2many(
        string="Conclusion",
        comodel_name="general_audit_ws_c8740d4.analytic_procedure_conclusion",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
