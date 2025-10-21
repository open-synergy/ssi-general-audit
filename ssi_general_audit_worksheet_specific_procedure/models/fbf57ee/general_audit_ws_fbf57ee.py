# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSfbf57ee(models.Model):
    _name = "general_audit_ws_fbf57ee"
    _description = "Going Concern (fbf57ee)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_specific_procedure." "worksheet_type_fbf57ee"
    )

    confirmation_procedure_line_ids = fields.One2many(
        comodel_name="general_audit_ws_fbf57ee.confirmation_procedure",
        inverse_name="worksheet_id",
        string="Confirmation Procedures",
        help="List of confirmation procedures related to this worksheet.",
        readonly=True,
        states={"draft": [("readonly", False)], "open": [("readonly", False)]},
    )
    analysis_line_ids = fields.One2many(
        comodel_name="general_audit_ws_fbf57ee.analysis",
        inverse_name="worksheet_id",
        string="Analysis Lines",
        help="List of analysis lines related to this worksheet.",
        readonly=True,
        states={"draft": [("readonly", False)], "open": [("readonly", False)]},
    )

    def action_load_confirmation_procedure(self):
        for record in self.sudo():
            record._load_confirmation_procedure()

    def action_load_analysis(self):
        for record in self.sudo():
            record._load_analysis()

    def _load_analysis(self):
        self.ensure_one()

        all_going_concerns = self.env["general_audit_going_concern"].search([])
        existing_going_concerns = self.analysis_line_ids.mapped("going_concern_id")
        going_concerns_to_add = all_going_concerns - existing_going_concerns
        going_concerns_to_remove = existing_going_concerns - all_going_concerns

        # Add new going concerns
        for going_concern in going_concerns_to_add:
            self.env["general_audit_ws_fbf57ee.analysis"].create(
                {
                    "worksheet_id": self.id,
                    "going_concern_id": going_concern.id,
                }
            )

        # Remove old going concerns
        for going_concern in going_concerns_to_remove:
            self.env["general_audit_ws_fbf57ee.analysis"].search(
                [
                    ("worksheet_id", "=", self.id),
                    ("going_concern_id", "=", going_concern.id),
                ]
            ).unlink()

    def _load_confirmation_procedure(self):
        self.ensure_one()

        all_procesures = self.env[
            "general_audit_going_concern_confirmation_procedure"
        ].search([])
        existing_procedures = self.confirmation_procesure_line_ids.mapped(
            "confirmation_procedure_id"
        )
        procedures_to_add = all_procesures - existing_procedures
        procedures_to_remove = existing_procedures - all_procesures

        # Add new procedures
        for procedure in procedures_to_add:
            self.env["general_audit_ws_fbf57ee.confirmation_procedure"].create(
                {
                    "worksheet_id": self.id,
                    "confirmation_procedure_id": procedure.id,
                }
            )

        # Remove old procedures
        for procedure in procedures_to_remove:
            self.env["general_audit_ws_fbf57ee.confirmation_procedure"].search(
                [
                    ("worksheet_id", "=", self.id),
                    ("confirmation_procedure_id", "=", procedure.id),
                ]
            ).unlink()
