# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, api, fields, models


class GeneralAuditWS805d4d5(models.Model):
    _name = "general_audit_ws_805d4d5"
    _description = "Know Your Customer Principles (805d4d5)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_805d4d5"
    )

    # LINK - 1 (110.2.1)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_1_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_842f0d6"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_1_ids = obj.search(criteria).ids

    allowed_link_1_ids = fields.Many2many(
        string="Allowed Link 1",
        comodel_name="general_audit_ws_842f0d6",
        compute="_compute_allowed_link_1_ids",
        store=False,
        help="""Eligible PE.110.2.1 worksheets from the same audit
that can be linked to this record.""",
    )

    link_1 = fields.Many2one(
        string="PE.110.2.1",
        comodel_name="general_audit_ws_842f0d6",
        ondelete="restrict",
        help="Selected PE.110.2.1 worksheet used to derive the risk category (PMPJ).",
    )
    link_1_pmpj = fields.Selection(
        string="Risk (110.2.1)",
        related="link_1.pmpj",
        store=True,
        help="""Risk level propagated from the linked PE.110.2.1 worksheet
(Simplified/Intermediate/Enhanced).""",
    )

    @api.depends(
        "link_1_pmpj",
    )
    def _compute_pmpj(self):
        for record in self:
            record.pmpj_simplified = False
            record.pmpj_intermediate = False
            record.pmpj_enhanced = False
            if record.link_1_pmpj == "simplified":
                record.pmpj_simplified = True
            elif record.link_1_pmpj == "intermediate":
                record.pmpj_simplified = True
                record.pmpj_intermediate = True
            else:
                record.pmpj_simplified = True
                record.pmpj_intermediate = True
                record.pmpj_enhanced = True

    pmpj_simplified = fields.Boolean(
        string="Simplified",
        compute="_compute_pmpj",
        compute_sudo=True,
        help="""Convenience flag derived from link_1_pmpj indicating
Simplified due diligence applies.""",
    )
    pmpj_intermediate = fields.Boolean(
        string="Intermediate",
        compute="_compute_pmpj",
        compute_sudo=True,
        help="""Convenience flag derived from link_1_pmpj indicating
Intermediate due diligence applies.""",
    )
    pmpj_enhanced = fields.Boolean(
        string="Enhanced",
        compute="_compute_pmpj",
        compute_sudo=True,
        help="""Convenience flag derived from link_1_pmpj indicating
Enhanced due diligence applies.""",
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_1(self):
        self.link_1 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_842f0d6"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria)
            if result:
                self.link_1 = result.id

    # PRINSIP MENGENAL PENGGUNA JASA – SEDERHANA
    # A.   Informasi dasar pengguna jasa
    entity_partner_id = fields.Many2one(
        string="Entity Name",
        comodel_name="res.partner",
        related="general_audit_id.partner_id",
        help="Client entity (res.partner) as specified in the General Audit.",
    )
    entity_type_id = fields.Many2one(
        string="Type of Entity",
        comodel_name="company_entity_type",
        ondelete="restrict",
        help="Legal form/type of the entity (e.g., PT, CV, Foundation).",
    )
    sk_number = fields.Char(
        string="Decree of Ratification",
        help="Number of the Decree of Ratification (Surat Keputusan Pengesahan).",
    )
    sk_date = fields.Date(
        string="Decree of Ratification Date",
        help="Date of the Decree of Ratification.",
    )
    bussines_license = fields.Char(
        string="Bussines License",
        help="Business license/permit identifier for the entity.",
    )
    business_license_date = fields.Date(
        string="Bussines License Date",
        help="Issue date of the business license/permit.",
    )
    npwp = fields.Char(
        string="NPWP",
        help="Tax Identification Number (NPWP) of the entity.",
    )
    legal_address = fields.Text(
        string="Legal Address",
        help="Registered/legal address of the entity as per official records.",
    )
    location_address = fields.Text(
        string="Location Address",
        help="""Operational/location address where the entity
conducts its activities.""",
    )
    phone = fields.Char(
        string="Phone",
        help="Primary contact phone number of the entity.",
    )
    fax = fields.Char(
        string="Fax",
        help="Fax number of the entity, if applicable.",
    )
    field_industry_id = fields.Many2one(
        string="Business Field #1",
        comodel_name="res.partner.industry",
        ondelete="restrict",
        help="Primary industry classification of the entity (res.partner.industry).",
    )
    deed_number = fields.Char(
        string="Deed of Establishment",
        help="Number of the Deed of Establishment.",
    )
    deed_date = fields.Date(
        string="Deed of Establishment Date",
        help="Date of the Deed of Establishment.",
    )
    # B. Informasi jasa yang diberikan
    partner_accountant_id = fields.Many2one(
        string="Partner Name",
        comodel_name="res.partner",
        related="general_audit_id.accountant_id",
        help="Engagement partner (res.partner) responsible for the audit.",
    )
    service = fields.Char(
        string="Services Provided",
        default="Audit of Historical Fincancial Statement",
        readonly="1",
        help="""Services to be provided under the engagement.
Defaults to 'Audit of Historical Financial Statement(s)'.""",
    )
    # C. Nama, jabatan dan identitas pengurus yang memiliki
    # wewenang bertindak untuk dan atas nama entitas
    management_ids = fields.One2many(
        string="Competency Analysis",
        comodel_name="general_audit_ws_805d4d5.management",
        inverse_name="worksheet_id",
        help="""List of management personnel authorized to act
for and on behalf of the entity.""",
    )

    # II. PRINSIP MENGENAL PENGGUNA JASA – MENENGAH
    # D. Informasi kekayaan entitas
    source_fund = fields.Char(
        string="Source of Funds",
        help=(
            "Main source(s) of funds of the entity "
            "(e.g., operating income, capital injections)."
        ),
    )
    field_industry_2_id = fields.Many2one(
        string="Business Field #2",
        comodel_name="res.partner.industry",
        ondelete="restrict",
        help="Secondary industry classification of the entity, if any.",
    )
    annual_income = fields.Char(
        string="Average Annual Income",
        help="Average annual income/revenue of the entity.",
    )
    trans_purpose = fields.Char(
        string="Purpose of Transaction",
        help="Purpose of transactions with the accounting/audit firm.",
    )

    # E. Informasi pemilik manfaat (Beneficial Owner)
    owner_name = fields.Char(
        string="Owner Full Name",
        help="Beneficial owner's full legal name.",
    )
    owner_alias = fields.Char(
        string="Owner Alias (if any)",
        help="Alias or other names used by the beneficial owner (if any).",
    )
    owner_identity_no = fields.Char(
        string="Owner Identity Number",
        help="Government-issued identity/document number of the beneficial owner.",
    )
    owner_identity_type = fields.Selection(
        string="Owner Type of Identity",
        selection=[
            ("ktp", "KTP"),
            ("passport", "Passport"),
            ("lainnya", "Lainnya"),
        ],
        help="Type of identity document provided by the beneficial owner.",
    )
    owner_birthday = fields.Date(
        string="Owner Date of Birth",
        help="Date of birth of the beneficial owner.",
    )
    owner_place_of_birth = fields.Char(
        string="Owner Place of Birth",
        help="Place of birth of the beneficial owner.",
    )
    owner_country_id = fields.Many2one(
        string="Owner Nationality (Country)",
        comodel_name="res.country",
        ondelete="restrict",
        help="Nationality (country) of the beneficial owner.",
    )
    owner_residential_address = fields.Text(
        string="Owner Residential Address",
        help="Residential address of the beneficial owner.",
    )
    owner_origin_address = fields.Text(
        string="Origin Address (WNA)",
        help="Address in the country of origin for foreign nationals (WNA), if applicable.",
    )
    owner_npwp = fields.Char(
        string="Owner NPWP",
        help="Tax Identification Number (NPWP) of the beneficial owner, if available.",
    )
    owner_relationship = fields.Char(
        string="Owner Relationship",
        help=(
            "Relationship of the beneficial owner to the entity "
            "(e.g., shareholder, controller)."
        ),
    )
    owner_verification = fields.Selection(
        string="Owner Identity Verification Statement",
        selection=[
            ("ada", "Ada"),
            ("tidak_ada", "Tidak Ada"),
        ],
        help="""Statement indicating whether the beneficial owner's identity
has been verified.""",
    )

    # F. Informasi kuasa entitas
    proxy_relationship = fields.Selection(
        string="Proxy Relationship",
        selection=[
            ("direktur_utama", "Direktur Utama"),
            ("direktur", "Direktur"),
            ("komisaris_utama", "Komisaris Utama"),
            ("komisaris", "Komisaris"),
            ("pemegang_saham", "Pemegang Saham"),
            ("lainnya", "Lainnya"),
        ],
        help="""Relationship of the proxy to the entity (e.g., Director,
Commissioner, Shareholder).""",
    )
    proxy_number = fields.Char(
        string="Power of Attorney Number",
        help="Power of Attorney (POA) document number authorizing the proxy.",
    )
    proxy_date = fields.Date(
        string="Power of Attorney Date",
        help="Date of the Power of Attorney document.",
    )
    proxy_signature = fields.Char(
        string="Signatory",
        help="Name of the authorized signatory on the POA document.",
    )
    proxy_name = fields.Char(
        string="Proxy Full Name",
        help="Proxy's full legal name.",
    )
    proxy_alias = fields.Char(
        string="Proxy Alias (if any)",
        help="Alias or other names used by the proxy (if any).",
    )
    proxy_identity_no = fields.Char(
        string="Proxy Identity Number",
        help="Government-issued identity/document number of the proxy.",
    )
    proxy_identity_type = fields.Selection(
        string="Proxy Type of Identity",
        selection=[
            ("ktp", "KTP"),
            ("passport", "Passport"),
            ("lainnya", "Lainnya"),
        ],
        help="Type of identity document provided by the proxy.",
    )
    proxy_birthday = fields.Date(
        string="Proxy Date of Birth",
        help="Date of birth of the proxy.",
    )
    proxy_place_of_birth = fields.Char(
        string="Proxy Place of Birth",
        help="Place of birth of the proxy.",
    )
    proxy_country_id = fields.Many2one(
        string="Proxy Nationality (Country)",
        comodel_name="res.country",
        ondelete="restrict",
        help="Nationality (country) of the proxy.",
    )
    proxy_residential_address = fields.Text(
        string="Proxy Residential Address",
        help="Residential address of the proxy.",
    )
    proxy_verification = fields.Selection(
        string="Proxy Identity Verification Statement",
        selection=[
            ("ada", "Ada"),
            ("tidak_ada", "Tidak Ada"),
        ],
        help="""Statement indicating whether the proxy's identity
has been verified.""",
    )

    # III. PRINSIP MENGENAL PENGGUNA JASA – MENDALAM
    identification_count = fields.Integer(
        string="Count of Identifications",
        help="""Number of identification documents/information obtained under
the enhanced due diligence process.""",
    )
    identification_statement = fields.Selection(
        string="Statement of Identifications",
        selection=[
            ("sudah", "Sudah"),
            ("belum", "Belum"),
        ],
        help="""Overall statement indicating whether the required identifications
have been completed.""",
    )

    @api.onchange(
        "partner_id",
    )
    def onchange_entity_type_id(self):
        self.entity_type_id = False
        if self.partner_id:
            self.entity_type_id = self.partner_id.entity_type_id

    @api.onchange(
        "partner_id",
    )
    def onchange_npwp(self):
        self.npwp = ""
        if self.partner_id:
            self.npwp = self.partner_id.vat

    @api.onchange(
        "partner_id",
    )
    def onchange_phone(self):
        self.phone = ""
        if self.partner_id:
            self.phone = self.partner_id.phone

    @api.onchange(
        "partner_id",
    )
    def onchange_legal_address(self):
        self.legal_address = ""
        if self.partner_id:
            self.legal_address = self.partner_id.contact_address

    @api.onchange(
        "partner_id",
    )
    def onchange_location_address(self):
        self.location_address = ""
        if self.partner_id:
            self.location_address = self.partner_id.contact_address

    def _get_fields_required_before_confirm(self):
        _super = super(GeneralAuditWS805d4d5, self)
        res = _super._get_fields_required_before_confirm()
        res += [
            "link_1",
        ]
        return res

    def _get_custom_field_labels(self):
        return {
            "link_1": _("Money Laundring Issues"),
        }
