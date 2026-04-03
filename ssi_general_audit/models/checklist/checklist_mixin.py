# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
import logging

from lxml import etree

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class MixinChecklist(models.AbstractModel):
    """
    Abstract Mixin untuk Fungsionalitas Checklist pada Worksheet.

    Mixin abstrak yang dapat diwarisi oleh model worksheet manapun untuk
    mendapatkan fungsionalitas checklist berbasis master data. Mixin ini
    secara otomatis:
    - Menyuntikkan tab "Checklist" ke dalam form view worksheet
    - Membuat baris checklist (``mixin.checklist.value``) dari master item
      saat dokumen dibuka
    - Memvalidasi bahwa semua butir checklist telah diisi sebelum dokumen
      dapat dikonfirmasi

    Digunakan oleh worksheet-worksheet yang memerlukan konfirmasi  terhadap
    serangkaian pertanyaan standar, misalnya checklist penerimaan/keberlanjutan
    klien (SQCS / ISQC 1) dan checklist prosedur audit.
    """

    _name = "mixin.checklist"
    _description = "Mixin for checklist from master items"
    _checklist_model_name = ""
    _item_model_name = ""
    _checklist_create_page = True
    _checklist_page_xpath = "//page[@name='note']"
    _checklist_position = "before"
    CHECKLIST_STATES = {
        "open": [("readonly", False), ("required", True)],
    }

    checklist_ids = fields.One2many(
        comodel_name="mixin.checklist.value",
        inverse_name="worksheet_id",
        string="Checklist",
        readonly=True,
        states=CHECKLIST_STATES,
        help="Checklist values generated from master items for this document.",
    )

    def _get_checklist_field_name(self):
        """Nama field One2many untuk checklist"""
        self.ensure_one()
        return "checklist_ids"

    def _get_checklist_extra_vals(self, item):
        """Override untuk menambahkan field tambahan ke checklist"""
        self.ensure_one()
        return {}

    def _get_checklist_item_domain(self):
        """Override untuk menambahkan domain ke checklist item"""
        self.ensure_one()
        return []

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super(MixinChecklist, self).fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu,
        )

        if view_type != "form" or not res.get("arch"):
            return res

        try:
            doc = etree.XML(res["arch"])
            notebook_nodes = doc.xpath("//notebook")
            if not notebook_nodes:
                return res

            notebook = notebook_nodes[0]
            checklist_pages = notebook.xpath("./page[@name='checklist']")

            if not checklist_pages and getattr(self, "_checklist_create_page", False):
                tmpl = self.env.ref(
                    "ssi_general_audit.checklist_page",
                    raise_if_not_found=False,
                )
                if tmpl:
                    new_page = etree.XML(tmpl._render({}))
                    notebook.insert(0, new_page)
            elif checklist_pages:
                checklist_page = checklist_pages[0]
                parent = checklist_page.getparent()
                parent.remove(checklist_page)
                parent.insert(0, checklist_page)

            res["arch"] = etree.tostring(doc, encoding="unicode")
        except Exception as e:
            _logger.warning("Failed to ensure checklist page is first: %s", e)

        return res

    # ---- Method utama ----
    def action_populate_checklist(self):
        """Generic method untuk populate checklist dari master items"""
        if self._checklist_model_name and self._item_model_name:
            Checklist = self.env[self._checklist_model_name]
            Item = self.env[self._item_model_name]

            for record in self:
                items = Item.search(record._get_checklist_item_domain())
                checklist_field = record._get_checklist_field_name()

                # mapping existing checklist by item_id
                checklist_map = {chk.item_id.id: chk for chk in record[checklist_field]}

                # 1. Tambah / update
                for item in items:
                    if item.id not in checklist_map:
                        Checklist.sudo().create(
                            {
                                "worksheet_id": record.id,
                                "item_id": item.id,
                                "sequence": item.sequence,
                                **record._get_checklist_extra_vals(item),
                            }
                        )

                # 2. Hapus yang sudah tidak ada di master
                item_ids = set(items.ids)
                for chk in record[checklist_field]:
                    if chk.item_id.id not in item_ids:
                        chk.sudo().unlink()
        else:
            return True
