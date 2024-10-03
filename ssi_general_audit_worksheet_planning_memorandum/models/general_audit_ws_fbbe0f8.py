# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSfbbe0f8(models.Model):
    _name = "general_audit_ws_fbbe0f8"
    _description = "Audit Planning Memorandum (fbbe0f8)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_planning_memorandum." "worksheet_type_fbbe0f8"
    )

    financial_accounting_standard_id = fields.Many2one(
        related="general_audit_id.financial_accounting_standard_id",
    )
    other_report_ids = fields.Many2many(
        related="general_audit_id.other_report_ids",
    )
    expert_type_ids = fields.Many2many(
        related="general_audit_id.expert_type_ids",
    )
