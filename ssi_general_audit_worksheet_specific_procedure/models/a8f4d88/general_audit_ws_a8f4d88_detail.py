# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa8f4d88Detail(models.Model):
    """Detail line for the Accounting Estimation worksheet (a8f4d88).

    Each line represents one account type being assessed for accounting estimation.
    The auditor records the estimation method applicable to that account type and
    identifies any external experts (e.g., actuaries, valuators) involved in the
    estimation process, as required by ISA 540.
    """

    _name = "general_audit_ws_a8f4d88.detail"
    _description = "Accounting Estimation (a8f4d88) - Detail"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_a8f4d88",
        string="Worksheet",
        required=True,
        ondelete="cascade",
        help="Parent Accounting Estimation worksheet for this detail line.",
    )
    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Standard Account",
        required=True,
        ondelete="restrict",
        help="Standard account type being assessed for accounting estimation.",
    )
    expert_ids = fields.Many2many(
        comodel_name="general_audit_expert_type",
        string="Experts Involved",
        help="Experts involved in the assessment of the accounting estimation (if any).",
    )
    estimation_method_ids = fields.Many2many(
        comodel_name="general_audit_accounting_estimation_method",
        string="Estimation Methods Used",
        relation="rel_general_audit_ws_a8f4d88_detail_2_acc_est_method",
        column1="detail_id",
        column2="estimation_method_id",
        required=True,
        help="Accounting estimation methods applied for this account type.",
    )
    relevant_control_id = fields.Many2one(
        comodel_name="general_audit_control_activity",
        string="Relevant Controls",
        relation="rel_general_audit_ws_a8f4d88_detail_2_acc_est_relevant_control",
        column1="detail_id",
        column2="relevant_control_id",
        required=True,
        help="Control activity relevant to the accounting estimation process.",
    )
    fair_value_measurement_level = fields.Selection(
        selection=[
            ("level_1", "Level 1"),
            ("level_2", "Level 2"),
            ("level_3", "Level 3"),
        ],
        string="Fair Value Measurement Level",
        required=True,
        help="IFRS fair value hierarchy level used for the measurement (Level 1/2/3).",
    )
    assumption = fields.Text(
        string="Key Assumptions",
        required=True,
        help="Key assumptions underlying the accounting estimation.",
    )
    reference = fields.Char(
        string="Reference",
        required=True,
        help="References to supporting documentation or working papers.",
    )
    conclusion = fields.Text(
        string="Conclusion",
        required=True,
        help="Auditor’s conclusion regarding the reasonableness of the estimation.",
    )
