# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import api, fields, models


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
    )

    link_1 = fields.Many2one(
        string="PE.110.2.1",
        comodel_name="general_audit_ws_842f0d6",
    )
    link_1_pmpj = fields.Selection(
        string="Risk (110.2.1)",
        related="link_1.pmpj",
        store=True,
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
    )
    pmpj_intermediate = fields.Boolean(
        string="Intermediate",
        compute="_compute_pmpj",
    )
    pmpj_enhanced = fields.Boolean(
        string="Enhanced",
        compute="_compute_pmpj",
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
    )
    entity_type_id = fields.Many2one(
        string="Type of Entity",
        comodel_name="company_entity_type",
    )
    sk_number = fields.Char(
        string="Decree of Ratification",
    )
    sk_date = fields.Date(string="Decree of Ratification Date")
    bussines_license = fields.Char(
        string="Bussines License",
    )
    business_license_date = fields.Date(string="Bussines License Date")
    npwp = fields.Char(
        string="NPWP",
    )
    legal_address = fields.Text(string="Legal Address")
    location_address = fields.Text(string="Location Address")
    phone = fields.Char(
        string="Phone",
    )
    fax = fields.Char(
        string="Fax",
    )
    field_industry_id = fields.Many2one(
        string="Business Field",
        comodel_name="res.partner.industry",
    )
    deed_number = fields.Char(
        string="Deed of Establishment",
    )
    deed_date = fields.Date(string="Deed of Establishment Date")
    # B. Informasi jasa yang diberikan
    partner_accountant_id = fields.Many2one(
        string="Partner Name",
        comodel_name="res.partner",
        related="general_audit_id.accountant_id",
    )
    service = fields.Char(
        string="Services Provided",
        default="Audit of Historical Fincancial Statement",
        readonly="1",
    )
    # C. Nama, jabatan dan identitas pengurus yang memiliki
    # wewenang bertindak untuk dan atas nama entitas
    management_ids = fields.One2many(
        string="Competency Analysis",
        comodel_name="general_audit_ws_805d4d5.management",
        inverse_name="worksheet_id",
    )

    # II. PRINSIP MENGENAL PENGGUNA JASA – MENENGAH
    # D. Informasi kekayaan entitas
    source_fund = fields.Char(
        string="Source of Funds",
    )
    field_industry_2_id = fields.Many2one(
        string="Business Field",
        comodel_name="res.partner.industry",
    )
    annual_income = fields.Char(
        string="Average Annual Income",
    )
    trans_purpose = fields.Char(
        string="Purpose of Transaction",
    )

    # E. Informasi pemilik manfaat (Beneficial Owner)
    owner_name = fields.Char(
        string="Full Name",
    )
    owner_alias = fields.Char(
        string="Alias (if any)",
    )
    owner_identity_no = fields.Char(
        string="Identity Number",
    )
    owner_identity_type = fields.Selection(
        string="Type of Identity",
        selection=[
            ("ktp", "KTP"),
            ("passport", "Passport"),
            ("lainnya", "Lainnya"),
        ],
    )
    owner_birthday = fields.Date(
        string="Date of Birth",
    )
    owner_place_of_birth = fields.Char(
        string="Place of Birth",
    )
    owner_country_id = fields.Many2one(
        string="Nationality (Country)",
        comodel_name="res.country",
    )
    owner_residential_address = fields.Text(string="Residential Address")
    owner_origin_address = fields.Text(string="Origin Address (WNA)")
    owner_npwp = fields.Char(
        string="NPWP",
    )
    owner_relationship = fields.Char(
        string="Relationship",
    )
    owner_verification = fields.Selection(
        string="Identity Verification Statement",
        selection=[
            ("ada", "Ada"),
            ("tidak_ada", "Tidak Ada"),
        ],
    )

    # F. Informasi kuasa entitas
    proxy_relationship = fields.Selection(
        string="Relationship",
        selection=[
            ("direktur_utama", "Direktur Utama"),
            ("direktur", "Direktur"),
            ("komisaris_utama", "Komisaris Utama"),
            ("komisaris", "Komisaris"),
            ("pemegang_saham", "Pemegang Saham"),
            ("lainnya", "Lainnya"),
        ],
    )
    proxy_number = fields.Char(
        string="Power of Attorney Number",
    )
    proxy_date = fields.Date(string="Power of Attorney Date")
    proxy_signature = fields.Char(
        string="Signatory",
    )
    proxy_name = fields.Char(
        string="Full Name",
    )
    proxy_alias = fields.Char(
        string="Alias (if any)",
    )
    proxy_identity_no = fields.Char(
        string="Identity Number",
    )
    proxy_identity_type = fields.Selection(
        string="Type of Identity",
        selection=[
            ("ktp", "KTP"),
            ("passport", "Passport"),
            ("lainnya", "Lainnya"),
        ],
    )
    proxy_birthday = fields.Date(
        string="Date of Birth",
    )
    proxy_place_of_birth = fields.Char(
        string="Place of Birth",
    )
    proxy_country_id = fields.Many2one(
        string="Nationality (Country)",
        comodel_name="res.country",
    )
    proxy_residential_address = fields.Text(string="Residential Address")
    proxy_verification = fields.Selection(
        string="Identity Verification Statement",
        selection=[
            ("ada", "Ada"),
            ("tidak_ada", "Tidak Ada"),
        ],
    )

    # III. PRINSIP MENGENAL PENGGUNA JASA – MENDALAM
    identification_count = fields.Integer(
        string="Count of Identifications",
    )
    identification_statement = fields.Selection(
        string="Statement of Identifications",
        selection=[
            ("sudah", "Sudah"),
            ("belum", "Belum"),
        ],
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
