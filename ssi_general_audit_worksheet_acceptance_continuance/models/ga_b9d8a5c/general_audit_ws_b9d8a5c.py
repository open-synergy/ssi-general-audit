# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb9d8a5c(models.Model):
    _name = "general_audit_ws_b9d8a5c"
    _description = (
        "Competency, Availability and Independency " "Of Assignment Team (b9d8a5c)"
    )
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_b9d8a5c"
    )

    personnel_ids = fields.One2many(
        string="List of Personnel",
        comodel_name="general_audit_ws_b9d8a5c.personnel",
        inverse_name="worksheet_id",
    )
    competency_analysis_ids = fields.One2many(
        string="Competency Analysis",
        comodel_name="general_audit_ws_b9d8a5c.competency",
        inverse_name="worksheet_id",
    )
    availability_analysis_ids = fields.One2many(
        string="Availability Analysis",
        comodel_name="general_audit_ws_b9d8a5c.availability",
        inverse_name="worksheet_id",
    )
    independency_analysis_ids = fields.One2many(
        string="Independency Analysis",
        comodel_name="general_audit_ws_b9d8a5c.independency",
        inverse_name="worksheet_id",
    )
    summary_ids = fields.One2many(
        string="Summary",
        comodel_name="general_audit_ws_b9d8a5c.summary",
        inverse_name="worksheet_id",
    )
