# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSddf034c(models.Model):
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
    )
    # General Information
    # Establishment of the Company
    est_no = fields.Char(
        string="Deed of Establishment Number",
    )
    est_date = fields.Date(
        string="Deed of Establishment Date",
    )
    est_notary_name = fields.Char(
        string="Name of Notary (Est.)",
    )
    est_notary_address = fields.Text(
        string="Address of Notary (Est.)",
    )
    est_company_purpose = fields.Char(
        string="Purpose of The Company (Est.)",
    )
    est_authorized_amount = fields.Float(
        string="Authorized Capital Amount (Est.)",
        default=False,
    )
    est_authorized_number = fields.Integer(
        string="Authorized Shared Number (Est.)",
        default=False,
    )
    est_authorized_value = fields.Float(
        string="Authorized Shared Value (Est.)",
        default=False,
    )
    est_paid_amount = fields.Float(
        string="Paid Capital Amount (Est.)",
    )
    est_paid_number = fields.Integer(
        string="Paid Shared Number (Est.)",
    )
    est_paid_value = fields.Float(
        string="Paid Shared Value (Est.)",
    )
    est_company_address = fields.Text(
        string="Address of Company (Est.)",
    )
    est_shareholding_ids = fields.One2many(
        string="Shareholding Structure (Est.)",
        comodel_name="general_audit_ws_ddf034c.est_shareholding",
        inverse_name="worksheet_id",
    )
    est_composition_ids = fields.One2many(
        string="Company Management Composition (Est.)",
        comodel_name="general_audit_ws_ddf034c.est_composition",
        inverse_name="worksheet_id",
    )
    # Amendment of the Company
    adm_no = fields.Char(
        string="Deed of Amendment Number",
    )
    adm_date = fields.Date(
        string="Deed of Amendment Date",
    )
    adm_notary_name = fields.Char(
        string="Name of Notary (Adm.)",
    )
    adm_notary_address = fields.Text(
        string="Address of Notary (Adm.)",
    )
    adm_company_purpose = fields.Char(
        string="Purpose of The Company (Adm.)",
    )
    adm_authorized_amount = fields.Float(
        string="Authorized Capital Amount (Adm.)",
        default=False,
    )
    adm_authorized_number = fields.Integer(
        string="Authorized Shared Number (Adm.)",
        default=False,
    )
    adm_authorized_value = fields.Float(
        string="Authorized Shared Value (Adm.)",
        default=False,
    )
    adm_paid_amount = fields.Float(
        string="Paid Capital Amount (Adm.)",
    )
    adm_paid_number = fields.Integer(
        string="Paid Shared Number (Adm.)",
    )
    adm_paid_value = fields.Float(
        string="Paid Shared Value (Adm.)",
    )
    adm_company_address = fields.Text(
        string="Address of Company (Adm.)",
    )
    adm_shareholding_ids = fields.One2many(
        string="Shareholding Structure (Adm.)",
        comodel_name="general_audit_ws_ddf034c.adm_shareholding",
        inverse_name="worksheet_id",
    )
    adm_composition_ids = fields.One2many(
        string="Company Management Composition (Adm.)",
        comodel_name="general_audit_ws_ddf034c.adm_composition",
        inverse_name="worksheet_id",
    )
    # Information Regarding Other Legalities
    business_no = fields.Char(
        string="Business License Number",
    )
    business_date = fields.Date(
        string="Business License Date",
    )
    business_validity = fields.Date(
        string="Business Validity Period",
    )
    registration_no = fields.Char(
        string="Registration Certificate Number",
    )
    registration_date = fields.Date(
        string="Registration Certificate Date",
    )
    registration_validity = fields.Date(
        string="Registration Certificate Validity Period",
    )
    other_type = fields.Char(
        string="Other Permit Type",
    )
    other_no = fields.Char(
        string="Other Permit Number",
    )
    other_date = fields.Date(
        string="Other Permit Date",
    )
    other_validity = fields.Date(
        string="Other Permit Validity Period",
    )
    npwp = fields.Char(
        string="Taxpayer Identification Number",
    )
    npwp_name = fields.Char(
        string="Taxpayer Identification Name",
    )
    npwp_address = fields.Text(
        string="Taxpayer Identification Address",
    )
    pkp_ok = fields.Boolean(
        string="PKP ok?",
    )
    pkp_no = fields.Char(
        string="PKP Number",
    )
    pkp_date = fields.Date(
        string="Date of PKP",
    )
    # Ownership Status
    ownership_status_ids = fields.One2many(
        string="Ownership Status",
        comodel_name="general_audit_ws_ddf034c.ownership",
        inverse_name="worksheet_id",
    )
    permanent_empolyee = fields.Integer(
        string="Number of Permanent Employees",
    )
