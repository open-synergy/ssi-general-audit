# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSfbf57ee(models.Model):
    _name = "general_audit_ws_fbf57ee"
    _description = "Going Concern (fbf57ee)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_specific_procedure." "worksheet_type_fbf57ee"
    )

    balance_type = fields.Selection(
        selection=[
            ("end_period", "End Period Balance"),
            ("interim", "Interim Balance"),
        ],
        string="Balance Type",
        required=True,
        default="end_period",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
        help="Type of balance to consider for the accounts.",
    )
    z_score_coefficient_set_id = fields.Many2one(
        comodel_name="general_audit_going_concern_z_score_coeficient_set",
        string="Z-Score Coefficient Set",
        required=True,
        ondelete="restrict",
        help="Z-Score Coefficient Set used in the going concern analysis.",
        readonly=True,
        states={"draft": [("readonly", False)], "open": [("readonly", False)]},
    )
    computation_line_ids = fields.One2many(
        comodel_name="general_audit_ws_fbf57ee.computation",
        inverse_name="worksheet_id",
        string="Computation Lines",
        help="List of computation lines related to this worksheet.",
        readonly=True,
        states={"draft": [("readonly", False)], "open": [("readonly", False)]},
    )
    z_score = fields.Float(
        string="Z-Score",
        digits=(16, 2),
        compute="_compute_z_score",
        store=True,
        compute_sudo=True,
    )
    z_score_category = fields.Selection(
        selection=[
            ("solvent", "Solvent"),
            ("grey_area", "Grey Area"),
            ("unsolvent", "Unsolvent"),
        ],
        string="Z-Score Category",
        compute="_compute_z_score",
        store=True,
        compute_sudo=True,
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

    @api.depends(
        "computation_line_ids.result",
        "computation_line_ids",
    )
    def _compute_z_score(self):
        for record in self:
            total_z_score = 0.0
            for line in record.computation_line_ids:
                total_z_score += line.result
            record.z_score = total_z_score

            # Determine Z-Score Category
            if total_z_score >= 2.90:
                record.z_score_category = "solvent"
            elif 1.23 <= total_z_score < 2.90:
                record.z_score_category = "grey_area"
            else:
                record.z_score_category = "unsolvent"

    def action_load_confirmation_procedure(self):
        for record in self.sudo():
            record._load_confirmation_procedure()

    def action_load_analysis(self):
        for record in self.sudo():
            record._load_analysis()

    def action_load_computation(self):
        for record in self.sudo():
            record._load_computation_lines()

    def _load_computation_lines(self):
        self.ensure_one()
        self.computation_line_ids.unlink()

        criteria = [
            ("general_audit_id", "=", self.general_audit_id.id),
            ("computation_item_id.going_concern_ok", "=", True),
        ]
        general_audit_computations = self.env["general_audit.computation"].search(
            criteria
        )

        for computation in general_audit_computations:
            coefficient = 0.0
            z_score_set = self.z_score_coefficient_set_id
            if z_score_set:
                item = z_score_set.item_ids.filtered(
                    lambda l: l.computation_item_id.id
                    == computation.computation_item_id.id
                )
                if item:
                    coefficient = item[0].coefficient
            self.env["general_audit_ws_fbf57ee.computation"].create(
                {
                    "worksheet_id": self.id,
                    "general_audit_computation_id": computation.id,
                    "coefficient": coefficient,
                }
            )

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
