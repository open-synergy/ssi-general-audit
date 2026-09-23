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
        """Populate ``link_5_id`` from open/done Inherent Risk - Financial
        Statement Level worksheets.

        Searches ``general_audit_ws_c16abd7`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results (matches the pattern
        applied to ``_compute_link_15_id`` onward).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c16abd7"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_5_id = obj.search(criteria, limit=1)
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
        """Populate ``link_6_id`` from open/done Team Communication
        Pre-Engagement worksheets.

        Searches ``general_audit_ws_437fc8f`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results (matches the pattern
        applied to ``_compute_link_15_id`` onward).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_437fc8f"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_6_id = obj.search(criteria, limit=1)
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
        """Populate ``link_7_id`` from open/done Main Business Activity
        Process worksheets.

        Searches ``general_audit_ws_ae11f7e`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results (matches the pattern
        applied to ``_compute_link_15_id`` onward).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ae11f7e"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_7_id = obj.search(criteria, limit=1)
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
        """Populate ``link_8_id`` from open/done Control Risk - Entity Level
        worksheets.

        Searches ``general_audit_ws_b59b886`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results (matches the pattern
        applied to ``_compute_link_15_id`` onward).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b59b886"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_8_id = obj.search(criteria, limit=1)
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
        """Populate ``link_9_id`` from open/done Competency, availability,
        and independency of assignment team worksheets.

        Searches ``general_audit_ws_b9d8a5c`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results (matches the pattern
        applied to ``_compute_link_15_id`` onward).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b9d8a5c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_9_id = obj.search(criteria, limit=1)
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
        """Populate ``link_10_id`` from open/done External Communication
        worksheets.

        Searches ``general_audit_ws_ae48e68`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results (matches the pattern
        applied to ``_compute_link_15_id`` onward).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ae48e68"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_10_id = obj.search(criteria, limit=1)
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
        """Populate ``link_13_id`` from open/done Audit Working Plan
        worksheets.

        Searches ``general_audit_ws_cbbbaf4`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done
        record may exist per audit, so the first match by default order is
        used instead of raising on multiple results (matches the pattern
        applied to ``_compute_link_15_id`` onward).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_cbbbaf4"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_13_id = obj.search(criteria, limit=1)
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

    # Data Collection
    # LINK - 14 f5a3cee (RA.500)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_14_ids(self):
        """Populate ``link_14_ids`` from open/done Data Collection worksheets.

        Searches ``general_audit_ws_f5a3cee`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` —
        same criteria pattern as the other ``link_N`` fields. Many2many
        (not Many2one) because a single audit engagement can have more
        than one Data Collection worksheet.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_f5a3cee"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_14_ids = obj.search(criteria)
            if link_14_ids:
                result = link_14_ids.ids
            record.link_14_ids = result

    link_14_ids = fields.Many2many(
        string="RA.500",
        comodel_name="general_audit_ws_f5a3cee",
        compute_sudo=True,
        compute="_compute_link_14_ids",
        relation="rel_ga_ws_fbbe0f8_2_f5a3cee",
        store=True,
        help=(
            "Collection of all (Data Collection) "
            "worksheets linked to this General Audit. Automatically computed; use it to "
            "navigate to each detailed worksheet."
        ),
    )

    @api.depends(
        "link_14_ids",
    )
    def _compute_reporting_timetable_ids(self):
        """Aggregate reporting timetable lines from ``link_14_ids``.

        Same aggregation pattern as ``_compute_unannounced_audit_ids``:
        gathers child records (``reporting_timetable_ids``) from every
        linked Data Collection worksheet into a single flat collection.
        """
        for record in self:
            result = False
            if record.link_14_ids:
                reporting_timetable_ids = record.link_14_ids.mapped(
                    "reporting_timetable_ids"
                )
                if reporting_timetable_ids:
                    result = reporting_timetable_ids.ids
            record.reporting_timetable_ids = result

    reporting_timetable_ids = fields.Many2many(
        string="Reporting Timetable",
        comodel_name="general_audit_ws_f5a3cee.reporting_timetable",
        compute_sudo=True,
        compute="_compute_reporting_timetable_ids",
        relation="rel_ga_ws_fbbe0f8_2_f5a3cee_reporting_timetable",
        store=True,
        help=(
            "Reporting timetable lines aggregated from every linked "
            "Data Collection worksheet (``link_14_ids``). Read-only "
            "summary; edited from the Data Collection worksheet itself."
        ),
    )

    # Acceptance and Continuance of Client Relationships Analysis
    # LINK - 15 806c4e1
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_15_id(self):
        """Populate ``link_15_id`` from open/done Acceptance and Continuance of
        Client Relationships Analysis worksheets.

        Searches ``general_audit_ws_806c4e1`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_806c4e1"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_15_id = obj.search(criteria, limit=1)
            if link_15_id:
                result = link_15_id.id
            record.link_15_id = result

    link_15_id = fields.Many2one(
        string="Acceptance and Continuance of Client Relationships Analysis",
        comodel_name="general_audit_ws_806c4e1",
        compute_sudo=True,
        compute="_compute_link_15_id",
        store=True,
        help=(
            "Link to worksheet (Acceptance and Continuance of Client "
            "Relationships Analysis) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_15_state = fields.Selection(
        string="State",
        related="link_15_id.state",
        help=(
            "Workflow state of the linked Acceptance and Continuance of "
            "Client Relationships Analysis worksheet. Read-only and "
            "follows the linked record."
        ),
    )
    link_15_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_15_id.conclusion_id",
        help=(
            "Conclusion from the Acceptance and Continuance of Client "
            "Relationships Analysis worksheet. Read-only, mirrors the "
            "linked record."
        ),
    )
    link_15_conclusion = fields.Text(
        string="Conclusion",
        related="link_15_id.conclusion",
        help=(
            "Conclusion on the Acceptance and Continuance of Client "
            "Relationships Analysis worksheet. Read-only, mirrors the "
            "linked record."
        ),
    )

    # Previous Financial Reporting Issues
    # LINK - 16 369c5a5
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_16_id(self):
        """Populate ``link_16_id`` from open/done Previous Financial Reporting
        Issues worksheets.

        Searches ``general_audit_ws_369c5a5`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_369c5a5"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_16_id = obj.search(criteria, limit=1)
            if link_16_id:
                result = link_16_id.id
            record.link_16_id = result

    link_16_id = fields.Many2one(
        string="Previous Financial Reporting Issues",
        comodel_name="general_audit_ws_369c5a5",
        compute_sudo=True,
        compute="_compute_link_16_id",
        store=True,
        help=(
            "Link to worksheet (Previous Financial Reporting Issues) "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_16_state = fields.Selection(
        string="State",
        related="link_16_id.state",
        help=(
            "Workflow state of the linked Previous Financial Reporting "
            "Issues worksheet. Read-only and follows the linked record."
        ),
    )
    link_16_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_16_id.conclusion_id",
        help=(
            "Conclusion from the Previous Financial Reporting Issues "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_16_conclusion = fields.Text(
        string="Conclusion",
        related="link_16_id.conclusion",
        help=(
            "Conclusion on the Previous Financial Reporting Issues "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )

    # Management Integrity
    # LINK - 17 f5e7049
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_17_id(self):
        """Populate ``link_17_id`` from open/done Management Integrity
        worksheets.

        Searches ``general_audit_ws_f5e7049`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_f5e7049"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_17_id = obj.search(criteria, limit=1)
            if link_17_id:
                result = link_17_id.id
            record.link_17_id = result

    link_17_id = fields.Many2one(
        string="Management Integrity",
        comodel_name="general_audit_ws_f5e7049",
        compute_sudo=True,
        compute="_compute_link_17_id",
        store=True,
        help=(
            "Link to worksheet (Management Integrity) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_17_state = fields.Selection(
        string="State",
        related="link_17_id.state",
        help=(
            "Workflow state of the linked Management Integrity "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_17_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_17_id.conclusion_id",
        help=(
            "Conclusion from the Management Integrity worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_17_conclusion = fields.Text(
        string="Conclusion",
        related="link_17_id.conclusion",
        help=(
            "Conclusion on the Management Integrity worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    # Communication with Previous Auditor
    # LINK - 18 0427d28
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_18_id(self):
        """Populate ``link_18_id`` from open/done Communication with Previous
        Auditor worksheets.

        Searches ``general_audit_ws_0427d28`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_0427d28"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_18_id = obj.search(criteria, limit=1)
            if link_18_id:
                result = link_18_id.id
            record.link_18_id = result

    link_18_id = fields.Many2one(
        string="Communication with Previous Auditor",
        comodel_name="general_audit_ws_0427d28",
        compute_sudo=True,
        compute="_compute_link_18_id",
        store=True,
        help=(
            "Link to worksheet (Communication with Previous Auditor) "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_18_state = fields.Selection(
        string="State",
        related="link_18_id.state",
        help=(
            "Workflow state of the linked Communication with Previous "
            "Auditor worksheet. Read-only and follows the linked "
            "record."
        ),
    )
    link_18_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_18_id.conclusion_id",
        help=(
            "Conclusion from the Communication with Previous Auditor "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_18_conclusion = fields.Text(
        string="Conclusion",
        related="link_18_id.conclusion",
        help=(
            "Conclusion on the Communication with Previous Auditor "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )

    # Engagement Letter
    # LINK - 19 d8aaebc
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_19_id(self):
        """Populate ``link_19_id`` from open/done Engagement Letter worksheets.

        Searches ``general_audit_ws_d8aaebc`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d8aaebc"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_19_id = obj.search(criteria, limit=1)
            if link_19_id:
                result = link_19_id.id
            record.link_19_id = result

    link_19_id = fields.Many2one(
        string="Engagement Letter",
        comodel_name="general_audit_ws_d8aaebc",
        compute_sudo=True,
        compute="_compute_link_19_id",
        store=True,
        help=(
            "Link to worksheet (Engagement Letter) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_19_state = fields.Selection(
        string="State",
        related="link_19_id.state",
        help=(
            "Workflow state of the linked Engagement Letter worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_19_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_19_id.conclusion_id",
        help=(
            "Conclusion from the Engagement Letter worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_19_conclusion = fields.Text(
        string="Conclusion",
        related="link_19_id.conclusion",
        help=(
            "Conclusion on the Engagement Letter worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )

    # Assignment Letter
    # LINK - 20 c435bcd
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_20_id(self):
        """Populate ``link_20_id`` from open/done Assignment Letter worksheets.

        Searches ``general_audit_ws_c435bcd`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c435bcd"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_20_id = obj.search(criteria, limit=1)
            if link_20_id:
                result = link_20_id.id
            record.link_20_id = result

    link_20_id = fields.Many2one(
        string="Assignment Letter",
        comodel_name="general_audit_ws_c435bcd",
        compute_sudo=True,
        compute="_compute_link_20_id",
        store=True,
        help=(
            "Link to worksheet (Assignment Letter) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_20_state = fields.Selection(
        string="State",
        related="link_20_id.state",
        help=(
            "Workflow state of the linked Assignment Letter worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_20_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_20_id.conclusion_id",
        help=(
            "Conclusion from the Assignment Letter worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_20_conclusion = fields.Text(
        string="Conclusion",
        related="link_20_id.conclusion",
        help=(
            "Conclusion on the Assignment Letter worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )

    # Independence Statement
    # LINK - 21 09253fe
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_21_id(self):
        """Populate ``link_21_id`` from open/done Independence Statement
        worksheets.

        Searches ``general_audit_ws_09253fe`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_09253fe"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_21_id = obj.search(criteria, limit=1)
            if link_21_id:
                result = link_21_id.id
            record.link_21_id = result

    link_21_id = fields.Many2one(
        string="Independence Statement",
        comodel_name="general_audit_ws_09253fe",
        compute_sudo=True,
        compute="_compute_link_21_id",
        store=True,
        help=(
            "Link to worksheet (Independence Statement) for this "
            "General Audit. Automatically computed and stored."
        ),
    )
    link_21_state = fields.Selection(
        string="State",
        related="link_21_id.state",
        help=(
            "Workflow state of the linked Independence Statement "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_21_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_21_id.conclusion_id",
        help=(
            "Conclusion from the Independence Statement worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_21_conclusion = fields.Text(
        string="Conclusion",
        related="link_21_id.conclusion",
        help=(
            "Conclusion on the Independence Statement worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    # Client Assistance Package
    # LINK - 22 abd82ed
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_22_id(self):
        """Populate ``link_22_id`` from open/done Client Assistance Package
        worksheets.

        Searches ``general_audit_ws_abd82ed`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_abd82ed"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_22_id = obj.search(criteria, limit=1)
            if link_22_id:
                result = link_22_id.id
            record.link_22_id = result

    link_22_id = fields.Many2one(
        string="Client Assistance Package",
        comodel_name="general_audit_ws_abd82ed",
        compute_sudo=True,
        compute="_compute_link_22_id",
        store=True,
        help=(
            "Link to worksheet (Client Assistance Package) for this "
            "General Audit. Automatically computed and stored."
        ),
    )
    link_22_state = fields.Selection(
        string="State",
        related="link_22_id.state",
        help=(
            "Workflow state of the linked Client Assistance Package "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_22_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_22_id.conclusion_id",
        help=(
            "Conclusion from the Client Assistance Package worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_22_conclusion = fields.Text(
        string="Conclusion",
        related="link_22_id.conclusion",
        help=(
            "Conclusion on the Client Assistance Package worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Trial Balance
    # LINK - 23 a033cc6
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_23_id(self):
        """Populate ``link_23_id`` from open/done Trial Balance worksheets.

        Searches ``general_audit_ws_a033cc6`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a033cc6"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_23_id = obj.search(criteria, limit=1)
            if link_23_id:
                result = link_23_id.id
            record.link_23_id = result

    link_23_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="general_audit_ws_a033cc6",
        compute_sudo=True,
        compute="_compute_link_23_id",
        store=True,
        help=(
            "Link to worksheet (Trial Balance) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_23_state = fields.Selection(
        string="State",
        related="link_23_id.state",
        help=(
            "Workflow state of the linked Trial Balance worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_23_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_23_id.conclusion_id",
        help=(
            "Conclusion from the Trial Balance worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )
    link_23_conclusion = fields.Text(
        string="Conclusion",
        related="link_23_id.conclusion",
        help=(
            "Conclusion on the Trial Balance worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )

    # Preliminary Analytic Procedure
    # LINK - 24 c8740d4
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_24_id(self):
        """Populate ``link_24_id`` from open/done Preliminary Analytic
        Procedure worksheets.

        Searches ``general_audit_ws_c8740d4`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c8740d4"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_24_id = obj.search(criteria, limit=1)
            if link_24_id:
                result = link_24_id.id
            record.link_24_id = result

    link_24_id = fields.Many2one(
        string="Preliminary Analytic Procedure",
        comodel_name="general_audit_ws_c8740d4",
        compute_sudo=True,
        compute="_compute_link_24_id",
        store=True,
        help=(
            "Link to worksheet (Preliminary Analytic Procedure) for "
            "this General Audit. Automatically computed and stored."
        ),
    )
    link_24_state = fields.Selection(
        string="State",
        related="link_24_id.state",
        help=(
            "Workflow state of the linked Preliminary Analytic "
            "Procedure worksheet. Read-only and follows the linked "
            "record."
        ),
    )
    link_24_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_24_id.conclusion_id",
        help=(
            "Conclusion from the Preliminary Analytic Procedure "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_24_conclusion = fields.Text(
        string="Conclusion",
        related="link_24_id.conclusion",
        help=(
            "Conclusion on the Preliminary Analytic Procedure "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )

    # Preliminary Analytic Procedure - Vertical & Horizontal Analysis
    # LINK - 25 b32655a
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_25_id(self):
        """Populate ``link_25_id`` from open/done Preliminary Analytic
        Procedure - Vertical & Horizontal Analysis worksheets.

        Searches ``general_audit_ws_b32655a`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b32655a"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_25_id = obj.search(criteria, limit=1)
            if link_25_id:
                result = link_25_id.id
            record.link_25_id = result

    link_25_id = fields.Many2one(
        string="Preliminary Analytic Procedure - Vertical & Horizontal Analysis",
        comodel_name="general_audit_ws_b32655a",
        compute_sudo=True,
        compute="_compute_link_25_id",
        store=True,
        help=(
            "Link to worksheet (Preliminary Analytic Procedure - "
            "Vertical & Horizontal Analysis) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_25_state = fields.Selection(
        string="State",
        related="link_25_id.state",
        help=(
            "Workflow state of the linked Preliminary Analytic "
            "Procedure - Vertical & Horizontal Analysis worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_25_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_25_id.conclusion_id",
        help=(
            "Conclusion from the Preliminary Analytic Procedure - "
            "Vertical & Horizontal Analysis worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )
    link_25_conclusion = fields.Text(
        string="Conclusion",
        related="link_25_id.conclusion",
        help=(
            "Conclusion on the Preliminary Analytic Procedure - "
            "Vertical & Horizontal Analysis worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )

    # Preliminary Analytic Procedure - Ratio Analysis
    # LINK - 26 d4289e4
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_26_id(self):
        """Populate ``link_26_id`` from open/done Preliminary Analytic
        Procedure - Ratio Analysis worksheets.

        Searches ``general_audit_ws_d4289e4`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d4289e4"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_26_id = obj.search(criteria, limit=1)
            if link_26_id:
                result = link_26_id.id
            record.link_26_id = result

    link_26_id = fields.Many2one(
        string="Preliminary Analytic Procedure - Ratio Analysis",
        comodel_name="general_audit_ws_d4289e4",
        compute_sudo=True,
        compute="_compute_link_26_id",
        store=True,
        help=(
            "Link to worksheet (Preliminary Analytic Procedure - Ratio "
            "Analysis) for this General Audit. Automatically computed "
            "and stored."
        ),
    )
    link_26_state = fields.Selection(
        string="State",
        related="link_26_id.state",
        help=(
            "Workflow state of the linked Preliminary Analytic "
            "Procedure - Ratio Analysis worksheet. Read-only and "
            "follows the linked record."
        ),
    )
    link_26_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_26_id.conclusion_id",
        help=(
            "Conclusion from the Preliminary Analytic Procedure - Ratio "
            "Analysis worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_26_conclusion = fields.Text(
        string="Conclusion",
        related="link_26_id.conclusion",
        help=(
            "Conclusion on the Preliminary Analytic Procedure - Ratio "
            "Analysis worksheet. Read-only, mirrors the linked record."
        ),
    )

    # General Information and Legal Aspect
    # LINK - 27 ddf034c
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_27_id(self):
        """Populate ``link_27_id`` from open/done General Information and Legal
        Aspect worksheets.

        Searches ``general_audit_ws_ddf034c`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ddf034c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_27_id = obj.search(criteria, limit=1)
            if link_27_id:
                result = link_27_id.id
            record.link_27_id = result

    link_27_id = fields.Many2one(
        string="General Information and Legal Aspect",
        comodel_name="general_audit_ws_ddf034c",
        compute_sudo=True,
        compute="_compute_link_27_id",
        store=True,
        help=(
            "Link to worksheet (General Information and Legal Aspect) "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_27_state = fields.Selection(
        string="State",
        related="link_27_id.state",
        help=(
            "Workflow state of the linked General Information and Legal "
            "Aspect worksheet. Read-only and follows the linked record."
        ),
    )
    link_27_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_27_id.conclusion_id",
        help=(
            "Conclusion from the General Information and Legal Aspect "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_27_conclusion = fields.Text(
        string="Conclusion",
        related="link_27_id.conclusion",
        help=(
            "Conclusion on the General Information and Legal Aspect "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )

    # Structure Organization and Responsibility
    # LINK - 28 e78a3c6
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_28_id(self):
        """Populate ``link_28_id`` from open/done Structure Organization and
        Responsibility worksheets.

        Searches ``general_audit_ws_e78a3c6`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_e78a3c6"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_28_id = obj.search(criteria, limit=1)
            if link_28_id:
                result = link_28_id.id
            record.link_28_id = result

    link_28_id = fields.Many2one(
        string="Structure Organization and Responsibility",
        comodel_name="general_audit_ws_e78a3c6",
        compute_sudo=True,
        compute="_compute_link_28_id",
        store=True,
        help=(
            "Link to worksheet (Structure Organization and "
            "Responsibility) for this General Audit. Automatically "
            "computed and stored."
        ),
    )
    link_28_state = fields.Selection(
        string="State",
        related="link_28_id.state",
        help=(
            "Workflow state of the linked Structure Organization and "
            "Responsibility worksheet. Read-only and follows the linked "
            "record."
        ),
    )
    link_28_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_28_id.conclusion_id",
        help=(
            "Conclusion from the Structure Organization and "
            "Responsibility worksheet. Read-only, mirrors the linked "
            "record."
        ),
    )
    link_28_conclusion = fields.Text(
        string="Conclusion",
        related="link_28_id.conclusion",
        help=(
            "Conclusion on the Structure Organization and "
            "Responsibility worksheet. Read-only, mirrors the linked "
            "record."
        ),
    )

    # Understanding of Relevant Regulation
    # LINK - 29 a13a30e
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_29_id(self):
        """Populate ``link_29_id`` from open/done Understanding of Relevant
        Regulation worksheets.

        Searches ``general_audit_ws_a13a30e`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a13a30e"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_29_id = obj.search(criteria, limit=1)
            if link_29_id:
                result = link_29_id.id
            record.link_29_id = result

    link_29_id = fields.Many2one(
        string="Understanding of Relevant Regulation",
        comodel_name="general_audit_ws_a13a30e",
        compute_sudo=True,
        compute="_compute_link_29_id",
        store=True,
        help=(
            "Link to worksheet (Understanding of Relevant Regulation) "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_29_state = fields.Selection(
        string="State",
        related="link_29_id.state",
        help=(
            "Workflow state of the linked Understanding of Relevant "
            "Regulation worksheet. Read-only and follows the linked "
            "record."
        ),
    )
    link_29_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_29_id.conclusion_id",
        help=(
            "Conclusion from the Understanding of Relevant Regulation "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_29_conclusion = fields.Text(
        string="Conclusion",
        related="link_29_id.conclusion",
        help=(
            "Conclusion on the Understanding of Relevant Regulation "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )

    # Going Concern Analysis
    # LINK - 30 c0d0898
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_30_id(self):
        """Populate ``link_30_id`` from open/done Going Concern Analysis
        worksheets.

        Searches ``general_audit_ws_c0d0898`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c0d0898"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_30_id = obj.search(criteria, limit=1)
            if link_30_id:
                result = link_30_id.id
            record.link_30_id = result

    link_30_id = fields.Many2one(
        string="Going Concern Analysis",
        comodel_name="general_audit_ws_c0d0898",
        compute_sudo=True,
        compute="_compute_link_30_id",
        store=True,
        help=(
            "Link to worksheet (Going Concern Analysis) for this "
            "General Audit. Automatically computed and stored."
        ),
    )
    link_30_state = fields.Selection(
        string="State",
        related="link_30_id.state",
        help=(
            "Workflow state of the linked Going Concern Analysis "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_30_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_30_id.conclusion_id",
        help=(
            "Conclusion from the Going Concern Analysis worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_30_conclusion = fields.Text(
        string="Conclusion",
        related="link_30_id.conclusion",
        help=(
            "Conclusion on the Going Concern Analysis worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    # Understanding of Preparation of Financial Statement
    # LINK - 31 f6a227
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_31_id(self):
        """Populate ``link_31_id`` from open/done Understanding of Preparation
        of Financial Statement worksheets.

        Searches ``general_audit_ws_f6a227`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_f6a227"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_31_id = obj.search(criteria, limit=1)
            if link_31_id:
                result = link_31_id.id
            record.link_31_id = result

    link_31_id = fields.Many2one(
        string="Understanding of Preparation of Financial Statement",
        comodel_name="general_audit_ws_f6a227",
        compute_sudo=True,
        compute="_compute_link_31_id",
        store=True,
        help=(
            "Link to worksheet (Understanding of Preparation of "
            "Financial Statement) for this General Audit. Automatically "
            "computed and stored."
        ),
    )
    link_31_state = fields.Selection(
        string="State",
        related="link_31_id.state",
        help=(
            "Workflow state of the linked Understanding of Preparation "
            "of Financial Statement worksheet. Read-only and follows "
            "the linked record."
        ),
    )
    link_31_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_31_id.conclusion_id",
        help=(
            "Conclusion from the Understanding of Preparation of "
            "Financial Statement worksheet. Read-only, mirrors the "
            "linked record."
        ),
    )
    link_31_conclusion = fields.Text(
        string="Conclusion",
        related="link_31_id.conclusion",
        help=(
            "Conclusion on the Understanding of Preparation of "
            "Financial Statement worksheet. Read-only, mirrors the "
            "linked record."
        ),
    )

    # Fraud Factor Analysis
    # LINK - 32 c0e0eec
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_32_id(self):
        """Populate ``link_32_id`` from open/done Fraud Factor Analysis
        worksheets.

        Searches ``general_audit_ws_c0e0eec`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c0e0eec"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_32_id = obj.search(criteria, limit=1)
            if link_32_id:
                result = link_32_id.id
            record.link_32_id = result

    link_32_id = fields.Many2one(
        string="Fraud Factor Analysis",
        comodel_name="general_audit_ws_c0e0eec",
        compute_sudo=True,
        compute="_compute_link_32_id",
        store=True,
        help=(
            "Link to worksheet (Fraud Factor Analysis) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_32_state = fields.Selection(
        string="State",
        related="link_32_id.state",
        help=(
            "Workflow state of the linked Fraud Factor Analysis "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_32_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_32_id.conclusion_id",
        help=(
            "Conclusion from the Fraud Factor Analysis worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_32_conclusion = fields.Text(
        string="Conclusion",
        related="link_32_id.conclusion",
        help=(
            "Conclusion on the Fraud Factor Analysis worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    # Inherent Risk - Account Level
    # LINK - 33 a418d89
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_33_id(self):
        """Populate ``link_33_id`` from open/done Inherent Risk - Account Level
        worksheets.

        Searches ``general_audit_ws_a418d89`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a418d89"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_33_id = obj.search(criteria, limit=1)
            if link_33_id:
                result = link_33_id.id
            record.link_33_id = result

    link_33_id = fields.Many2one(
        string="Inherent Risk - Account Level",
        comodel_name="general_audit_ws_a418d89",
        compute_sudo=True,
        compute="_compute_link_33_id",
        store=True,
        help=(
            "Link to worksheet (Inherent Risk - Account Level) for this "
            "General Audit. Automatically computed and stored."
        ),
    )
    link_33_state = fields.Selection(
        string="State",
        related="link_33_id.state",
        help=(
            "Workflow state of the linked Inherent Risk - Account Level "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_33_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_33_id.conclusion_id",
        help=(
            "Conclusion from the Inherent Risk - Account Level "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_33_conclusion = fields.Text(
        string="Conclusion",
        related="link_33_id.conclusion",
        help=(
            "Conclusion on the Inherent Risk - Account Level worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # ROMM
    # LINK - 34 de417a6
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_34_id(self):
        """Populate ``link_34_id`` from open/done ROMM worksheets.

        Searches ``general_audit_ws_de417a6`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_de417a6"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_34_id = obj.search(criteria, limit=1)
            if link_34_id:
                result = link_34_id.id
            record.link_34_id = result

    link_34_id = fields.Many2one(
        string="ROMM",
        comodel_name="general_audit_ws_de417a6",
        compute_sudo=True,
        compute="_compute_link_34_id",
        store=True,
        help=(
            "Link to worksheet (ROMM) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_34_state = fields.Selection(
        string="State",
        related="link_34_id.state",
        help=(
            "Workflow state of the linked ROMM worksheet. Read-only and "
            "follows the linked record."
        ),
    )
    link_34_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_34_id.conclusion_id",
        help=(
            "Conclusion from the ROMM worksheet. Read-only, mirrors the "
            "linked record."
        ),
    )
    link_34_conclusion = fields.Text(
        string="Conclusion",
        related="link_34_id.conclusion",
        help=(
            "Conclusion on the ROMM worksheet. Read-only, mirrors the " "linked record."
        ),
    )

    # ROMM - Financial Statement Level
    # LINK - 35 c165170
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_35_id(self):
        """Populate ``link_35_id`` from open/done ROMM - Financial Statement
        Level worksheets.

        Searches ``general_audit_ws_c165170`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c165170"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_35_id = obj.search(criteria, limit=1)
            if link_35_id:
                result = link_35_id.id
            record.link_35_id = result

    link_35_id = fields.Many2one(
        string="ROMM - Financial Statement Level",
        comodel_name="general_audit_ws_c165170",
        compute_sudo=True,
        compute="_compute_link_35_id",
        store=True,
        help=(
            "Link to worksheet (ROMM - Financial Statement Level) for "
            "this General Audit. Automatically computed and stored."
        ),
    )
    link_35_state = fields.Selection(
        string="State",
        related="link_35_id.state",
        help=(
            "Workflow state of the linked ROMM - Financial Statement "
            "Level worksheet. Read-only and follows the linked record."
        ),
    )
    link_35_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_35_id.conclusion_id",
        help=(
            "Conclusion from the ROMM - Financial Statement Level "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_35_conclusion = fields.Text(
        string="Conclusion",
        related="link_35_id.conclusion",
        help=(
            "Conclusion on the ROMM - Financial Statement Level "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )

    # ROMM - Account Level
    # LINK - 36 d66d87a
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_36_id(self):
        """Populate ``link_36_id`` from open/done ROMM - Account Level
        worksheets.

        Searches ``general_audit_ws_d66d87a`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d66d87a"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_36_id = obj.search(criteria, limit=1)
            if link_36_id:
                result = link_36_id.id
            record.link_36_id = result

    link_36_id = fields.Many2one(
        string="ROMM - Account Level",
        comodel_name="general_audit_ws_d66d87a",
        compute_sudo=True,
        compute="_compute_link_36_id",
        store=True,
        help=(
            "Link to worksheet (ROMM - Account Level) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_36_state = fields.Selection(
        string="State",
        related="link_36_id.state",
        help=(
            "Workflow state of the linked ROMM - Account Level "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_36_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_36_id.conclusion_id",
        help=(
            "Conclusion from the ROMM - Account Level worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_36_conclusion = fields.Text(
        string="Conclusion",
        related="link_36_id.conclusion",
        help=(
            "Conclusion on the ROMM - Account Level worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    # Team Communication - Risk Assessment
    # LINK - 37 b1f820c
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_37_id(self):
        """Populate ``link_37_id`` from open/done Team Communication - Risk
        Assessment worksheets.

        Searches ``general_audit_ws_b1f820c`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b1f820c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_37_id = obj.search(criteria, limit=1)
            if link_37_id:
                result = link_37_id.id
            record.link_37_id = result

    link_37_id = fields.Many2one(
        string="Team Communication - Risk Assessment",
        comodel_name="general_audit_ws_b1f820c",
        compute_sudo=True,
        compute="_compute_link_37_id",
        store=True,
        help=(
            "Link to worksheet (Team Communication - Risk Assessment) "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_37_state = fields.Selection(
        string="State",
        related="link_37_id.state",
        help=(
            "Workflow state of the linked Team Communication - Risk "
            "Assessment worksheet. Read-only and follows the linked "
            "record."
        ),
    )
    link_37_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_37_id.conclusion_id",
        help=(
            "Conclusion from the Team Communication - Risk Assessment "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_37_conclusion = fields.Text(
        string="Conclusion",
        related="link_37_id.conclusion",
        help=(
            "Conclusion on the Team Communication - Risk Assessment "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )

    # Communication with Management
    # LINK - 38 b3ff42f
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_38_id(self):
        """Populate ``link_38_id`` from open/done Communication with Management
        worksheets.

        Searches ``general_audit_ws_b3ff42f`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b3ff42f"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_38_id = obj.search(criteria, limit=1)
            if link_38_id:
                result = link_38_id.id
            record.link_38_id = result

    link_38_id = fields.Many2one(
        string="Communication with Management",
        comodel_name="general_audit_ws_b3ff42f",
        compute_sudo=True,
        compute="_compute_link_38_id",
        store=True,
        help=(
            "Link to worksheet (Communication with Management) for this "
            "General Audit. Automatically computed and stored."
        ),
    )
    link_38_state = fields.Selection(
        string="State",
        related="link_38_id.state",
        help=(
            "Workflow state of the linked Communication with Management "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_38_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_38_id.conclusion_id",
        help=(
            "Conclusion from the Communication with Management "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_38_conclusion = fields.Text(
        string="Conclusion",
        related="link_38_id.conclusion",
        help=(
            "Conclusion on the Communication with Management worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Communication with TCWG
    # LINK - 39 c94e287
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_39_id(self):
        """Populate ``link_39_id`` from open/done Communication with TCWG
        worksheets.

        Searches ``general_audit_ws_c94e287`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c94e287"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_39_id = obj.search(criteria, limit=1)
            if link_39_id:
                result = link_39_id.id
            record.link_39_id = result

    link_39_id = fields.Many2one(
        string="Communication with TCWG",
        comodel_name="general_audit_ws_c94e287",
        compute_sudo=True,
        compute="_compute_link_39_id",
        store=True,
        help=(
            "Link to worksheet (Communication with TCWG) for this "
            "General Audit. Automatically computed and stored."
        ),
    )
    link_39_state = fields.Selection(
        string="State",
        related="link_39_id.state",
        help=(
            "Workflow state of the linked Communication with TCWG "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_39_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_39_id.conclusion_id",
        help=(
            "Conclusion from the Communication with TCWG worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_39_conclusion = fields.Text(
        string="Conclusion",
        related="link_39_id.conclusion",
        help=(
            "Conclusion on the Communication with TCWG worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    # Use of Internal Auditor's Work Result
    # LINK - 40 d133f46
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_40_id(self):
        """Populate ``link_40_id`` from open/done Use of Internal Auditor's
        Work Result worksheets.

        Searches ``general_audit_ws_d133f46`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]`` -- same
        criteria pattern as ``_compute_link_5_id``, plus ``limit=1``:
        this worksheet type may allow more than one open/done record
        per audit (``allowed_audit=True``), so the first match by
        default order is used instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d133f46"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_40_id = obj.search(criteria, limit=1)
            if link_40_id:
                result = link_40_id.id
            record.link_40_id = result

    link_40_id = fields.Many2one(
        string="Use of Internal Auditor's Work Result",
        comodel_name="general_audit_ws_d133f46",
        compute_sudo=True,
        compute="_compute_link_40_id",
        store=True,
        help=(
            "Link to worksheet (Use of Internal Auditor's Work Result) "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_40_state = fields.Selection(
        string="State",
        related="link_40_id.state",
        help=(
            "Workflow state of the linked Use of Internal Auditor's "
            "Work Result worksheet. Read-only and follows the linked "
            "record."
        ),
    )
    link_40_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_40_id.conclusion_id",
        help=(
            "Conclusion from the Use of Internal Auditor's Work Result "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_40_conclusion = fields.Text(
        string="Conclusion",
        related="link_40_id.conclusion",
        help=(
            "Conclusion on the Use of Internal Auditor's Work Result "
            "worksheet. Read-only, mirrors the linked record."
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
        self._compute_link_14_ids()
        self._compute_link_15_id()
        self._compute_link_16_id()
        self._compute_link_17_id()
        self._compute_link_18_id()
        self._compute_link_19_id()
        self._compute_link_20_id()
        self._compute_link_21_id()
        self._compute_link_22_id()
        self._compute_link_23_id()
        self._compute_link_24_id()
        self._compute_link_25_id()
        self._compute_link_26_id()
        self._compute_link_27_id()
        self._compute_link_28_id()
        self._compute_link_29_id()
        self._compute_link_30_id()
        self._compute_link_31_id()
        self._compute_link_32_id()
        self._compute_link_33_id()
        self._compute_link_34_id()
        self._compute_link_35_id()
        self._compute_link_36_id()
        self._compute_link_37_id()
        self._compute_link_38_id()
        self._compute_link_39_id()
        self._compute_link_40_id()

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
            "link_14_ids": _("Data Collection"),
            "link_15_id": _(
                "Acceptance and Continuance of Client " "Relationships Analysis"
            ),
            "link_16_id": _("Previous Financial Reporting Issues"),
            "link_17_id": _("Management Integrity"),
            "link_18_id": _("Communication with Previous Auditor"),
            "link_19_id": _("Engagement Letter"),
            "link_20_id": _("Assignment Letter"),
            "link_21_id": _("Independence Statement"),
            "link_22_id": _("Client Assistance Package"),
            "link_23_id": _("Trial Balance"),
            "link_24_id": _("Preliminary Analytic Procedure"),
            "link_25_id": _(
                "Preliminary Analytic Procedure - Vertical & " "Horizontal Analysis"
            ),
            "link_26_id": _("Preliminary Analytic Procedure - Ratio Analysis"),
            "link_27_id": _("General Information and Legal Aspect"),
            "link_28_id": _("Structure Organization and Responsibility"),
            "link_29_id": _("Understanding of Relevant Regulation"),
            "link_30_id": _("Going Concern Analysis"),
            "link_31_id": _("Understanding of Preparation of Financial " "Statement"),
            "link_32_id": _("Fraud Factor Analysis"),
            "link_33_id": _("Inherent Risk - Account Level"),
            "link_34_id": _("ROMM"),
            "link_35_id": _("ROMM - Financial Statement Level"),
            "link_36_id": _("ROMM - Account Level"),
            "link_37_id": _("Team Communication - Risk Assessment"),
            "link_38_id": _("Communication with Management"),
            "link_39_id": _("Communication with TCWG"),
            "link_40_id": _("Use of Internal Auditor's Work Result"),
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
