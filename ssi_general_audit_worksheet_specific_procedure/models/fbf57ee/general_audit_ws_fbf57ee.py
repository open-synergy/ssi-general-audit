# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSfbf57ee(models.Model):
    """WS: Going Concern (fbf57ee) — ISA 570.

    This worksheet assesses the client's ability to continue as a going concern
    in accordance with ISA 570. The auditor evaluates:

    - Going concern indicators (financial, operational, and other factors).
    - Altman Z-Score computation using trial balance computation items and
      configurable coefficient sets.
    - Confirmation procedures to gather additional evidence.

    The Z-Score analysis provides a quantitative basis for the going concern
    assessment, supplementing the qualitative indicator review. The auditor
    concludes on whether material uncertainty exists and determines the
    appropriate reporting response.
    """

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
        required=False,
        ondelete="restrict",
        help="Z-Score Coefficient Set used in the going concern analysis.",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False), ("required", True)],
        },
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
        help="Computed Altman Z-Score based on the worksheet’s computation lines.",
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
        help="Category derived from the Z-Score threshold (Solvent/Grey Area/Unsolvent).",
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
        """Synchronise ``computation_line_ids`` with the audit.

        Lines are matched by ``general_audit_computation_id`` against the
        computations of ``general_audit_id`` whose item is flagged for
        going concern. A computation without a line gets one, with the
        coefficient of the selected Z-Score coefficient set. The lines
        of computations that no longer qualify are removed. Other lines
        are not rewritten, so a coefficient changed by the auditor is
        kept, and their stored amount and result are refreshed.

        :return: nothing; adds, removes and refreshes computation lines
        """
        self.ensure_one()
        Computation = self.env["general_audit_ws_fbf57ee.computation"]

        criteria = [
            ("general_audit_id", "=", self.general_audit_id.id),
            ("computation_item_id.going_concern_ok", "=", True),
        ]
        wanted = self.env["general_audit.computation"].search(criteria)

        obsolete = self.computation_line_ids.filtered(
            lambda line: line.general_audit_computation_id not in wanted
        )
        obsolete.unlink()
        kept = self.computation_line_ids - obsolete

        for computation in wanted - kept.mapped("general_audit_computation_id"):
            coefficient = 0.0
            z_score_set = self.z_score_coefficient_set_id
            if z_score_set:
                item = z_score_set.item_ids.filtered(
                    lambda l, c=computation: l.computation_item_id.id
                    == c.computation_item_id.id
                )
                if item:
                    coefficient = item[0].coefficient
            Computation.create(
                {
                    "worksheet_id": self.id,
                    "general_audit_computation_id": computation.id,
                    "coefficient": coefficient,
                }
            )
        kept._refresh_computed_columns()

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

        all_procedures = self.env[
            "general_audit_going_concern_confirmation_procedure"
        ].search([])
        existing_procedures = self.confirmation_procedure_line_ids.mapped(
            "confirmation_procedure_id"
        )
        procedures_to_add = all_procedures - existing_procedures
        procedures_to_remove = existing_procedures - all_procedures

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
