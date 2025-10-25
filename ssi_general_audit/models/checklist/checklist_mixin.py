# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinChecklist(models.AbstractModel):
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

    @ssi_decorator.insert_on_form_view()
    def _checklist_insert_form_element(self, view_arch):
        if self._checklist_create_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_general_audit.checklist_page",
                xpath=self._checklist_page_xpath,
                position=self._checklist_position,
            )
        return view_arch

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
                        Checklist.create(
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
                        chk.unlink()
        else:
            return True
