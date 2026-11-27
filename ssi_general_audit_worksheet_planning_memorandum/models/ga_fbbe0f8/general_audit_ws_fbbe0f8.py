# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from functools import lru_cache

from lxml import etree

from odoo import _, api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSfbbe0f8(models.Model):
    """
    WS: Audit Planning Memorandum — Detail Summary (fbbe0f8) — ISA 300 / SA 300.

    A consolidated partner-reviewable narrative that aggregates key information
    from multiple upstream worksheets into a single Audit Planning Memorandum
    document.  This worksheet is the "cover page" of the planning phase and
    is intended to be reviewed and approved by the Engagement Partner before
    fieldwork commences.

    The following information is pulled from linked upstream worksheets:

    * **Business environment** (``link_1_ids``) — IT environment details
      and the conclusions of the IT, industry, regulatory, and amendment
      environments.
    * **Business cycles** (``link_2_ids``) — Significant transaction cycles,
      assigned team members, estimated transaction volumes, and entities
      flagged for unannounced audit.
    * **Preliminary materiality** (``link_3_ids``) — Overall materiality (OM),
      performance materiality (PM), and tolerable misstatement (TM).
    * **Specific materiality** (``link_4_ids``) — Material account type
      mappings.
    * **Inherent risk finance** (``link_5_id``) — Review note.
    * **Team preliminary engagement** (``link_6_id``) — Communication
      dates.
    * **Team communication risk assessment** (``link_37_id``) —
      Conclusion.
    * **Control risk entity level** (``link_8_id``) — Conclusion.
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
        "general_audit_conclusion_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_planning_memorandum." "worksheet_type_fbbe0f8"
    )
    _conclusion_line_model = "general_audit_ws_fbbe0f8.conclusion"
    _conclusion_line_owner_field = "worksheet_id"
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
        help=(
            "Taken from the audit engagement (General Audit) this "
            "memorandum belongs to."
        ),
    )
    other_report_ids = fields.Many2many(
        related="general_audit_id.other_report_ids",
        compute_sudo=True,
        relation="rel_ga_ws_fbbe0f8_2_ga_other_report",
        column1="ws_fbbe0f8_id",
        column2="other_report_id",
        store=True,
        help=(
            "Taken from the audit engagement (General Audit) this "
            "memorandum belongs to."
        ),
    )
    expert_type_ids = fields.Many2many(
        related="general_audit_id.expert_type_ids",
        compute_sudo=True,
        relation="rel_ga_ws_fbbe0f8_2_ga_expert_type",
        column1="ws_fbbe0f8_id",
        column2="expert_type_id",
        store=True,
        help=(
            "Taken from the audit engagement (General Audit) this "
            "memorandum belongs to."
        ),
    )

    def _get_following_states(self):
        """Return the states in which source worksheet data is followed.

        While the worksheet is in one of these states, the data copied
        from the linked worksheets follows their changes. In any other
        state the copied data is kept as a snapshot.

        :return: list of state codes
        """
        return ["draft", "open"]

    @ssi_decorator.post_open_action()
    def _10_refresh_source_links(self):
        """Refresh every link to the source worksheets on start.

        Worksheets created or opened after this one was drafted are
        picked up, and the data copied from them is recomputed.

        :return: nothing; marks the link fields to be recomputed
        """
        self.ensure_one()
        self.modified(["general_audit_id"])

    @api.depends(
        "link_1_ids",
        "link_1_ids.business_environment_id",
        "link_1_ids.detail_ids",
        "link_1_ids.conclusion",
    )
    def _compute_it_detail_review_ids(self):
        """Copy the IT environment details and conclusion from RA.150.5.

        Follows the source while the worksheet is draft or open and
        keeps the stored values afterwards.
        """
        for record in self:
            result = record.it_detail_ids.ids
            review = record.it_review
            if record.state in record._get_following_states():
                result = review = False
                if record.link_1_ids:
                    it_env_id = self.env.ref(
                        "ssi_general_audit."
                        "general_audit_business_environment_5_ffea3e57"
                    ).id
                    it_env = record.link_1_ids.filtered(
                        lambda x: x.business_environment_id.id == it_env_id
                    )
                    if len(it_env) == 1:
                        result = it_env.detail_ids.ids
                        review = it_env.conclusion
            record.it_detail_ids = result
            record.it_review = review

    it_detail_ids = fields.Many2many(
        comodel_name="general_audit_ws_bdcdfc5.detail",
        compute_sudo=True,
        compute="_compute_it_detail_review_ids",
        store=True,
        help=(
            "Taken from the 'Understanding of the Business Environment' "
            "worksheet, field 'Details', from the 'Technological "
            "Developments' environment."
        ),
    )
    it_review = fields.Text(
        compute_sudo=True,
        compute="_compute_it_detail_review_ids",
        store=True,
        help=(
            "Taken from the 'Understanding of the Business Environment' "
            "worksheet, field 'Conclusion Additional Explanation', from "
            "the 'Technological Developments' environment."
        ),
    )

    @api.depends(
        "link_1_ids",
        "link_1_ids.business_environment_id",
        "link_1_ids.conclusion",
    )
    def _compute_industry_review(self):
        """Copy the industry conclusion from RA.150.5.

        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            review = record.industry_review
            if record.state in record._get_following_states():
                review = False
                if record.link_1_ids:
                    env_id = self.env.ref(
                        "ssi_general_audit."
                        "general_audit_business_environment_1_297034dd"
                    ).id
                    it_env = record.link_1_ids.filtered(
                        lambda x: x.business_environment_id.id == env_id
                    )
                    if len(it_env) == 1:
                        review = it_env.conclusion
            record.industry_review = review

    industry_review = fields.Text(
        compute_sudo=True,
        compute="_compute_industry_review",
        store=True,
        help=(
            "Taken from the 'Understanding of the Business Environment' "
            "worksheet, field 'Conclusion Additional Explanation', from "
            "the 'Industry Trends' environment."
        ),
    )
    label_shedule_meeting_auditor = fields.Char()
    label_mgmt = fields.Char(
        string="Management",
    )
    mgmt_communication_planning_date = fields.Date(
        related="link_10_id.mgmt_communication_planning_date",
        compute_sudo=True,
        store=True,
        help=(
            "Taken from the 'External Communication' worksheet, field 'Date "
            "of Management Communication Planning'."
        ),
    )
    mgmt_communication_date = fields.Date(
        related="link_10_id.mgmt_communication_date",
        compute_sudo=True,
        store=True,
        help=(
            "Taken from the 'External Communication' worksheet, field 'Date "
            "of Management Communication'."
        ),
    )
    mgmt_communication_reporting_date = fields.Date(
        related="link_10_id.mgmt_communication_reporting_date",
        compute_sudo=True,
        store=True,
        help=(
            "Taken from the 'External Communication' worksheet, field 'Date "
            "of Management Communication Reporting'."
        ),
    )
    label_tcwg = fields.Char(
        string="TCWG",
    )
    tcwg_communication_planning_date = fields.Date(
        related="link_10_id.tcwg_communication_planning_date",
        compute_sudo=True,
        store=True,
        help=(
            "Taken from the 'External Communication' worksheet, field 'Date "
            "of TCWG Communication Planning'."
        ),
    )
    tcwg_communication_date = fields.Date(
        related="link_10_id.tcwg_communication_date",
        compute_sudo=True,
        store=True,
        help=(
            "Taken from the 'External Communication' worksheet, field 'Date "
            "of TCWG Communication'."
        ),
    )
    tcwg_communication_reporting_date = fields.Date(
        related="link_10_id.tcwg_communication_reporting_date",
        compute_sudo=True,
        store=True,
        help=(
            "Taken from the 'External Communication' worksheet, field 'Date "
            "of TCWG Communication Reporting'."
        ),
    )
    label_internal_auditor = fields.Char(
        string="Internal Auditor",
    )
    ia_communication_planning_date = fields.Date(
        related="link_10_id.ia_communication_planning_date",
        compute_sudo=True,
        store=True,
        help=(
            "Taken from the 'External Communication' worksheet, field 'Date "
            "of IA Communication Planning'."
        ),
    )
    ia_communication_date = fields.Date(
        related="link_10_id.ia_communication_date",
        compute_sudo=True,
        store=True,
        help=(
            "Taken from the 'External Communication' worksheet, field 'Date "
            "of IA Communication'."
        ),
    )
    ia_communication_reporting_date = fields.Date(
        related="link_10_id.ia_communication_reporting_date",
        compute_sudo=True,
        store=True,
        help=(
            "Taken from the 'External Communication' worksheet, field 'Date "
            "of IA Communication Reporting'."
        ),
    )
    label_shedule_meeting_team = fields.Char()
    communication_planning_date = fields.Date(
        related="link_6_id.communication_planning_date",
        compute_sudo=True,
        store=True,
        help=(
            "Taken from the 'Team Communication - Pre-Engagement' "
            "worksheet, field 'Communication Planning Date'."
        ),
    )
    communication_date = fields.Date(
        related="link_6_id.communication_date",
        compute_sudo=True,
        store=True,
        help=(
            "Taken from the 'Team Communication - Pre-Engagement' "
            "worksheet, field 'Communication Date'."
        ),
    )
    communication_reporting_date = fields.Date(
        related="link_6_id.communication_reporting_date",
        compute_sudo=True,
        store=True,
        help=(
            "Taken from the 'Team Communication - Pre-Engagement' "
            "worksheet, field 'Communication Reporting Date'."
        ),
    )

    @api.depends(
        "link_1_ids",
        "link_1_ids.business_environment_id",
        "link_1_ids.conclusion",
    )
    def _compute_amendment_review(self):
        """Copy the amendment conclusion from RA.150.5.

        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            review = record.amendment_review
            if record.state in record._get_following_states():
                review = False
                if record.link_1_ids:
                    env_id = self.env.ref(
                        "ssi_general_audit."
                        "general_audit_business_environment_3_bd6c9b55"
                    ).id
                    it_env = record.link_1_ids.filtered(
                        lambda x: x.business_environment_id.id == env_id
                    )
                    if len(it_env) == 1:
                        review = it_env.conclusion
            record.amendment_review = review

    amendment_review = fields.Text(
        compute_sudo=True,
        compute="_compute_amendment_review",
        store=True,
        help=(
            "Taken from the 'Understanding of the Business Environment' "
            "worksheet, field 'Conclusion Additional Explanation', from "
            "the 'Amendments or Changes to Accounting Standards' "
            "environment."
        ),
    )

    @api.depends(
        "link_1_ids",
        "link_1_ids.business_environment_id",
        "link_1_ids.conclusion",
    )
    def _compute_regulatory_review(self):
        """Copy the regulatory conclusion from RA.150.5.

        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            review = record.regulatory_review
            if record.state in record._get_following_states():
                review = False
                if record.link_1_ids:
                    env_id = self.env.ref(
                        "ssi_general_audit."
                        "general_audit_business_environment_4_aaeebb37"
                    ).id
                    it_env = record.link_1_ids.filtered(
                        lambda x: x.business_environment_id.id == env_id
                    )
                    if len(it_env) == 1:
                        review = it_env.conclusion
            record.regulatory_review = review

    regulatory_review = fields.Text(
        compute_sudo=True,
        compute="_compute_regulatory_review",
        store=True,
        help=(
            "Taken from the 'Understanding of the Business Environment' "
            "worksheet, field 'Conclusion Additional Explanation', from "
            "the 'Regulatory Changes' environment."
        ),
    )

    @api.depends(
        "link_2_ids",
        "link_2_ids.detail_ids",
        "link_2_ids.detail_ids.need_unannounced_audit",
    )
    def _compute_unannounced_audit_ids(self):
        """Copy the details that need an unannounced audit from RA.150.3.

        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            result = record.unannounced_audit_ids.ids
            if record.state in record._get_following_states():
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
        help=(
            "Taken from the 'Business Cycle Summaries' worksheet, field "
            "'Details', only the lines where Need Unannounced Audit is "
            "checked."
        ),
    )

    @api.depends(
        "link_2_ids",
        "link_2_ids.assigned_team_member_ids",
    )
    def _compute_business_cycle_member_ids(self):
        """Copy the RA.150.3 worksheets that have assigned team members.

        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            result = record.assigned_team_member_ids.ids
            if record.state in record._get_following_states():
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
        help=(
            "Taken from the 'Business Cycle Summaries' worksheet, field "
            "'Assigned Team Members', only the business cycles that have "
            "assigned team members."
        ),
    )

    @api.depends(
        "link_2_ids",
        "link_2_ids.estimated_transaction_volume",
    )
    def _compute_volume_transaction_ids(self):
        """Copy the RA.150.3 worksheets that have a transaction volume.

        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            result = record.volume_transaction_ids.ids
            if record.state in record._get_following_states():
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
        help=(
            "Taken from the 'Business Cycle Summaries' worksheet, field "
            "'Estimated Transaction Volume', only the business cycles with "
            "a volume above zero."
        ),
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
            "Which balance is used as the base amount of the materiality: "
            "Extrapolation or End Period."
        ),
    )

    @api.depends(
        "materiality_balance_type",
        "link_3_ids",
        "link_3_ids.base_amount_source",
        "link_3_ids.overall_materiality",
        "link_3_ids.performance_materiality",
        "link_3_ids.tolerable_misstatement",
    )
    def _compute_materiality(self):
        """Copy the materiality amounts from the preliminary materiality.

        Follows the source while the worksheet is draft or open and
        keeps the stored values afterwards.
        """
        for record in self:
            overall = record.overall_materiality
            performance = record.performance_materiality
            tolerable = record.tolerable_misstatement
            if record.state in record._get_following_states():
                overall = performance = tolerable = 0.0
                if record.materiality_balance_type and record.link_3_ids:
                    ttype = record.materiality_balance_type
                    # More than one worksheet can share a balance type;
                    # use the first one, like the other single links do.
                    materiality = record.link_3_ids.filtered(
                        lambda x: x.base_amount_source == ttype
                    )[:1]
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
        help=(
            "Taken from the 'Materiality Computation' worksheet, field "
            "'Overall Materiality', from the worksheet whose Balance Type "
            "is the same as the Balance Type chosen in this memorandum."
        ),
    )
    performance_materiality = fields.Monetary(
        compute_sudo=True,
        compute="_compute_materiality",
        store=True,
        help=(
            "Taken from the 'Materiality Computation' worksheet, field "
            "'Performance Materiality', from the worksheet whose Balance "
            "Type is the same as the Balance Type chosen in this "
            "memorandum."
        ),
    )
    tolerable_misstatement = fields.Monetary(
        compute_sudo=True,
        compute="_compute_materiality",
        store=True,
        help=(
            "Taken from the 'Materiality Computation' worksheet, field "
            "'Tolerable Misstatement', from the worksheet whose Balance "
            "Type is the same as the Balance Type chosen in this "
            "memorandum."
        ),
    )

    @api.depends(
        "materiality_balance_type",
        "link_4_ids",
        "link_4_ids.base_amount_source",
        "link_4_ids.materiality_mapping_ids",
        "link_4_ids.materiality_mapping_ids.use_specific_materiality",
    )
    def _compute_specific_materiality_ids(self):
        """Copy the specific materiality lines from the source worksheet.

        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            result = record.specific_materiality_ids.ids
            if record.state in record._get_following_states():
                result = False
                if record.materiality_balance_type and record.link_4_ids:
                    ttype = record.materiality_balance_type
                    materiality = record.link_4_ids.filtered(
                        lambda x: x.base_amount_source == ttype
                    )
                    if materiality:
                        specific_materiality = (
                            materiality.materiality_mapping_ids.filtered(
                                lambda y: y.use_specific_materiality
                            )
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
        help=(
            "Taken from the 'Specific Materiality' worksheet, field "
            "'Materiality Mapping', only the lines where Use Specific "
            "Materiality is checked, from the worksheet whose Balance Type "
            "is the same as the Balance Type chosen in this memorandum."
        ),
    )

    inherent_finance_review = fields.Text(
        related="link_5_id.review",
        store=True,
        help=(
            "Taken from the 'Financial Statement Level Inherent Risk' "
            "worksheet, field 'Review Notes'."
        ),
    )

    @api.depends(
        "link_37_id",
        "link_37_id.conclusion",
    )
    def _compute_team_pe_review(self):
        """Copy the conclusion of the team risk assessment communication.

        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            result = record.team_pe_review
            if record.state in record._get_following_states():
                result = False
                if record.link_37_id:
                    result = record.link_37_id.conclusion
            record.team_pe_review = result

    team_pe_review = fields.Text(
        string="Review Notes",
        compute_sudo=True,
        compute="_compute_team_pe_review",
        store=True,
        help=(
            "Taken from the 'Team Communication - Risk Assessment' "
            "worksheet, field 'Conclusion Additional Explanation'."
        ),
    )

    @api.depends(
        "link_7_id",
        "link_7_id.previous_audit_information_ids",
        "link_7_id.other_provided_service_ids",
        "link_7_id.previous_audit_evidence_ids",
        "link_7_id.other_evidence_ids",
    )
    def _compute_main_business_activity(self):
        """Copy the audit information and evidence from RA.150.3.1.

        Follows the source while the worksheet is draft or open and
        keeps the stored values afterwards.
        """
        for record in self:
            previous_auditor = record.previous_auditor_ids.ids
            other_provided = record.other_provided_service_ids.ids
            previous_audit_evidence = record.previous_audit_evidence_ids.ids
            other_evidence = record.other_evidence_ids.ids
            if record.state in record._get_following_states():
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
        help=(
            "Taken from the 'Main Business Activity Processes' worksheet, "
            "field 'Previous Significant Audit Information'."
        ),
    )
    other_provided_service_ids = fields.Many2many(
        comodel_name=("general_audit_ws_ae11f7e." "other_provided_service"),
        compute_sudo=True,
        compute="_compute_main_business_activity",
        relation="rel_ga_ws_fbbe0f8_2_ae11f7e_other_provided_service",
        store=True,
        help=(
            "Taken from the 'Main Business Activity Processes' worksheet, "
            "field 'Other Provided Service'."
        ),
    )
    previous_audit_evidence_ids = fields.Many2many(
        comodel_name=("general_audit_ws_ae11f7e." "previous_audit_evidence"),
        compute_sudo=True,
        compute="_compute_main_business_activity",
        relation="rel_ga_ws_fbbe0f8_2_ae11f7e_previous_audit_evidence",
        store=True,
        help=(
            "Taken from the 'Main Business Activity Processes' worksheet, "
            "field 'Previous Audit Evidence'."
        ),
    )
    other_evidence_ids = fields.Many2many(
        comodel_name=("general_audit_ws_ae11f7e." "other_evidence"),
        compute_sudo=True,
        compute="_compute_main_business_activity",
        relation="rel_ga_ws_fbbe0f8_2_ae11f7e_other_evidence",
        store=True,
        help=(
            "Taken from the 'Main Business Activity Processes' worksheet, "
            "field 'Other Evidence'."
        ),
    )

    @api.depends(
        "link_8_id",
        "link_8_id.conclusion",
    )
    def _compute_control_entity_review(self):
        """Copy the conclusion of the entity level control risk.

        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            result = record.control_entity_review
            if record.state in record._get_following_states():
                result = False
                if record.link_8_id:
                    result = record.link_8_id.conclusion
            record.control_entity_review = result

    control_entity_review = fields.Text(
        string="Review Notes",
        compute_sudo=True,
        compute="_compute_control_entity_review",
        store=True,
        help=(
            "Taken from the 'Control Risk - Entity Level' worksheet, field "
            "'Conclusion Additional Explanation'."
        ),
    )

    @api.depends(
        "link_9_ids",
        "link_9_ids.summary_ids",
        "link_9_ids.summary_ids.select_team",
    )
    def _compute_assignment_team_ids(self):
        """Copy the selected team summaries from the source worksheets.

        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            result = record.assignment_team_ids.ids
            if record.state in record._get_following_states():
                result = False
                summaries = record.link_9_ids.mapped("summary_ids")
                if summaries:
                    summary = summaries.filtered(lambda y: y.select_team == "yes")
                    if summary:
                        result = summary.ids
            record.assignment_team_ids = result

    assignment_team_ids = fields.Many2many(
        comodel_name="general_audit_ws_b9d8a5c.summary",
        compute_sudo=True,
        compute="_compute_assignment_team_ids",
        relation="rel_ga_ws_fbbe0f8_2_b9d8a5c_summary",
        store=True,
        help=(
            "Taken from the 'Competency, Availability and Independency Of "
            "Assignment Team' worksheet, field 'Summary', only the lines "
            "where Select As Team is Yes."
        ),
    )

    @api.depends(
        "link_11_ids",
        "link_11_ids.risk",
        "link_11_ids.business_cycle_id",
    )
    def _compute_cycle_level_ids(self):
        """Copy the high risk business cycles from the source worksheets.

        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            result = record.cycle_level_ids.ids
            if record.state in record._get_following_states():
                result = False
                if record.link_11_ids:
                    cycle_level = record.link_11_ids.filtered(
                        lambda y: y.risk == "high"
                    )
                    if cycle_level:
                        result = cycle_level.business_cycle_id.ids
            record.cycle_level_ids = result

    cycle_level_ids = fields.Many2many(
        comodel_name="client_business_process",
        compute_sudo=True,
        compute="_compute_cycle_level_ids",
        relation="rel_ga_ws_fbbe0f8_2_cycle_client_business",
        store=True,
        help=(
            "Taken from the 'Control Risk - Cycle Level' worksheet, field "
            "'Business Cycle', only the lines where Risk is High."
        ),
    )

    @api.depends(
        "link_12_ids",
        "link_12_ids.risk",
        "link_12_ids.account_type_id",
    )
    def _compute_significant_acc_ids(self):
        """Copy the high risk account types from the source worksheets.

        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            result = record.significant_acc_ids.ids
            if record.state in record._get_following_states():
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
        help=(
            "Taken from the 'Significant Account Internal Control' "
            "worksheet, field 'Standard Account', only the lines where Risk "
            "is High."
        ),
    )

    allocation_total_hour_id = fields.Many2one(
        related="link_13_id.allocation_total_hour_id",
        store=True,
        help=("Taken from the 'Audit Working Plan' worksheet, field 'Total " "Hour'."),
    )
    budget_plan_status = fields.Selection(
        related="link_13_id.budget_plan_status",
        store=True,
        help=(
            "Taken from the 'Audit Working Plan' worksheet, field 'Budget "
            "Plan Status'."
        ),
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
            "All 'Understanding of the Business Environment' worksheets of "
            "this audit engagement. Filled in automatically."
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
            "All 'Business Cycle Summaries' worksheets of this audit "
            "engagement. Filled in automatically."
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
            "All 'Materiality Computation' worksheets of this audit "
            "engagement. Filled in automatically."
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
            "All 'Specific Materiality' worksheets of this audit "
            "engagement. Filled in automatically."
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
        applied to ``_compute_link_15_ids`` onward).
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
            "The 'Inherent Risk - Financial Statement Level' worksheet of "
            "this audit engagement. Filled in automatically."
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
        applied to ``_compute_link_15_ids`` onward).
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
            "The 'Team Communication Pre-Engagement' worksheet of this "
            "audit engagement. Filled in automatically."
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
        applied to ``_compute_link_15_ids`` onward).
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
            "The 'Main Business Activity Process' worksheet of this audit "
            "engagement. Filled in automatically."
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
        applied to ``_compute_link_15_ids`` onward).
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
            "The 'Control Risk - Entity Level' worksheet of this audit "
            "engagement. Filled in automatically."
        ),
    )

    # Competency, availability, and
    # independency of assignment team
    # LINK - 9 b9d8a5c (PE.110.3)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_9_ids(self):
        """Populate ``link_9_ids`` with the open/done worksheets.

        Links every worksheet of type "Competency, availability, and
        independency of assignment team" (``general_audit_ws_b9d8a5c``) that
        shares the same ``general_audit_id`` and has ``state`` in ``["open",
        "done"]``. Every match is linked: the worksheet type allows more than
        one per audit (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b9d8a5c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_9_ids = obj.search(criteria)
            if link_9_ids:
                result = link_9_ids.ids
            record.link_9_ids = result

    link_9_ids = fields.Many2many(
        string="PE.110.3",
        comodel_name="general_audit_ws_b9d8a5c",
        compute_sudo=True,
        compute="_compute_link_9_ids",
        store=True,
        help=(
            "All 'Competency, availability, and independency of assignment "
            "team' worksheets of this audit engagement. Filled in "
            "automatically."
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
        applied to ``_compute_link_15_ids`` onward).
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
            "The 'External Communication' worksheet of this audit "
            "engagement. Filled in automatically."
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
            "All 'Control Risk - Cycle Level' worksheets of this audit "
            "engagement. Filled in automatically."
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
            "All 'Significant Account' worksheets of this audit engagement. "
            "Filled in automatically."
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
        applied to ``_compute_link_15_ids`` onward).
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
            "The 'Audit Working Plan' worksheet of this audit engagement. "
            "Filled in automatically."
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
            "All 'Data Collection' worksheets of this audit engagement. "
            "Filled in automatically."
        ),
    )

    @api.depends(
        "link_14_ids",
        "link_14_ids.reporting_timetable_ids",
    )
    def _compute_reporting_timetable_ids(self):
        """Aggregate reporting timetable lines from ``link_14_ids``.

        Same aggregation pattern as ``_compute_unannounced_audit_ids``:
        gathers child records (``reporting_timetable_ids``) from every
        linked Data Collection worksheet into a single flat collection.
        Follows the source while the worksheet is draft or open and
        keeps the stored value afterwards.
        """
        for record in self:
            result = record.reporting_timetable_ids.ids
            if record.state in record._get_following_states():
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
            "Taken from the 'Data Collection' worksheet, field 'Reporting "
            "Timetable'. Cannot be edited here; edit it in the Data "
            "Collection worksheet."
        ),
    )

    # Acceptance and Continuance of Client Relationships Analysis
    # LINK - 15 806c4e1
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_15_ids(self):
        """Populate ``link_15_ids`` with the open/done worksheets.

        Links every worksheet of type "Acceptance and Continuance of Client
        Relationships Analysis" (``general_audit_ws_806c4e1``) that shares the
        same ``general_audit_id`` and has ``state`` in ``["open", "done"]``.
        Every match is linked: the worksheet type allows more than one per
        audit (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_806c4e1"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_15_ids = obj.search(criteria)
            if link_15_ids:
                result = link_15_ids.ids
            record.link_15_ids = result

    link_15_ids = fields.Many2many(
        string="Acceptance and Continuance of Client Relationships Analysis",
        comodel_name="general_audit_ws_806c4e1",
        compute_sudo=True,
        compute="_compute_link_15_ids",
        store=True,
        help=(
            "All 'Acceptance and Continuance of Client Relationships "
            "Analysis' worksheets of this audit engagement. Filled in "
            "automatically."
        ),
    )

    # Previous Financial Reporting Issues
    # LINK - 16 369c5a5
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_16_ids(self):
        """Populate ``link_16_ids`` with the open/done worksheets.

        Links every worksheet of type "Previous Financial Reporting Issues"
        (``general_audit_ws_369c5a5``) that shares the same
        ``general_audit_id`` and has ``state`` in ``["open", "done"]``. Every
        match is linked: the worksheet type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_369c5a5"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_16_ids = obj.search(criteria)
            if link_16_ids:
                result = link_16_ids.ids
            record.link_16_ids = result

    link_16_ids = fields.Many2many(
        string="Previous Financial Reporting Issues",
        comodel_name="general_audit_ws_369c5a5",
        compute_sudo=True,
        compute="_compute_link_16_ids",
        store=True,
        help=(
            "All 'Previous Financial Reporting Issues' worksheets of this "
            "audit engagement. Filled in automatically."
        ),
    )

    # Management Integrity
    # LINK - 17 f5e7049
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_17_ids(self):
        """Populate ``link_17_ids`` with the open/done worksheets.

        Links every worksheet of type "Management Integrity"
        (``general_audit_ws_f5e7049``) that shares the same
        ``general_audit_id`` and has ``state`` in ``["open", "done"]``. Every
        match is linked: the worksheet type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_f5e7049"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_17_ids = obj.search(criteria)
            if link_17_ids:
                result = link_17_ids.ids
            record.link_17_ids = result

    link_17_ids = fields.Many2many(
        string="Management Integrity",
        comodel_name="general_audit_ws_f5e7049",
        compute_sudo=True,
        compute="_compute_link_17_ids",
        store=True,
        help=(
            "All 'Management Integrity' worksheets of this audit "
            "engagement. Filled in automatically."
        ),
    )

    # Communication with Previous Auditor
    # LINK - 18 0427d28
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_18_ids(self):
        """Populate ``link_18_ids`` with the open/done worksheets.

        Links every worksheet of type "Communication with Previous Auditor"
        (``general_audit_ws_0427d28``) that shares the same
        ``general_audit_id`` and has ``state`` in ``["open", "done"]``. Every
        match is linked: the worksheet type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_0427d28"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_18_ids = obj.search(criteria)
            if link_18_ids:
                result = link_18_ids.ids
            record.link_18_ids = result

    link_18_ids = fields.Many2many(
        string="Communication with Previous Auditor",
        comodel_name="general_audit_ws_0427d28",
        compute_sudo=True,
        compute="_compute_link_18_ids",
        store=True,
        help=(
            "All 'Communication with Previous Auditor' worksheets of this "
            "audit engagement. Filled in automatically."
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
            "The 'Engagement Letter' worksheet of this audit engagement. "
            "Filled in automatically."
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
            "The 'Assignment Letter' worksheet of this audit engagement. "
            "Filled in automatically."
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
            "The 'Independence Statement' worksheet of this audit "
            "engagement. Filled in automatically."
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
            "The 'Client Assistance Package' worksheet of this audit "
            "engagement. Filled in automatically."
        ),
    )

    # Trial Balance
    # LINK - 23 a033cc6
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_23_ids(self):
        """Populate ``link_23_ids`` with the open/done worksheets.

        Links every worksheet of type "Trial Balance"
        (``general_audit_ws_a033cc6``) that shares the same
        ``general_audit_id`` and has ``state`` in ``["open", "done"]``. Every
        match is linked: the worksheet type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a033cc6"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_23_ids = obj.search(criteria)
            if link_23_ids:
                result = link_23_ids.ids
            record.link_23_ids = result

    link_23_ids = fields.Many2many(
        string="Trial Balance",
        comodel_name="general_audit_ws_a033cc6",
        compute_sudo=True,
        compute="_compute_link_23_ids",
        store=True,
        help=(
            "All 'Trial Balance' worksheets of this audit engagement. "
            "Filled in automatically."
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
            "The 'Preliminary Analytic Procedure' worksheet of this audit "
            "engagement. Filled in automatically."
        ),
    )

    # Preliminary Analytic Procedure - Vertical & Horizontal Analysis
    # LINK - 25 b32655a
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_25_ids(self):
        """Populate ``link_25_ids`` with the open/done worksheets.

        Links every worksheet of type "Preliminary Analytic Procedure -
        Vertical & Horizontal Analysis" (``general_audit_ws_b32655a``) that
        shares the same ``general_audit_id`` and has ``state`` in ``["open",
        "done"]``. Every match is linked: the worksheet type allows more than
        one per audit (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b32655a"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_25_ids = obj.search(criteria)
            if link_25_ids:
                result = link_25_ids.ids
            record.link_25_ids = result

    link_25_ids = fields.Many2many(
        string="Preliminary Analytic Procedure - Vertical & Horizontal Analysis",
        comodel_name="general_audit_ws_b32655a",
        compute_sudo=True,
        compute="_compute_link_25_ids",
        store=True,
        help=(
            "All 'Preliminary Analytic Procedure - Vertical & Horizontal "
            "Analysis' worksheets of this audit engagement. Filled in "
            "automatically."
        ),
    )

    # Preliminary Analytic Procedure - Ratio Analysis
    # LINK - 26 d4289e4
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_26_ids(self):
        """Populate ``link_26_ids`` with the open/done worksheets.

        Links every worksheet of type "Preliminary Analytic Procedure - Ratio
        Analysis" (``general_audit_ws_d4289e4``) that shares the same
        ``general_audit_id`` and has ``state`` in ``["open", "done"]``. Every
        match is linked: the worksheet type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d4289e4"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_26_ids = obj.search(criteria)
            if link_26_ids:
                result = link_26_ids.ids
            record.link_26_ids = result

    link_26_ids = fields.Many2many(
        string="Preliminary Analytic Procedure - Ratio Analysis",
        comodel_name="general_audit_ws_d4289e4",
        compute_sudo=True,
        compute="_compute_link_26_ids",
        store=True,
        help=(
            "All 'Preliminary Analytic Procedure - Ratio Analysis' "
            "worksheets of this audit engagement. Filled in automatically."
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
            "The 'General Information and Legal Aspect' worksheet of this "
            "audit engagement. Filled in automatically."
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
            "The 'Structure Organization and Responsibility' worksheet of "
            "this audit engagement. Filled in automatically."
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
            "The 'Understanding of Relevant Regulation' worksheet of this "
            "audit engagement. Filled in automatically."
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
            "The 'Going Concern Analysis' worksheet of this audit "
            "engagement. Filled in automatically."
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
            "The 'Understanding of Preparation of Financial Statement' "
            "worksheet of this audit engagement. Filled in automatically."
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
            "The 'Fraud Factor Analysis' worksheet of this audit "
            "engagement. Filled in automatically."
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
            "The 'Inherent Risk - Account Level' worksheet of this audit "
            "engagement. Filled in automatically."
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
            "The 'ROMM' worksheet of this audit engagement. Filled in " "automatically."
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
            "The 'ROMM - Financial Statement Level' worksheet of this audit "
            "engagement. Filled in automatically."
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
            "The 'ROMM - Account Level' worksheet of this audit engagement. "
            "Filled in automatically."
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
            "The 'Team Communication - Risk Assessment' worksheet of this "
            "audit engagement. Filled in automatically."
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
            "The 'Communication with Management' worksheet of this audit "
            "engagement. Filled in automatically."
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
            "The 'Communication with TCWG' worksheet of this audit "
            "engagement. Filled in automatically."
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
            "The 'Use of Internal Auditor's Work Result' worksheet of this "
            "audit engagement. Filled in automatically."
        ),
    )

    # Free-text conclusions for the Many2many links. A Many2many link
    # holds many worksheets, so no single source conclusion exists; the
    # user summarises the whole group here. Never touched by reload.
    link_1_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Understanding of the "
            "Business Environment' worksheets. Typed manually and not "
            "changed when you click Reload."
        ),
    )
    link_2_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Business Cycle Summaries' "
            "worksheets. Typed manually and not changed when you click "
            "Reload."
        ),
    )
    link_3_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Materiality Computation' "
            "worksheets. Typed manually and not changed when you click "
            "Reload."
        ),
    )
    link_4_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Specific Materiality' "
            "worksheets. Typed manually and not changed when you click "
            "Reload."
        ),
    )
    link_9_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Competency, availability, "
            "and independency of assignment team' worksheets. Typed "
            "manually and not changed when you click Reload."
        ),
    )
    link_11_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Control Risk - Cycle "
            "Level' worksheets. Typed manually and not changed when you "
            "click Reload."
        ),
    )
    link_12_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Significant Account' "
            "worksheets. Typed manually and not changed when you click "
            "Reload."
        ),
    )
    link_14_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Data Collection' "
            "worksheets. Typed manually and not changed when you click "
            "Reload."
        ),
    )
    link_15_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Acceptance and Continuance "
            "of Client Relationships Analysis' worksheets. Typed manually "
            "and not changed when you click Reload."
        ),
    )
    link_16_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Previous Financial "
            "Reporting Issues' worksheets. Typed manually and not changed "
            "when you click Reload."
        ),
    )
    link_17_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Management Integrity' "
            "worksheets. Typed manually and not changed when you click "
            "Reload."
        ),
    )
    link_18_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Communication with "
            "Previous Auditor' worksheets. Typed manually and not changed "
            "when you click Reload."
        ),
    )
    link_23_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Trial Balance' worksheets. "
            "Typed manually and not changed when you click Reload."
        ),
    )
    link_25_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Preliminary Analytic "
            "Procedure - Vertical & Horizontal Analysis' worksheets. Typed "
            "manually and not changed when you click Reload."
        ),
    )
    link_26_conclusion = fields.Text(
        string="Conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Your own overall conclusion on all 'Preliminary Analytic "
            "Procedure - Ratio Analysis' worksheets. Typed manually and not "
            "changed when you click Reload."
        ),
    )

    # Preliminary Materiality
    # LINK - 41 1d9338d
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_41_id(self):
        """Populate ``link_41_id`` from Preliminary Materiality worksheets.

        Considers only open/done worksheets.

        Searches ``general_audit_ws_1d9338d`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: the first match by default order is used instead of
        raising on multiple results (same pattern as
        ``_compute_link_13_id``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_1d9338d"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_41_id = obj.search(criteria, limit=1)
            if link_41_id:
                result = link_41_id.id
            record.link_41_id = result

    link_41_id = fields.Many2one(
        string="Preliminary Materiality",
        comodel_name="general_audit_ws_1d9338d",
        compute_sudo=True,
        compute="_compute_link_41_id",
        store=True,
        help=(
            "The 'Preliminary Materiality' worksheet of this audit "
            "engagement. Filled in automatically."
        ),
    )

    # Understanding of The Entity
    # LINK - 42 f87b2e1
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_42_id(self):
        """Populate ``link_42_id`` from Understanding of The Entity worksheets.

        Considers only open/done worksheets.

        Searches ``general_audit_ws_f87b2e1`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: the first match by default order is used instead of
        raising on multiple results (same pattern as
        ``_compute_link_13_id``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_f87b2e1"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_42_id = obj.search(criteria, limit=1)
            if link_42_id:
                result = link_42_id.id
            record.link_42_id = result

    link_42_id = fields.Many2one(
        string="Understanding of The Entity",
        comodel_name="general_audit_ws_f87b2e1",
        compute_sudo=True,
        compute="_compute_link_42_id",
        store=True,
        help=(
            "The 'Understanding of The Entity' worksheet of this audit "
            "engagement. Filled in automatically."
        ),
    )

    # Inherent Risk
    # LINK - 43 bfb6dae
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_43_id(self):
        """Populate ``link_43_id`` from Inherent Risk worksheets.

        Considers only open/done worksheets.

        Searches ``general_audit_ws_bfb6dae`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: the first match by default order is used instead of
        raising on multiple results (same pattern as
        ``_compute_link_13_id``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_bfb6dae"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_43_id = obj.search(criteria, limit=1)
            if link_43_id:
                result = link_43_id.id
            record.link_43_id = result

    link_43_id = fields.Many2one(
        string="Inherent Risk",
        comodel_name="general_audit_ws_bfb6dae",
        compute_sudo=True,
        compute="_compute_link_43_id",
        store=True,
        help=(
            "The 'Inherent Risk' worksheet of this audit engagement. Filled "
            "in automatically."
        ),
    )

    # Control Risk
    # LINK - 44 a58e29c
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_44_id(self):
        """Populate ``link_44_id`` from Control Risk worksheets.

        Considers only open/done worksheets.

        Searches ``general_audit_ws_a58e29c`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: the first match by default order is used instead of
        raising on multiple results (same pattern as
        ``_compute_link_13_id``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a58e29c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_44_id = obj.search(criteria, limit=1)
            if link_44_id:
                result = link_44_id.id
            record.link_44_id = result

    link_44_id = fields.Many2one(
        string="Control Risk",
        comodel_name="general_audit_ws_a58e29c",
        compute_sudo=True,
        compute="_compute_link_44_id",
        store=True,
        help=(
            "The 'Control Risk' worksheet of this audit engagement. Filled "
            "in automatically."
        ),
    )

    def action_reload_links(self):
        for record in self.sudo():
            record._reload_links()

    conclusion_line_ids = fields.One2many(
        string="Conclusions",
        comodel_name="general_audit_ws_fbbe0f8.conclusion",
        inverse_name="worksheet_id",
        help=(
            "Summary of the conclusion of each worksheet type. Filled in "
            "when you click Reload."
        ),
    )

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
        self._compute_link_9_ids()
        self._compute_link_10_id()
        self._compute_link_11_ids()
        self._compute_link_12_ids()
        self._compute_link_13_id()
        self._compute_link_14_ids()
        self._compute_link_15_ids()
        self._compute_link_16_ids()
        self._compute_link_17_ids()
        self._compute_link_18_ids()
        self._compute_link_19_id()
        self._compute_link_20_id()
        self._compute_link_21_id()
        self._compute_link_22_id()
        self._compute_link_23_ids()
        self._compute_link_24_id()
        self._compute_link_25_ids()
        self._compute_link_26_ids()
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
        self._compute_link_41_id()
        self._compute_link_42_id()
        self._compute_link_43_id()
        self._compute_link_44_id()
        self._reload_conclusion_lines()

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
            "link_9_ids",
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
            "link_9_ids": _(
                "Competency, availability, and " "independency of assignment team"
            ),
            "link_10_id": _("External Communication"),
            "link_11_ids": _("Control Risk - Cycle Level"),
            "link_12_ids": _("Significant Account"),
            "link_13_id": _("Audit Working Plan"),
            "link_14_ids": _("Data Collection"),
            "link_15_ids": _(
                "Acceptance and Continuance of Client " "Relationships Analysis"
            ),
            "link_16_ids": _("Previous Financial Reporting Issues"),
            "link_17_ids": _("Management Integrity"),
            "link_18_ids": _("Communication with Previous Auditor"),
            "link_19_id": _("Engagement Letter"),
            "link_20_id": _("Assignment Letter"),
            "link_21_id": _("Independence Statement"),
            "link_22_id": _("Client Assistance Package"),
            "link_23_ids": _("Trial Balance"),
            "link_24_id": _("Preliminary Analytic Procedure"),
            "link_25_ids": _(
                "Preliminary Analytic Procedure - Vertical & " "Horizontal Analysis"
            ),
            "link_26_ids": _("Preliminary Analytic Procedure - Ratio Analysis"),
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
            "link_41_id": _("Preliminary Materiality"),
            "link_42_id": _("Understanding of The Entity"),
            "link_43_id": _("Inherent Risk"),
            "link_44_id": _("Control Risk"),
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
