# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models

DEFAULT_DRAFT_OPINION = (
    "<p>Kami telah mengaudit laporan keuangan [Nama Perusahaan] "
    "(&ldquo;Perusahaan&rdquo;), yang terdiri dari laporan posisi keuangan tanggal "
    "[tanggal laporan posisi keuangan], serta laporan laba rugi dan penghasilan "
    "komprehensif lain, laporan perubahan ekuitas, dan laporan arus kas untuk tahun "
    "yang berakhir pada tanggal tersebut, serta catatan atas laporan keuangan, termasuk "
    "ikhtisar kebijakan akuntansi signifikan.</p>"
    "<p>Menurut opini kami, laporan keuangan terlampir menyajikan secara wajar, dalam "
    "semua hal yang material, posisi keuangan Perusahaan tanggal [tanggal laporan "
    "posisi keuangan], serta kinerja keuangan dan arus kasnya untuk tahun yang berakhir "
    "pada tanggal tersebut, sesuai dengan Standar Akuntansi Keuangan di Indonesia.</p>"
)

DEFAULT_DRAFT_BASIS_FOR_OPINION = (
    "<p>Kami melaksanakan audit kami berdasarkan Standar Audit yang ditetapkan oleh "
    "Institut Akuntan Publik Indonesia. Tanggung jawab kami menurut standar tersebut "
    "diuraikan lebih lanjut dalam paragraf Tanggung Jawab Auditor terhadap Audit atas "
    "Laporan Keuangan pada laporan kami. Kami independen terhadap Perusahaan "
    "berdasarkan ketentuan etika yang relevan dalam audit kami atas laporan keuangan di "
    "Indonesia, dan kami telah memenuhi tanggung jawab etika lainnya berdasarkan "
    "ketentuan tersebut. Kami yakin bahwa bukti audit yang telah kami peroleh adalah "
    "cukup dan tepat untuk menyediakan suatu basis bagi opini audit kami.</p>"
)

DEFAULT_DRAFT_RESPONSIBILITIES_OF_MANAGEMENT = (
    "<p>Manajemen bertanggung jawab atas penyusunan dan penyajian wajar laporan "
    "keuangan tersebut sesuai dengan Standar Akuntansi Keuangan di Indonesia, dan atas "
    "pengendalian internal yang dianggap perlu oleh manajemen untuk memungkinkan "
    "penyusunan laporan keuangan yang bebas dari kesalahan penyajian material, baik "
    "yang disebabkan oleh kecurangan maupun kesalahan.</p>"
    "<p>Dalam penyusunan laporan keuangan, manajemen bertanggung jawab untuk menilai "
    "kemampuan Perusahaan dalam mempertahankan kelangsungan usahanya, mengungkapkan, "
    "sesuai dengan kondisinya, hal-hal yang berkaitan dengan kelangsungan usaha, dan "
    "menggunakan basis akuntansi kelangsungan usaha, kecuali manajemen memiliki intensi "
    "untuk melikuidasi Perusahaan atau menghentikan operasi, atau tidak memiliki "
    "alternatif yang realistis selain melaksanakannya.</p>"
    "<p>Pihak yang bertanggung jawab atas tata kelola bertanggung jawab untuk mengawasi "
    "proses pelaporan keuangan Perusahaan.</p>"
)

DEFAULT_DRAFT_AUDITOR_RESPONSIBILITIES = (
    "<p>Tujuan kami adalah untuk memeroleh keyakinan memadai tentang apakah laporan "
    "keuangan secara keseluruhan bebas dari kesalahan penyajian material, baik yang "
    "disebabkan oleh kecurangan maupun kesalahan, dan untuk menerbitkan laporan auditor "
    "yang mencakup opini kami. Keyakinan memadai merupakan suatu tingkat keyakinan "
    "tinggi, namun bukan merupakan suatu jaminan bahwa audit yang dilaksanakan "
    "berdasarkan Standar Audit akan selalu mendeteksi kesalahan penyajian material "
    "ketika hal tersebut ada. Kesalahan penyajian dapat disebabkan oleh kecurangan "
    "maupun kesalahan dan dianggap material jika, baik secara individual maupun secara "
    "agregat, dapat diekspektasikan secara wajar akan memengaruhi keputusan ekonomi "
    "yang diambil oleh pengguna berdasarkan laporan keuangan tersebut.</p>"
    "<p>Sebagai bagian dari suatu audit berdasarkan Standar Audit, kami menerapkan "
    "pertimbangan profesional dan mempertahankan skeptisisme profesional selama audit. "
    "Kami juga:</p>"
    "<ul>"
    "<li>Mengidentifikasi dan menilai risiko kesalahan penyajian material dalam laporan "
    "keuangan, baik yang disebabkan oleh kecurangan maupun kesalahan, mendesain dan "
    "melaksanakan prosedur audit yang responsif terhadap risiko tersebut, serta "
    "memeroleh bukti audit yang cukup dan tepat untuk menyediakan basis bagi opini "
    "kami. Risiko tidak terdeteksinya kesalahan penyajian material yang disebabkan oleh "
    "kecurangan lebih tinggi dari yang disebabkan oleh kesalahan, karena kecurangan "
    "dapat melibatkan kolusi, pemalsuan, penghilangan secara sengaja, pernyataan salah, "
    "atau pengabaian pengendalian internal.</li>"
    "<li>Memeroleh suatu pemahaman tentang pengendalian internal yang relevan dengan "
    "audit untuk mendesain prosedur audit yang tepat sesuai dengan kondisinya, tetapi "
    "bukan untuk tujuan menyatakan opini atas keefektivitasan pengendalian internal "
    "Perusahaan.</li>"
    "<li>Mengevaluasi ketepatan kebijakan akuntansi yang digunakan serta kewajaran "
    "estimasi akuntansi dan pengungkapan terkait yang dibuat oleh manajemen.</li>"
    "<li>Menyimpulkan ketepatan penggunaan basis akuntansi kelangsungan usaha oleh "
    "manajemen dan, berdasarkan bukti audit yang diperoleh, apakah terdapat suatu "
    "ketidakpastian material yang terkait dengan peristiwa atau kondisi yang dapat "
    "menyebabkan keraguan signifikan atas kemampuan Perusahaan untuk mempertahankan "
    "kelangsungan usahanya. Ketika kami menyimpulkan bahwa terdapat suatu "
    "ketidakpastian material, kami diharuskan untuk menarik perhatian dalam laporan "
    "auditor kami ke pengungkapan terkait dalam laporan keuangan atau, jika "
    "pengungkapan tersebut tidak memadai, harus menentukan apakah perlu untuk "
    "memodifikasi opini kami. Kesimpulan kami didasarkan pada bukti audit yang "
    "diperoleh hingga tanggal laporan auditor kami. Namun, peristiwa atau kondisi masa "
    "depan dapat menyebabkan Perusahaan tidak dapat mempertahankan kelangsungan "
    "usaha.</li>"
    "<li>Mengevaluasi penyajian, struktur, dan isi laporan keuangan secara keseluruhan, "
    "termasuk pengungkapannya, dan apakah laporan keuangan mencerminkan transaksi dan "
    "peristiwa yang mendasarinya dengan suatu cara yang mencapai penyajian wajar.</li>"
    "</ul>"
    "<p>Kami mengomunikasikan kepada pihak yang bertanggung jawab atas tata kelola "
    "mengenai, antara lain, ruang lingkup dan saat yang direncanakan atas audit, serta "
    "temuan audit signifikan, termasuk setiap defisiensi signifikan dalam pengendalian "
    "internal yang teridentifikasi oleh kami selama audit.</p>"
)


class GeneralAuditWSfc75636(models.Model):
    """
    WS: Independent Auditor's Report Review Checklist (fc75636) — ISA 700 / SA 700.

    A structured Yes / No / N-A checklist for reviewing the **draft
    independent auditor's report** before it is issued, ensuring compliance
    with the applicable ISA / SA reporting standards.

    Checklist item types (``checklist_type``):

    * ``unmodified``       — Requirements for an unmodified (clean) opinion
      under ISA 700 / SA 700.
    * ``modified``         — Additional requirements when a modified opinion
      (qualified, adverse, disclaimer) is issued per ISA 705 / SA 705.
    * ``emphasis_other``   — Requirements for Emphasis of Matter and Other
      Matter paragraphs per ISA 706 / SA 706.

    Items are further grouped by ``category_id``
    (``general_audit_ws_fc75636.category``) to organise the review by
    report section or paragraph type.

    Also cross-references the Audit Final Memorandum (``a8c54f3``) KKA of
    the same engagement in a "Links" tab: ``audit_final_memorandum_id``
    (compute+store) and the related ``proposed_audit_opinion_id`` it
    mirrors. Filled in automatically whenever the engagement's sibling
    changes state, and can also be refreshed on demand with the
    ``action_reload_links`` button, following the pattern established by
    ``general_audit_ws_de69c2f``.

    Also holds a "Draft Audit Opinion" tab with nine free-text ``Html``
    fields (``draft_opinion``, ``draft_basis_for_opinion``,
    ``draft_key_audit_matters``, ``draft_other_information``,
    ``draft_responsibilities_of_management``,
    ``draft_auditor_responsibilities``, ``draft_other_legal_regulatory``,
    ``draft_emphasis_of_matter``, ``draft_other_matter``) that the auditor
    fills manually while drafting the narrative sections of the
    independent auditor's report, meant to be used as the default source
    when the final report KKA (``general_audit_ws_b66777d``) is drafted.
    """

    _name = "general_audit_ws_fc75636"
    _description = "Independen Auditor Report Review(fc75636)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_review." "worksheet_type_fc75636"
    _checklist_model_name = "general_audit_ws_fc75636.checklist"
    _item_model_name = "general_audit_ws_fc75636.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_fc75636.checklist",
        help="Checklist lines for this worksheet.",
    )

    # Draft Audit Opinion
    draft_opinion = fields.Html(
        string="Opinion",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        default=DEFAULT_DRAFT_OPINION,
        help=(
            "Draft narrative of the audit Opinion paragraph, filled "
            "manually by the auditor as a source for the final "
            "independent auditor's report."
        ),
    )
    draft_basis_for_opinion = fields.Html(
        string="Basis for Opinion",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        default=DEFAULT_DRAFT_BASIS_FOR_OPINION,
        help=(
            "Draft narrative of the Basis for Opinion paragraph, filled "
            "manually by the auditor as a source for the final "
            "independent auditor's report."
        ),
    )
    draft_key_audit_matters = fields.Html(
        string="Key Audit Matters",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help=(
            "Draft narrative of the Key Audit Matters paragraph, filled "
            "manually by the auditor as a source for the final "
            "independent auditor's report. Situational: only relevant "
            "for engagements that require a Key Audit Matters section."
        ),
    )
    draft_other_information = fields.Html(
        string="Other Information",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help=(
            "Draft narrative of the Other Information paragraph, filled "
            "manually by the auditor as a source for the final "
            "independent auditor's report. Situational: only relevant "
            "when the engagement includes other information."
        ),
    )
    draft_responsibilities_of_management = fields.Html(
        string="Responsibilities of Management",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        default=DEFAULT_DRAFT_RESPONSIBILITIES_OF_MANAGEMENT,
        help=(
            "Draft narrative of the Responsibilities of Management "
            "paragraph, filled manually by the auditor as a source for "
            "the final independent auditor's report."
        ),
    )
    draft_auditor_responsibilities = fields.Html(
        string="Auditor's Responsibilities",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        default=DEFAULT_DRAFT_AUDITOR_RESPONSIBILITIES,
        help=(
            "Draft narrative of the Auditor's Responsibilities "
            "paragraph, filled manually by the auditor as a source for "
            "the final independent auditor's report."
        ),
    )
    draft_other_legal_regulatory = fields.Html(
        string="Report on Other Legal and Regulatory Requirements",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help=(
            "Draft narrative of the Report on Other Legal and "
            "Regulatory Requirements section, filled manually by the "
            "auditor as a source for the final independent auditor's "
            "report. Situational: only relevant when such requirements "
            "apply to the engagement."
        ),
    )
    draft_emphasis_of_matter = fields.Html(
        string="Emphasis of Matter",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help=(
            "Draft narrative of the Emphasis of Matter paragraph, "
            "filled manually by the auditor as a source for the final "
            "independent auditor's report. Situational: only relevant "
            "when an emphasis of matter paragraph is needed."
        ),
    )
    draft_other_matter = fields.Html(
        string="Other Matter",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help=(
            "Draft narrative of the Other Matter paragraph, filled "
            "manually by the auditor as a source for the final "
            "independent auditor's report. Situational: only relevant "
            "when an other matter paragraph is needed."
        ),
    )

    # Audit Final Memorandum
    @api.depends(
        "general_audit_id",
    )
    def _compute_audit_final_memorandum_id(self):
        """Compute the linked Audit Final Memorandum worksheet.

        :return: None; sets ``audit_final_memorandum_id`` on every
            record in ``self``.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a8c54f3"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            audit_final_memorandum_id = obj.search(criteria)
            if audit_final_memorandum_id:
                result = audit_final_memorandum_id.id
            record.audit_final_memorandum_id = result

    audit_final_memorandum_id = fields.Many2one(
        string="Audit Final Memorandum",
        comodel_name="general_audit_ws_a8c54f3",
        compute_sudo=True,
        compute="_compute_audit_final_memorandum_id",
        store=True,
        help=(
            "Link to the Audit Final Memorandum (a8c54f3) worksheet of "
            "the same General Audit. Automatically computed and stored."
        ),
    )
    proposed_audit_opinion_id = fields.Many2one(
        string="Proposed Audit Opinion",
        related="audit_final_memorandum_id.proposed_audit_opinion_id",
        store=True,
        help=(
            "Proposed audit opinion, mirrored from the linked Audit "
            "Final Memorandum worksheet. Read-only."
        ),
    )

    def action_reload_links(self):
        """Refresh the Audit Final Memorandum reference on the Links tab.

        :return: None; calls ``_reload_links`` on every record in
            ``self``, run with ``sudo()`` so users without direct write
            access on the linked worksheet can still trigger the reload
            from the button.
        """
        for record in self.sudo():
            record._reload_links()

    def _reload_links(self):
        """Recompute the Links tab reference.

        :return: None; re-runs ``_compute_audit_final_memorandum_id`` on
            this record.
        """
        self.ensure_one()
        self._compute_audit_final_memorandum_id()
