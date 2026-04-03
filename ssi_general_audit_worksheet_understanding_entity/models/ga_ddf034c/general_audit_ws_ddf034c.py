# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSddf034c(models.Model):
    """Worksheet: General Information and Legal Aspect (ddf034c) — RA.150.1.

    Records the entity's foundational legal and general information as part of
    understanding the entity, in accordance with ISA 315 (Revised) / SA 315.

    This worksheet captures:
    - Client contact persons (names, roles, communication details)
    - Deed of Establishment (notarial deed number, date, notary details)
    - Subsequent amendments to the deed (amendment history)
    - Composition of management and shareholders (establishment and amendments)
    - Ownership of locations (head office, branches, facilities: owned/leased)
    - Licensing, registration, and legal/regulatory information

    Understanding the entity's legal structure and key persons enables the
    auditor to assess governance, identify related parties, and evaluate
    compliance with applicable regulations and reporting frameworks
    (ISA 250 / SA 250 — Consideration of Laws and Regulations).

    Inherits from ``general_audit_worksheet_mixin``.
    """

    _name = "general_audit_ws_ddf034c"
    _description = "General Information and Legal Aspec (ddf034c)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_ddf034c"
    )

    # Client Contacts
    client_contact_ids = fields.One2many(
        string="Client Contacts",
        comodel_name="general_audit_ws_ddf034c.contact",
        inverse_name="worksheet_id",
        help=(
            "List of client contact persons related to this worksheet. "
            "Maintain names, roles, and contact details for communication."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    # General Information
    # Establishment of the Company
    est_no = fields.Char(
        string="Deed of Establishment Number",
        help=(
            "Official number as stated in the Deed of Establishment. "
            "Use the exact identifier appearing on the notarial deed."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    est_date = fields.Date(
        string="Deed of Establishment Date",
        help=(
            "Date on which the Deed of Establishment was executed/issued "
            "by the notary."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    est_notary_name = fields.Char(
        string="Name of Notary (Est.)",
        help=("Full name of the notary who issued the Deed of Establishment."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    est_notary_address = fields.Text(
        string="Address of Notary (Est.)",
        help=(
            "Registered address of the notary office related to the Deed of Establishment."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    est_company_purpose = fields.Char(
        string="Purpose of The Company (Est.)",
        help=(
            "Business purpose/object of the company as stated in the Deed of Establishment."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    est_authorized_amount = fields.Float(
        string="Authorized Capital Amount (Est.)",
        default=False,
        help=(
            "Total authorized share capital amount per the Deed of Establishment. "
            "Currency follows the company configuration."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    est_authorized_number = fields.Integer(
        string="Authorized Shared Number (Est.)",
        default=False,
        help=(
            "Total number of authorized shares as specified in the Deed of Establishment."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "est_authorized_amount",
        "est_authorized_number",
    )
    def _compute_est_authorized_value(self):
        for record in self:
            record.est_authorized_value = 0.0
            if record.est_authorized_amount and record.est_authorized_number:
                record.est_authorized_value = (
                    record.est_authorized_amount * record.est_authorized_number
                )

    est_authorized_value = fields.Float(
        string="Authorized Shared Value (Est.)",
        compute_sudo=True,
        compute="_compute_est_authorized_value",
        help=(
            "Par value per authorized share as specified in the Deed of Establishment."
        ),
    )
    est_paid_amount = fields.Float(
        string="Paid Capital Amount (Est.)",
        help=("Total paid-in share capital amount at the time of establishment."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    est_paid_number = fields.Integer(
        string="Paid Shared Number (Est.)",
        help=("Number of paid-in shares at the time of establishment."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "est_paid_amount",
        "est_paid_number",
    )
    def _compute_est_paid_value(self):
        for record in self:
            record.est_paid_value = 0.0
            if record.est_paid_amount and record.est_paid_number:
                record.est_paid_value = record.est_paid_amount * record.est_paid_number

    est_paid_value = fields.Float(
        string="Paid Shared Value (Est.)",
        compute_sudo=True,
        compute="_compute_est_paid_value",
        help=("Par value per paid-in share at the time of establishment."),
    )
    est_company_address = fields.Text(
        string="Address of Company (Est.)",
        help=("Registered company address as stated in the Deed of Establishment."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    est_shareholding_ids = fields.One2many(
        string="Shareholding Structure (Est.)",
        comodel_name="general_audit_ws_ddf034c.est_shareholding",
        inverse_name="worksheet_id",
        help=(
            "Shareholding structure at the time of establishment. "
            "List shareholders, ownership percentages, and capital amounts."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    est_composition_ids = fields.One2many(
        string="Company Management Composition (Est.)",
        comodel_name="general_audit_ws_ddf034c.est_composition",
        inverse_name="worksheet_id",
        help=(
            "Management composition at establishment, such as directors and commissioners."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    # Amendment of the Company
    adm_no = fields.Char(
        string="Deed of Amendment Number",
        help=("Official number of the latest Deed of Amendment."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    adm_date = fields.Date(
        string="Deed of Amendment Date",
        help=("Issuance/execution date of the latest Deed of Amendment."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    adm_notary_name = fields.Char(
        string="Name of Notary (Adm.)",
        help=("Full name of the notary who issued the Deed of Amendment."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    adm_notary_address = fields.Text(
        string="Address of Notary (Adm.)",
        help=(
            "Registered address of the notary office related to the Deed of Amendment."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    adm_company_purpose = fields.Char(
        string="Purpose of The Company (Adm.)",
        help=(
            "Business purpose/object of the company as stated in the latest Deed of Amendment."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    adm_authorized_amount = fields.Float(
        string="Authorized Capital Amount (Adm.)",
        default=False,
        help=("Total authorized share capital amount per the Deed of Amendment."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    adm_authorized_number = fields.Integer(
        string="Authorized Shared Number (Adm.)",
        default=False,
        help=(
            "Total number of authorized shares as specified in the Deed of Amendment."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "adm_authorized_amount",
        "adm_authorized_number",
    )
    def _compute_adm_authorized_value(self):
        for record in self:
            record.adm_authorized_value = 0.0
            if record.adm_authorized_amount and record.adm_authorized_number:
                record.adm_authorized_value = (
                    record.adm_authorized_amount * record.adm_authorized_number
                )

    adm_authorized_value = fields.Float(
        string="Authorized Shared Value (Adm.)",
        compute_sudo=True,
        compute="_compute_adm_authorized_value",
        help=("Par value per authorized share as specified in the Deed of Amendment."),
    )
    adm_paid_amount = fields.Float(
        string="Paid Capital Amount (Adm.)",
        help=(
            "Total paid-in share capital amount as per the latest Deed of Amendment."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    adm_paid_number = fields.Integer(
        string="Paid Shared Number (Adm.)",
        help=("Number of paid-in shares as per the latest Deed of Amendment."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "adm_paid_amount",
        "adm_paid_number",
    )
    def _compute_adm_paid_value(self):
        for record in self:
            record.adm_paid_value = 0.0
            if record.adm_paid_amount and record.adm_paid_number:
                record.adm_paid_value = record.adm_paid_amount * record.adm_paid_number

    adm_paid_value = fields.Float(
        string="Paid Shared Value (Adm.)",
        compute_sudo=True,
        compute="_compute_adm_paid_value",
        help=("Par value per paid-in share as per the latest Deed of Amendment."),
    )
    adm_company_address = fields.Text(
        string="Address of Company (Adm.)",
        help=("Registered company address as stated in the latest Deed of Amendment."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    adm_shareholding_ids = fields.One2many(
        string="Shareholding Structure (Adm.)",
        comodel_name="general_audit_ws_ddf034c.adm_shareholding",
        inverse_name="worksheet_id",
        help=(
            "Shareholding structure according to the latest amendment. "
            "List shareholders, ownership percentages, and capital amounts."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    adm_composition_ids = fields.One2many(
        string="Company Management Composition (Adm.)",
        comodel_name="general_audit_ws_ddf034c.adm_composition",
        inverse_name="worksheet_id",
        help=("Management composition according to the latest amendment."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    # Information Regarding Other Legalities
    business_no = fields.Char(
        string="Business License Number",
        help=(
            "Identifier/number of the business license (e.g., NIB/OSS or sectoral license)."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    business_date = fields.Date(
        string="Business License Date",
        help=("Issuance date of the business license."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    business_validity = fields.Date(
        string="Business Validity Period",
        help=("Validity end date or expiry of the business license."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    registration_no = fields.Char(
        string="Registration Certificate Number",
        help=("Number of the company registration certificate (if applicable)."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    registration_date = fields.Date(
        string="Registration Certificate Date",
        help=("Issuance date of the registration certificate."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    registration_validity = fields.Date(
        string="Registration Certificate Validity Period",
        help=("Validity end date or expiry of the registration certificate."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    other_type = fields.Char(
        string="Other Permit Type",
        help=(
            "Type/category of other permit or license (e.g., sector-specific permit)."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    other_no = fields.Char(
        string="Other Permit Number",
        help=("Identifier/number of the other permit or license."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    other_date = fields.Date(
        string="Other Permit Date",
        help=("Issuance date of the other permit or license."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    other_validity = fields.Date(
        string="Other Permit Validity Period",
        help=("Validity end date or expiry of the other permit or license."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    npwp = fields.Char(
        string="Taxpayer Identification Number",
        help=(
            "Taxpayer Identification Number (NPWP) registered with the tax authority."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    npwp_name = fields.Char(
        string="Taxpayer Identification Name",
        help=("Registered name associated with the NPWP."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    npwp_address = fields.Text(
        string="Taxpayer Identification Address",
        help=("Registered tax address associated with the NPWP."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    pkp_ok = fields.Boolean(
        string="PKP ok?",
        help=(
            "Check if the company is registered as a VAT-Registered Taxable Entrepreneur (PKP)."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    pkp_no = fields.Char(
        string="PKP Number",
        help=("Registration number for PKP status (if applicable)."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    pkp_date = fields.Date(
        string="Date of PKP",
        help=("Effective date of PKP registration (VAT taxable entrepreneur)."),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    # Ownership Status
    ownership_status_ids = fields.One2many(
        string="Ownership Status",
        comodel_name="general_audit_ws_ddf034c.ownership",
        inverse_name="worksheet_id",
        help=(
            "Details of ownership status (e.g., domestic/foreign ownership and ultimate owner)."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    permanent_empolyee = fields.Integer(
        string="Number of Permanent Employees",
        help=(
            "Total number of permanent employees, as of the reporting/reference date."
        ),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
