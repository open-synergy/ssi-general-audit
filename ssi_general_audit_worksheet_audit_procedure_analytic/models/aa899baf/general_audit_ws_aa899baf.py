# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSaa899baf(models.Model):
    """Plausible Relationship Audit Procedure (WS-AA899BAF).

    Worksheet untuk mendokumentasikan **Prosedur Audit Analitis — Hubungan
    yang Masuk Akal** (*Plausible Relationship*) sebagai bagian dari fase
    **Risk Responses** audit umum, sesuai **SA 520** (Prosedur Analitis).

    Prosedur ini mengidentifikasi dan mengevaluasi hubungan yang diperkirakan
    ada di antara data keuangan dan non-keuangan, atau di antara item-item
    dalam laporan keuangan itu sendiri.  Contoh hubungan yang masuk akal:

    * Antara jumlah karyawan dengan biaya gaji.
    * Antara volume produksi dengan biaya bahan baku.
    * Antara saldo piutang dengan pendapatan penjualan.

    Auditor menetapkan ekspektasi nilai (*expected value*) berdasarkan
    hubungan tersebut, kemudian membandingkannya dengan nilai tercatat.
    Selisih yang signifikan di luar ambang yang dapat diterima (*threshold*)
    merupakan indikasi potensi salah saji yang harus ditindaklanjuti.

    **SA Reference:** SA 520 (Prosedur Analitis), SA 330 (Respons Auditor
    atas Risiko yang Dinilai)

    **Worksheet Category:** Risk Responses (RE)
    **Worksheet Type Code:** AA899BAF

    Hubungan ke Worksheet Lain
    --------------------------
    Worksheet ini mensyaratkan referensi ke **WS-E51BB1C** (Key Audit
    Procedures) yang telah berstatus *performed*, sehingga auditor hanya
    dapat memilih prosedur audit kunci yang memang sudah direncanakan dan
    dimuat dalam program audit.

    Field Utama
    -----------
    ws_e51bb1c_id : Many2one ke ``general_audit_ws_e51bb1c``
        Worksheet Key Audit Procedures yang menjadi dasar pemilihan prosedur.
    key_audit_procedure_id : Many2one ke ``general_audit_audit_procedure_category``
        Prosedur audit kunci (kategori prosedur) yang sedang direspons.
    account_type_id : Many2one ke ``client_account_type``
        Tipe akun standar yang menjadi subjek prosedur analitis ini.
    assertion_type_ids : Many2many ke ``general_audit_assersion_type``
        Asersi laporan keuangan (SA 315) yang diuji melalui prosedur ini,
        misalnya: Keberadaan, Kelengkapan, Penilaian, Penyajian.
    """

    _name = "general_audit_ws_aa899baf"
    _description = "Plausible Relationship Audit Procedure (aa899baf)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_audit_procedure_analytic."
        "worksheet_type_aa899baf"
    )

    ws_e51bb1c_id = fields.Many2one(
        comodel_name="general_audit_ws_e51bb1c",
        string="# WS-E51BB1C",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Reference to the Key Audit Procedures worksheet.",
    )
    detail_ws_e51bb1c_id = fields.Many2one(
        comodel_name="general_audit_ws_e51bb1c.detail",
        string="Detail WS-E51BB1C",
        compute="_compute_detail_ws_e51bb1c_id",
        store=True,
        help="Details from the referenced Key Audit Procedures worksheet.",
        compute_sudo=True,
    )
    allowed_key_audit_procedure_ids = fields.Many2many(
        comodel_name="general_audit_audit_procedure_category",
        string="Allowed Key Audit Procedures",
        help="Key audit procedures that can be selected based on the referenced worksheet.",
        compute="_compute_allowed_key_audit_procedure_ids",
        store=False,
        compute_sudo=True,
    )
    key_audit_procedure_id = fields.Many2one(
        comodel_name="general_audit_audit_procedure_category",
        string="Key Audit Procedure",
        help="The key audit procedure associated with the referenced worksheet.",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
    )
    allowed_account_type_ids = fields.Many2many(
        comodel_name="client_account_type",
        related="general_audit_id.account_type_ids",
        string="Allowed Account Types",
        store=False,
        help="Account types allowed for selection in this observation procedure.",
        compute_sudo=True,
    )
    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Standard Account",
        required=False,
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="The standard account type related to this observation procedure.",
    )
    allowed_assertion_type_ids = fields.Many2many(
        comodel_name="general_audit_assersion_type",
        string="Allowed Assertion Types",
        help="Assertion types that can be selected based on the key audit procedure.",
        related="detail_ws_e51bb1c_id.assertion_type_ids",
        store=False,
        compute_sudo=True,
    )
    assertion_type_ids = fields.Many2many(
        comodel_name="general_audit_assersion_type",
        relation="general_audit_ws_aa899baf_assertion_type_rel",
        column1="worksheet_id",
        column2="assertion_type_id",
        string="Assertion Types",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help="Assertion types relevant to this observation procedure.",
    )

    @api.depends(
        "ws_e51bb1c_id",
    )
    def _compute_allowed_key_audit_procedure_ids(self):
        Detail = self.env["general_audit_ws_e51bb1c.detail"]
        for record in self:
            record.allowed_key_audit_procedure_ids = False
            if record.ws_e51bb1c_id:
                criteria = [
                    ("worksheet_id", "=", record.ws_e51bb1c_id.id),
                    ("status", "=", "performed"),
                ]
                details = Detail.search(criteria)
                if details:
                    procedures = details.mapped("audit_procedure_category_id")
                    record.allowed_key_audit_procedure_ids = procedures

    @api.depends(
        "ws_e51bb1c_id",
        "key_audit_procedure_id",
    )
    def _compute_detail_ws_e51bb1c_id(self):
        Detail = self.env["general_audit_ws_e51bb1c.detail"]
        for record in self:
            record.detail_ws_e51bb1c_id = False
            if record.ws_e51bb1c_id and record.key_audit_procedure_id:
                criteria = [
                    ("worksheet_id", "=", record.ws_e51bb1c_id.id),
                    (
                        "audit_procedure_category_id",
                        "=",
                        record.key_audit_procedure_id.id,
                    ),
                ]
                detail = Detail.search(criteria, limit=1)
                if detail:
                    record.detail_ws_e51bb1c_id = detail

    @api.onchange(
        "general_audit_id",
    )
    def onchange_account_type_id(self):
        self.account_type_id = False

    @api.onchange(
        "general_audit_id",
    )
    def onchange_ws_e51bb1c_id(self):
        self.ws_e51bb1c_id = False
