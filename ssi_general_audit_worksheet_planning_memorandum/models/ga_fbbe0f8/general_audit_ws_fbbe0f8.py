# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from functools import lru_cache

from lxml import etree

from odoo import _, api, fields, models


class GeneralAuditWSfbbe0f8(models.Model):
    """
    WS: Audit Planning Memorandum — Detail Summary (fbbe0f8) — ISA 300 / SA 300.

    A consolidated partner-reviewable narrative that aggregates key information
    from multiple upstream worksheets into a single Audit Planning Memorandum
    document.  This worksheet is the "cover page" of the planning phase and
    is intended to be reviewed and approved by the Engagement Partner before
    fieldwork commences.

    The following information is pulled from linked upstream worksheets:

    * **Business environment** (``link_1_ids``) — IT environment details,
      IT risk review, regulatory/legal environment review, and amendment
      review notes.
    * **Business cycles** (``link_2_ids``) — Significant transaction cycles,
      assigned team members, estimated transaction volumes, and entities
      flagged for unannounced audit.
    * **Preliminary materiality** (``link_3_ids``) — Overall materiality (OM),
      performance materiality (PM), and tolerable misstatement (TM).
    * **Specific materiality** (``link_4_ids``) — Material account type
      mappings.
    * **Inherent risk finance** (``link_5_id``) — Review note.
    * **Team preliminary engagement** (``link_6_id``) — Review note.
    * **Understanding of the entity** (``link_7_id``) — Prior auditor history,
      other services provided, prior audit evidence, and other evidence.

    Dynamic field labels are generated from the ``general_audit_ws_a753ab9``
    checklist items via ``get_dynamic_labels()`` (LRU-cached), allowing the
    form view to reflect the custom planning area labels configured in the item
    master without modifying XML.
    """

    _name = "general_audit_ws_fbbe0f8"
    _description = "Audit Planning Memorandum - Detail (fbbe0f8)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_planning_memorandum." "worksheet_type_fbbe0f8"
    )
    _label_exceptions = [
        "id",
        "create_uid",
        "create_date",
        "write_uid",
        "write_date",
        "display_name",
        "note",
    ]

    financial_accounting_standard_id = fields.Many2one(
        related="general_audit_id.financial_accounting_standard_id",
        compute_sudo=True,
        store=True,
    )
    other_report_ids = fields.Many2many(
        related="general_audit_id.other_report_ids",
        compute_sudo=True,
        relation="rel_ga_ws_fbbe0f8_2_ga_other_report",
        column1="ws_fbbe0f8_id",
        column2="other_report_id",
        store=True,
    )
    expert_type_ids = fields.Many2many(
        related="general_audit_id.expert_type_ids",
        compute_sudo=True,
        relation="rel_ga_ws_fbbe0f8_2_ga_expert_type",
        column1="ws_fbbe0f8_id",
        column2="expert_type_id",
        store=True,
    )

    @api.depends(
        "link_1_ids",
    )
    def _compute_it_detail_review_ids(self):
        for record in self:
            result = review = False
            if record.link_1_ids:
                it_env_id = self.env.ref(
                    "ssi_general_audit." "general_audit_business_environment_5_ffea3e57"
                ).id
                it_env = record.link_1_ids.filtered(
                    lambda x: x.business_environment_id.id == it_env_id
                )
                if len(it_env) == 1:
                    result = it_env.detail_ids.ids
                    review = it_env.review
            record.it_detail_ids = result
            record.it_review = review

    it_detail_ids = fields.Many2many(
        comodel_name="general_audit_ws_bdcdfc5.detail",
        compute_sudo=True,
        compute="_compute_it_detail_review_ids",
        store=True,
    )
    it_review = fields.Text(
        compute_sudo=True,
        compute="_compute_it_detail_review_ids",
        store=True,
    )

    @api.depends(
        "link_1_ids",
    )
    def _compute_industry_review(self):
        for record in self:
            review = False
            if record.link_1_ids:
                env_id = self.env.ref(
                    "ssi_general_audit." "general_audit_business_environment_1_297034dd"
                ).id
                it_env = record.link_1_ids.filtered(
                    lambda x: x.business_environment_id.id == env_id
                )
                if len(it_env) == 1:
                    review = it_env.review
            record.industry_review = review

    industry_review = fields.Text(
        compute_sudo=True,
        compute="_compute_industry_review",
        store=True,
    )
    label_shedule_meeting_auditor = fields.Char()
    label_mgmt = fields.Char(
        string="Management",
    )
    mgmt_communication_planning_date = fields.Date(
        related="link_10_id.mgmt_communication_planning_date",
        compute_sudo=True,
        store=True,
    )
    mgmt_communication_date = fields.Date(
        related="link_10_id.mgmt_communication_date",
        compute_sudo=True,
        store=True,
    )
    mgmt_communication_reporting_date = fields.Date(
        related="link_10_id.mgmt_communication_reporting_date",
        compute_sudo=True,
        store=True,
    )
    label_tcwg = fields.Char(
        string="TCWG",
    )
    tcwg_communication_planning_date = fields.Date(
        related="link_10_id.tcwg_communication_planning_date",
        compute_sudo=True,
        store=True,
    )
    tcwg_communication_date = fields.Date(
        related="link_10_id.tcwg_communication_date",
        compute_sudo=True,
        store=True,
    )
    tcwg_communication_reporting_date = fields.Date(
        related="link_10_id.tcwg_communication_reporting_date",
        compute_sudo=True,
        store=True,
    )
    label_internal_auditor = fields.Char(
        string="Internal Auditor",
    )
    ia_communication_planning_date = fields.Date(
        related="link_10_id.ia_communication_planning_date",
        compute_sudo=True,
        store=True,
    )
    ia_communication_date = fields.Date(
        related="link_10_id.ia_communication_date",
        compute_sudo=True,
        store=True,
    )
    ia_communication_reporting_date = fields.Date(
        related="link_10_id.ia_communication_reporting_date",
        compute_sudo=True,
        store=True,
    )
    label_shedule_meeting_team = fields.Char()
    communication_planning_date = fields.Date(
        related="link_6_id.communication_planning_date",
        compute_sudo=True,
        store=True,
    )
    communication_date = fields.Date(
        related="link_6_id.communication_date",
        compute_sudo=True,
        store=True,
    )
    communication_reporting_date = fields.Date(
        related="link_6_id.communication_reporting_date",
        compute_sudo=True,
        store=True,
    )

    @api.depends(
        "link_1_ids",
    )
    def _compute_amendment_review(self):
        for record in self:
            review = False
            if record.link_1_ids:
                env_id = self.env.ref(
                    "ssi_general_audit." "general_audit_business_environment_3_bd6c9b55"
                ).id
                it_env = record.link_1_ids.filtered(
                    lambda x: x.business_environment_id.id == env_id
                )
                if len(it_env) == 1:
                    review = it_env.review
            record.amendment_review = review

    amendment_review = fields.Text(
        compute_sudo=True,
        compute="_compute_amendment_review",
        store=True,
    )

    @api.depends(
        "link_1_ids",
    )
    def _compute_regulatory_review(self):
        for record in self:
            review = False
            if record.link_1_ids:
                env_id = self.env.ref(
                    "ssi_general_audit." "general_audit_business_environment_4_aaeebb37"
                ).id
                it_env = record.link_1_ids.filtered(
                    lambda x: x.business_environment_id.id == env_id
                )
                if len(it_env) == 1:
                    review = it_env.review
            record.regulatory_review = review

    regulatory_review = fields.Text(
        compute_sudo=True,
        compute="_compute_regulatory_review",
        store=True,
    )

    @api.depends(
        "link_2_ids",
    )
    def _compute_unannounced_audit_ids(self):
        for record in self:
            result = False
            if record.link_2_ids:
                nannounced_audit = record.link_2_ids.detail_ids.filtered(
                    lambda x: x.need_unannounced_audit
                )
                if nannounced_audit:
                    result = nannounced_audit.ids
            record.unannounced_audit_ids = result

    unannounced_audit_ids = fields.Many2many(
        comodel_name="general_audit_ws_a604795.detail",
        compute_sudo=True,
        compute="_compute_unannounced_audit_ids",
        store=True,
    )

    @api.depends(
        "link_2_ids",
    )
    def _compute_business_cycle_member_ids(self):
        for record in self:
            result = False
            if record.link_2_ids:
                assigned_team_member_ids = record.link_2_ids.filtered(
                    lambda y: y.assigned_team_member_ids
                )
                if assigned_team_member_ids:
                    result = assigned_team_member_ids.ids
            record.assigned_team_member_ids = result

    assigned_team_member_ids = fields.Many2many(
        comodel_name="general_audit_ws_a604795",
        compute_sudo=True,
        compute="_compute_business_cycle_member_ids",
        relation="rel_ga_ws_fbbe0f8_2_assigned_team_member",
        store=True,
    )

    @api.depends(
        "link_2_ids",
    )
    def _compute_volume_transaction_ids(self):
        for record in self:
            result = False
            if record.link_2_ids:
                volume_transaction_ids = record.link_2_ids.filtered(
                    lambda y: y.estimated_transaction_volume > 0
                )
                if volume_transaction_ids:
                    result = volume_transaction_ids.ids
            record.volume_transaction_ids = result

    volume_transaction_ids = fields.Many2many(
        comodel_name="general_audit_ws_a604795",
        compute_sudo=True,
        compute="_compute_volume_transaction_ids",
        relation="rel_ga_ws_fbbe0f8_2_volume_transaction",
        store=True,
    )

    label_materiality = fields.Char()
    materiality_balance_type = fields.Selection(
        string="Balance Type",
        selection=[
            ("extrapolation", "Extrapolation"),
            ("end_period", "End Period"),
        ],
        required=False,
        default="extrapolation",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help=(
            "Source of the base amount used in materiality computation: "
            "Extrapolation or End Period."
        ),
    )

    @api.depends(
        "materiality_balance_type",
        "link_3_ids",
    )
    def _compute_materiality(self):
        for record in self:
            overall = 0.0
            performance = 0.0
            tolerable = 0.0

            if record.materiality_balance_type and record.link_3_ids:
                ttype = record.materiality_balance_type
                materiality = record.link_3_ids.filtered(
                    lambda x: x.base_amount_source == ttype
                )
                if materiality:
                    overall = materiality.overall_materiality
                    performance = materiality.performance_materiality
                    tolerable = materiality.tolerable_misstatement
            record.overall_materiality = overall
            record.performance_materiality = performance
            record.tolerable_misstatement = tolerable

    overall_materiality = fields.Monetary(
        compute_sudo=True,
        compute="_compute_materiality",
        store=True,
    )
    performance_materiality = fields.Monetary(
        compute_sudo=True,
        compute="_compute_materiality",
        store=True,
    )
    tolerable_misstatement = fields.Monetary(
        compute_sudo=True,
        compute="_compute_materiality",
        store=True,
    )

    @api.depends(
        "materiality_balance_type",
        "link_4_ids",
    )
    def _compute_specific_materiality_ids(self):
        for record in self:
            result = False
            if record.materiality_balance_type and record.link_4_ids:
                ttype = record.materiality_balance_type
                materiality = record.link_4_ids.filtered(
                    lambda x: x.base_amount_source == ttype
                )
                if materiality:
                    specific_materiality = materiality.materiality_mapping_ids.filtered(
                        lambda y: y.use_specific_materiality
                    )
                    if specific_materiality:
                        result = specific_materiality.ids
            record.specific_materiality_ids = result

    label_specific_materiality = fields.Char()
    specific_materiality_ids = fields.Many2many(
        comodel_name="general_audit_ws_6dcda0e_materiality_mapping",
        compute_sudo=True,
        compute="_compute_specific_materiality_ids",
        relation="rel_ga_ws_fbbe0f8_2_6dcda0e_materiality_mapping",
        store=True,
    )

    inherent_finance_review = fields.Text(
        related="link_5_id.review",
        store=True,
    )

    team_pe_review = fields.Text(
        related="link_6_id.review",
        store=True,
    )

    @api.depends(
        "link_7_id",
    )
    def _compute_main_business_activity(self):
        for record in self:
            previous_auditor = other_provided = False
            previous_audit_evidence = other_evidence = False
            if record.link_7_id:
                if record.link_7_id.previous_audit_information_ids:
                    previous_auditor = (
                        record.link_7_id.previous_audit_information_ids.ids
                    )
                if record.link_7_id.other_provided_service_ids:
                    other_provided = record.link_7_id.other_provided_service_ids.ids
                if record.link_7_id.previous_audit_evidence_ids:
                    previous_audit_evidence = (
                        record.link_7_id.previous_audit_evidence_ids.ids
                    )
                if record.link_7_id.other_evidence_ids:
                    other_evidence = record.link_7_id.other_evidence_ids.ids
            record.previous_auditor_ids = previous_auditor
            record.other_provided_service_ids = other_provided
            record.previous_audit_evidence_ids = previous_audit_evidence
            record.other_evidence_ids = other_evidence

    previous_auditor_ids = fields.Many2many(
        comodel_name=("general_audit_ws_ae11f7e." "previous_audit_information"),
        compute_sudo=True,
        compute="_compute_main_business_activity",
        relation="rel_ga_ws_fbbe0f8_2_ae11f7e_previous_audit",
        store=True,
    )
    other_provided_service_ids = fields.Many2many(
        comodel_name=("general_audit_ws_ae11f7e." "other_provided_service"),
        compute_sudo=True,
        compute="_compute_main_business_activity",
        relation="rel_ga_ws_fbbe0f8_2_ae11f7e_other_provided_service",
        store=True,
    )
    previous_audit_evidence_ids = fields.Many2many(
        comodel_name=("general_audit_ws_ae11f7e." "previous_audit_evidence"),
        compute_sudo=True,
        compute="_compute_main_business_activity",
        relation="rel_ga_ws_fbbe0f8_2_ae11f7e_previous_audit_evidence",
        store=True,
    )
    other_evidence_ids = fields.Many2many(
        comodel_name=("general_audit_ws_ae11f7e." "other_evidence"),
        compute_sudo=True,
        compute="_compute_main_business_activity",
        relation="rel_ga_ws_fbbe0f8_2_ae11f7e_other_evidence",
        store=True,
    )

    control_entity_review = fields.Text(
        related="link_8_id.review",
        store=True,
    )

    @api.depends(
        "link_9_id",
    )
    def _compute_assignment_team_ids(self):
        for record in self:
            result = False
            if record.link_9_id and record.link_9_id.summary_ids:
                summary = record.link_9_id.summary_ids.filtered(
                    lambda y: y.select_team == "yes"
                )
                if summary:
                    result = summary.ids
            record.assignment_team_ids = result

    assignment_team_ids = fields.Many2many(
        comodel_name="general_audit_ws_b9d8a5c.summary",
        compute_sudo=True,
        compute="_compute_assignment_team_ids",
        relation="rel_ga_ws_fbbe0f8_2_b9d8a5c_summary",
        store=True,
    )

    @api.depends(
        "link_11_ids",
    )
    def _compute_cycle_level_ids(self):
        for record in self:
            result = False
            if record.link_11_ids:
                cycle_level = record.link_11_ids.filtered(lambda y: y.risk == "high")
                if cycle_level:
                    result = cycle_level.business_cycle_id.ids
            record.cycle_level_ids = result

    cycle_level_ids = fields.Many2many(
        comodel_name="client_business_process",
        compute_sudo=True,
        compute="_compute_cycle_level_ids",
        relation="rel_ga_ws_fbbe0f8_2_cycle_client_business",
        store=True,
    )

    @api.depends(
        "link_12_ids",
    )
    def _compute_significant_acc_ids(self):
        for record in self:
            result = False
            if record.link_12_ids:
                significant_acc = record.link_12_ids.filtered(
                    lambda y: y.risk == "high"
                )
                if significant_acc:
                    result = significant_acc.account_type_id.ids
            record.significant_acc_ids = result

    significant_acc_ids = fields.Many2many(
        comodel_name="client_account_type",
        compute_sudo=True,
        compute="_compute_significant_acc_ids",
        relation="rel_ga_ws_fbbe0f8_2_significant_client_account",
        store=True,
    )

    allocation_total_hour_id = fields.Many2one(
        related="link_13_id.allocation_total_hour_id",
        store=True,
    )
    budget_plan_status = fields.Selection(
        related="link_13_id.budget_plan_status",
        store=True,
    )

    # Understanding of The Business Environment
    # LINK - 1 bdcdfc5 (RA.150.5)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_1_ids(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_bdcdfc5"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_1_ids = obj.search(criteria)
            if link_1_ids:
                result = link_1_ids.ids
            record.link_1_ids = result

    link_1_ids = fields.Many2many(
        string="RA.150.5",
        comodel_name="general_audit_ws_bdcdfc5",
        compute_sudo=True,
        compute="_compute_link_1_ids",
        store=True,
        help=(
            "Collection of all (Understanding of the Business Environment) "
            "worksheets linked to this General Audit. Automatically computed; use it to "
            "navigate to each detailed worksheet."
        ),
    )

    # Business Cycle Summaries
    # LINK - 2 a604795 (RA.150.3)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_2_ids(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a604795"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_2_ids = obj.search(criteria)
            if link_2_ids:
                result = link_2_ids.ids
            record.link_2_ids = result

    link_2_ids = fields.Many2many(
        string="RA.150.3",
        comodel_name="general_audit_ws_a604795",
        compute_sudo=True,
        compute="_compute_link_2_ids",
        store=True,
        help=(
            "Collection of all (Business Cycle Summaries) "
            "worksheets linked to this General Audit. Automatically computed; use it to "
            "navigate to each detailed worksheet."
        ),
    )

    # Materiality Computation
    # LINK - 3 d9d2b44 (RA.130.1)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_3_ids(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d9d2b44"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_3_ids = obj.search(criteria)
            if link_3_ids:
                result = link_3_ids.ids
            record.link_3_ids = result

    link_3_ids = fields.Many2many(
        string="RA.130.1",
        comodel_name="general_audit_ws_d9d2b44",
        compute_sudo=True,
        compute="_compute_link_3_ids",
        store=True,
        help=(
            "Collection of all (Materiality Computation) "
            "worksheets linked to this General Audit. Automatically computed; use it to "
            "navigate to each detailed worksheet."
        ),
    )

    # Specific Materiality
    # LINK - 4 6dcda0e (RA.130.2)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_4_ids(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_6dcda0e"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_4_ids = obj.search(criteria)
            if link_4_ids:
                result = link_4_ids.ids
            record.link_4_ids = result

    link_4_ids = fields.Many2many(
        string="RA.130.2",
        comodel_name="general_audit_ws_6dcda0e",
        compute_sudo=True,
        compute="_compute_link_4_ids",
        store=True,
        help=(
            "Collection of all (Specific Materiality) "
            "worksheets linked to this General Audit. Automatically computed; use it to "
            "navigate to each detailed worksheet."
        ),
    )

    # Inherent Risk - Financial Statement Level
    # LINK - 5 c16abd7 (RA.210.1)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_5_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c16abd7"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_5_id = obj.search(criteria)
            if link_5_id:
                result = link_5_id.id
            record.link_5_id = result

    link_5_id = fields.Many2one(
        string="RA.210.1",
        comodel_name="general_audit_ws_c16abd7",
        compute_sudo=True,
        compute="_compute_link_5_id",
        store=True,
        help=(
            "Link to worksheet (Inherent Risk - Financial Statement Level) "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_5_state = fields.Selection(
        string="State (RA.210.1)",
        related="link_5_id.state",
        help=(
            "Workflow state of the linked Inherent Risk - "
            "Financial Statement Level worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_5_conclusion_id = fields.Many2one(
        string="Conclusion ID (RA.210.1)",
        related="link_5_id.conclusion_id",
        help=(
            "Conclusion from the Inherent Risk - "
            "Financial Statement Level worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_5_conclusion = fields.Text(
        string="Conclusion (RA.210.1)",
        related="link_5_id.conclusion",
        help=(
            "Conclusion on the Inherent Risk - "
            "Financial Statement Level worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Team Communication Pre-Engagement
    # LINK - 6 437fc8f (PE.160)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_6_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_437fc8f"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_6_id = obj.search(criteria)
            if link_6_id:
                result = link_6_id.id
            record.link_6_id = result

    link_6_id = fields.Many2one(
        string="PE.160",
        comodel_name="general_audit_ws_437fc8f",
        compute_sudo=True,
        compute="_compute_link_6_id",
        store=True,
        help=(
            "Link to worksheet Team Communication Pre-Engagement "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_6_state = fields.Selection(
        string="State (PE.160)",
        related="link_6_id.state",
        help=(
            "Workflow state of the linked Team Communication "
            "Pre-Engagement worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_6_conclusion_id = fields.Many2one(
        string="Conclusion ID (PE.160)",
        related="link_6_id.conclusion_id",
        help=(
            "Conclusion from the Team Communication "
            "Pre-Engagement worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_6_conclusion = fields.Text(
        string="Conclusion (PE.160)",
        related="link_6_id.conclusion",
        help=(
            "Conclusion on the Team Communication "
            "Pre-Engagement worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Main Business Activity Process
    # LINK - 7 ae11f7e (RA.150.3)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_7_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ae11f7e"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_7_id = obj.search(criteria)
            if link_7_id:
                result = link_7_id.id
            record.link_7_id = result

    link_7_id = fields.Many2one(
        string="PE.150.3",
        comodel_name="general_audit_ws_ae11f7e",
        compute_sudo=True,
        compute="_compute_link_7_id",
        store=True,
        help=(
            "Link to worksheet Main Business Activity Process "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_7_state = fields.Selection(
        string="State (PE.150.3)",
        related="link_7_id.state",
        help=(
            "Workflow state of the linked Main Business "
            "Activity Process worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_7_conclusion_id = fields.Many2one(
        string="Conclusion ID (PE.150.3)",
        related="link_7_id.conclusion_id",
        help=(
            "Conclusion from the Main Business "
            "Activity Process worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_7_conclusion = fields.Text(
        string="Conclusion (PE.150.3)",
        related="link_7_id.conclusion",
        help=(
            "Conclusion on the Main Business "
            "Activity Process worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Control Risk - Entity Level
    # LINK - 8 b59b886 (RA.220.1)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_8_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b59b886"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_8_id = obj.search(criteria)
            if link_8_id:
                result = link_8_id.id
            record.link_8_id = result

    link_8_id = fields.Many2one(
        string="RA.220.1",
        comodel_name="general_audit_ws_b59b886",
        compute_sudo=True,
        compute="_compute_link_8_id",
        store=True,
        help=(
            "Link to worksheet Control Risk - Entity Level "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_8_state = fields.Selection(
        string="State (RA.220.1)",
        related="link_8_id.state",
        help=(
            "Workflow state of the linked Control Risk "
            "Entity Level worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_8_conclusion_id = fields.Many2one(
        string="Conclusion ID (RA.220.1)",
        related="link_8_id.conclusion_id",
        help=(
            "Conclusion from the Control Risk "
            "Entity Level worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_8_conclusion = fields.Text(
        string="Conclusion (RA.220.1)",
        related="link_8_id.conclusion",
        help=(
            "Conclusion on the Control Risk "
            "Entity Level worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Competency, availability, and
    # independency of assignment team
    # LINK - 9 b9d8a5c (PE.110.3)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_9_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b9d8a5c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_9_id = obj.search(criteria)
            if link_9_id:
                result = link_9_id.id
            record.link_9_id = result

    link_9_id = fields.Many2one(
        string="PE.110.3",
        comodel_name="general_audit_ws_b9d8a5c",
        compute_sudo=True,
        compute="_compute_link_9_id",
        store=True,
        help=(
            "Link to worksheet Competency, availability, and "
            "independency of assignment team "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_9_state = fields.Selection(
        string="State (PE.110.3)",
        related="link_9_id.state",
        help=(
            "Workflow state of the linked Competency, availability, and "
            "independency of assignment team worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_9_conclusion_id = fields.Many2one(
        string="Conclusion ID (PE.110.3)",
        related="link_9_id.conclusion_id",
        help=(
            "Conclusion from the Competency, availability, and "
            "independency of assignment team worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_9_conclusion = fields.Text(
        string="Conclusion (PE.110.3)",
        related="link_9_id.conclusion",
        help=(
            "Conclusion on the Competency, availability, and "
            "independency of assignment team worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # External Communication
    # LINK - 10 ae48e68 (RA.330)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_10_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ae48e68"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_10_id = obj.search(criteria)
            if link_10_id:
                result = link_10_id.id
            record.link_10_id = result

    link_10_id = fields.Many2one(
        string="RA.330",
        comodel_name="general_audit_ws_ae48e68",
        compute_sudo=True,
        compute="_compute_link_10_id",
        store=True,
        help=(
            "Link to worksheet External Communication "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_10_state = fields.Selection(
        string="State (RA.330)",
        related="link_10_id.state",
        help=(
            "Workflow state of the linked External Communication "
            "worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_10_conclusion_id = fields.Many2one(
        string="Conclusion ID (RA.330)",
        related="link_10_id.conclusion_id",
        help=(
            "Conclusion from the External Communication "
            "worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_10_conclusion = fields.Text(
        string="Conclusion (RA.330)",
        related="link_10_id.conclusion",
        help=(
            "Conclusion on the External Communication "
            "worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Control Risk - Cycle Level
    # LINK - 11 eabdaad (RA.220.2)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_11_ids(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_eabdaad"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_11_ids = obj.search(criteria)
            if link_11_ids:
                result = link_11_ids.ids
            record.link_11_ids = result

    link_11_ids = fields.Many2many(
        string="RA.220.2",
        comodel_name="general_audit_ws_eabdaad",
        compute_sudo=True,
        compute="_compute_link_11_ids",
        store=True,
        help=(
            "Collection of all (Control Risk - Cycle Level) "
            "worksheets linked to this General Audit. Automatically computed; use it to "
            "navigate to each detailed worksheet."
        ),
    )

    # Significant Account
    # LINK - 12 eabdaad (RA.220.3)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_12_ids(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ba9b2f0"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_12_ids = obj.search(criteria)
            if link_12_ids:
                result = link_12_ids.ids
            record.link_12_ids = result

    link_12_ids = fields.Many2many(
        string="RA.220.3",
        comodel_name="general_audit_ws_ba9b2f0",
        compute_sudo=True,
        compute="_compute_link_12_ids",
        store=True,
        help=(
            "Collection of all (Significant Account) "
            "worksheets linked to this General Audit. Automatically computed; use it to "
            "navigate to each detailed worksheet."
        ),
    )

    # Audit Working Plan
    # LINK - 13 cbbbaf4 (PE.120)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_13_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_cbbbaf4"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_13_id = obj.search(criteria)
            if link_13_id:
                result = link_13_id.id
            record.link_13_id = result

    link_13_id = fields.Many2one(
        string="PE.120",
        comodel_name="general_audit_ws_cbbbaf4",
        compute_sudo=True,
        compute="_compute_link_13_id",
        store=True,
        help=(
            "Link to worksheet Audit Working Plan "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_13_state = fields.Selection(
        string="State (PE.120)",
        related="link_13_id.state",
        help=(
            "Workflow state of the linked Audit Working Plan "
            "worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_13_conclusion_id = fields.Many2one(
        string="Conclusion ID (PE.120)",
        related="link_13_id.conclusion_id",
        help=(
            "Conclusion from the Audit Working Plan "
            "worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_13_conclusion = fields.Text(
        string="Conclusion (PE.120)",
        related="link_13_id.conclusion",
        help=(
            "Conclusion on the Audit Working Plan "
            "worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    def action_reload_links(self):
        for record in self.sudo():
            record._reload_links()

    def _reload_links(self):
        self.ensure_one()
        self._compute_link_1_ids()
        self._compute_link_2_ids()
        self._compute_link_3_ids()
        self._compute_link_4_ids()
        self._compute_link_5_id()
        self._compute_link_6_id()
        self._compute_link_7_id()
        self._compute_link_8_id()
        self._compute_link_9_id()
        self._compute_link_10_id()
        self._compute_link_11_ids()
        self._compute_link_12_ids()
        self._compute_link_13_id()

    def _get_fields_required_before_confirm(self):
        _super = super(GeneralAuditWSfbbe0f8, self)
        res = _super._get_fields_required_before_confirm()
        res += [
            "link_1_ids",
            "link_2_ids",
            "link_3_ids",
            "link_4_ids",
            "link_5_id",
            "link_6_id",
            "link_7_id",
            "link_8_id",
            "link_9_id",
            "link_10_id",
            "link_11_ids",
            "link_12_ids",
            "link_13_id",
        ]
        return res

    def _get_custom_field_labels(self):
        return {
            "link_1_ids": _("Understanding of The Business Environment"),
            "link_2_ids": _("Business Cycle Summaries"),
            "link_3_ids": _("Materiality Computation"),
            "link_4_ids": _("Specific Materiality"),
            "link_5_id": _("Inherent Risk - Financial Statement Level"),
            "link_6_id": _("Team Communication Pre-Engagement"),
            "link_7_id": _("Main Business Activity Process"),
            "link_8_id": _("Control Risk - Entity Level"),
            "link_9_id": _(
                "Competency, availability, and " "independency of assignment team"
            ),
            "link_10_id": _("External Communication"),
            "link_11_ids": _("Control Risk - Cycle Level"),
            "link_12_ids": _("Significant Account"),
            "link_13_id": _("Audit Working Plan"),
        }

    @api.model
    @lru_cache()
    def get_dynamic_labels(self):
        ChecklistItem = self.env["general_audit_ws_a753ab9.item"]
        items = ChecklistItem.search([("related_field", "!=", False)])
        return {item.related_field: item.name for item in items}

    def get_field_label(self, field_name):
        labels = self.get_dynamic_labels()
        return labels.get(field_name, self._fields[field_name].string)

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        _super = super(GeneralAuditWSfbbe0f8, self)
        res = _super.fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )

        if view_type == "form":
            doc = etree.XML(res["arch"])
            labels = self.get_dynamic_labels()

            for field_name in self._fields:
                if field_name in self._label_exceptions:
                    continue

                label = labels.get(field_name)
                if not label:  # <-- tambahkan validasi aman
                    continue

                # ubah string field
                for node in doc.xpath(f"//field[@name='{field_name}']"):
                    node.set("string", label)

                # ubah label manual juga, kalau ada
                for label_node in doc.xpath(f"//label[@for='{field_name}']"):
                    if label:  # <-- pastikan label bukan None
                        label_node.set("string", label)

            res["arch"] = etree.tostring(doc, encoding="unicode")
        return res
