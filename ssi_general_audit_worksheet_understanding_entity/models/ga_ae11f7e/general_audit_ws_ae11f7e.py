# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSae11f7e(models.Model):
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

    def _inverse_other_report_ids(self):
        for record in self:
            record.general_audit_id.write(
                {
                    "other_report_ids": [(6, 0, self.other_report_ids.ids)],
                }
            )
