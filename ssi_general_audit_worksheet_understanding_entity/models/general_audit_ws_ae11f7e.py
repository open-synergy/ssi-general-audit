# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSae11f7e(models.Model):
    _name = "general_audit_ws_ae11f7e"
    _description = "Main Business Activity Process (ae11f7e)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_ae11f7e"
    )

    business_cycle_ids = fields.Many2many(
        string="Business Cycles",
        related="general_audit_id.business_cycle_ids",
        inverse="_inverse_business_cycle_ids",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    other_report_ids = fields.Many2many(
        string="Other Reports",
        related="general_audit_id.other_report_ids",
        inverse="_inverse_other_report_ids",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    expert_ids = fields.One2many(
        string="Experts",
        comodel_name="general_audit_ws_ae11f7e.expert",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    previous_audit_information_ids = fields.One2many(
        string="Previous Significant Audit Information",
        comodel_name="general_audit_ws_ae11f7e.previous_audit_information",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    previous_other_information_ids = fields.One2many(
        string="Previous Significant Other Information",
        comodel_name="general_audit_ws_ae11f7e.previous_other_information",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    other_information_ids = fields.One2many(
        string="Other Significant Information",
        comodel_name="general_audit_ws_ae11f7e.other_information",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    def _inverse_business_cycle_ids(self):
        for record in self:
            record.general_audit_id.write(
                {
                    "business_cycle_ids": [(6, 0, self.business_cycle_ids.ids)],
                }
            )

    def _inverse_other_report_ids(self):
        for record in self:
            record.general_audit_id.write(
                {
                    "other_report_ids": [(6, 0, self.other_report_ids.ids)],
                }
            )
