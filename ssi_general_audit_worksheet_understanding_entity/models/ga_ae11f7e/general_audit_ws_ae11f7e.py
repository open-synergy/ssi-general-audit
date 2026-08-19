# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSae11f7e(models.Model):
    """Worksheet: Main Business Activity Process (ae11f7e) — RA.150.3.

    Documents the entity's main business activities, external relationships,
    and operational context as required by ISA 315 (Revised) / SA 315 and
    ISA 550 / SA 550 (Related Parties).

    This worksheet captures a comprehensive picture of the entity's business
    environment including:

    **Business Structure & Cycles**
    - Business cycles (synchronized with the General Audit record)

    **External Parties**
    - Related parties: names, relationships, impacted account types
    - Other significant investments: entity equity interests
    - Primary funding sources: lenders, facility types, outstanding balances

    **Market Context**
    - Key customers: names, sales values, percentage of total sales
    - Key suppliers: names, purchase values, percentage of total purchases
    - Competitors: names, relative market size

    **Financial Reporting Infrastructure**
    - Information systems and accounting applications used
    - Other provided services (outsourced processes)
    - Experts engaged for fair value, actuarial, legal, or technical matters

    **Evidence & Prior Audit Information**
    - Previous audit evidence and information (carry-forward from prior periods)
    - Other information from external sources relevant to the audit
    - Relevant accounting policies applied by the entity

    Understanding these elements enables the auditor to identify risks of
    material misstatement at the financial statement and assertion levels.

    Inherits from ``general_audit_worksheet_mixin``.
    """

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
        compute_sudo=True,
        inverse="_inverse_business_cycle_ids",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Business cycles applicable to the entity; synchronized with the General "
            "Audit record."
        ),
    )
    business_cycle_summary_ids = fields.Many2many(
        string="Business Cycle Summaries",
        comodel_name="general_audit_ws_a604795",
        compute="_compute_business_cycle_summary_ids",
        compute_sudo=True,
        store=False,
        help=(
            "Business Cycle Summaries (KKA RA.150.4) worksheets linked to the "
            "business cycles above, matched by General Audit and business "
            "process. Provided so downstream/client-built reports can "
            "cross-reference this worksheet with its Business Cycle "
            "Summaries."
        ),
    )
    # Other Parties and Funding
    related_party_ids = fields.One2many(
        string="Related Parties",
        comodel_name="general_audit_ws_ae11f7e.related_party",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="List of related parties relevant to the entity.",
    )
    other_investment_ids = fields.One2many(
        string="Other Investments",
        comodel_name="general_audit_ws_ae11f7e.other_investment",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="List of other significant investments.",
    )
    primary_funding_ids = fields.One2many(
        string="Primary Fundings",
        comodel_name="general_audit_ws_ae11f7e.primary_funding",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Primary funding sources supporting operations.",
    )
    # Customer, Supplier and Competitor
    customer_ids = fields.One2many(
        string="Customers",
        comodel_name="general_audit_ws_ae11f7e.customer",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Key customers and their contribution to sales.",
    )
    supplier_ids = fields.One2many(
        string="Suppliers",
        comodel_name="general_audit_ws_ae11f7e.supplier",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Key suppliers and their contribution to purchases.",
    )
    competitor_ids = fields.One2many(
        string="Competitors",
        comodel_name="general_audit_ws_ae11f7e.competitor",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Key competitors in the market.",
    )
    # Accounting Policy
    accounting_policy_ids = fields.One2many(
        string="Accounting Policy",
        comodel_name="general_audit_ws_ae11f7e.accounting_policy",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Relevant accounting policies identified for the entity.",
    )
    accounting_application_ids = fields.Many2many(
        string="Accounting Applications",
        comodel_name="accounting_application",
        relation="rel_ga_ae11f7e_2_accounting_application",
        column1="ws_ae11f7e_id",
        column2="accounting_application_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Accounting applications/systems used by the entity.",
    )
    other_report_ids = fields.Many2many(
        string="Other Reports",
        related="general_audit_id.other_report_ids",
        compute_sudo=True,
        inverse="_inverse_other_report_ids",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Other reports used for understanding the entity; synchronized with the "
            "General Audit record."
        ),
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
        help="Experts engaged and their relevance to the engagement.",
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
        help="Significant audit information from prior periods.",
    )
    previous_audit_evidence_ids = fields.One2many(
        string="Previous Audit Evidence",
        comodel_name="general_audit_ws_ae11f7e.previous_audit_evidence",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Audit evidence from prior periods that remains "
            "relevant to the current audit."
        ),
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
        help="Other significant information from prior periods.",
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
        help="Other significant information relevant to understanding the entity.",
    )
    other_provided_service_ids = fields.One2many(
        string="Other Provided Service",
        comodel_name="general_audit_ws_ae11f7e.other_provided_service",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Other provided service relevant to understanding the entity.",
    )
    other_evidence_ids = fields.One2many(
        string="Other Evidence",
        comodel_name="general_audit_ws_ae11f7e.other_evidence",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Other audit evidence relevant to understanding the entity that is not "
            "classified under specific prior period categories."
        ),
    )

    def _inverse_business_cycle_ids(self):
        for record in self:
            record.general_audit_id.write(
                {
                    "business_cycle_ids": [(6, 0, self.business_cycle_ids.ids)],
                }
            )

    @api.depends(
        "general_audit_id",
        "business_cycle_ids",
    )
    def _compute_business_cycle_summary_ids(self):
        """Cross-reference the business cycles to their KKA summaries.

        Resolve, for each business cycle listed in ``business_cycle_ids``,
        the corresponding "Business Cycle Summaries" (RA.150.4) worksheet
        belonging to the same General Audit. Provided so client-built
        reports can cross-reference this worksheet ("Main Business
        Activity Process", RA.150.3) with its Business Cycle Summaries
        without duplicating the lookup logic.

        :return: nothing; assigns ``business_cycle_summary_ids``
        """
        Worksheet = self.env["general_audit_ws_a604795"]  # pylint: disable=invalid-name
        for record in self:
            result = []
            if record.general_audit_id and record.business_cycle_ids:
                criteria = record._get_business_cycle_summary_criteria()
                result = Worksheet.search(criteria).ids
            record.business_cycle_summary_ids = [(6, 0, result)]

    def _get_business_cycle_summary_criteria(self):
        """Build the domain selecting this worksheet's KKA summaries.

        Extension point: override to narrow or widen which "Business
        Cycle Summaries" (RA.150.4) worksheets are cross-referenced.

        :return: an Odoo search domain
        """
        self.ensure_one()
        return [
            ("general_audit_id", "=", self.general_audit_id.id),
            ("business_process_id", "in", self.business_cycle_ids.ids),
        ]

    def _inverse_other_report_ids(self):
        for record in self:
            record.general_audit_id.write(
                {
                    "other_report_ids": [(6, 0, self.other_report_ids.ids)],
                }
            )
