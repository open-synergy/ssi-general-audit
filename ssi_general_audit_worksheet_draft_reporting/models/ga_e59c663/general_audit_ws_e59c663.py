# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
import logging

from lxml import etree

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class GeneralAuditWSe59c663(models.Model):
    """Worksheet — Draft Financial Statements (e59c663).

    Used to review the client's draft financial statements prior to issuing
    the audit opinion.  The auditor confirms the statements are in accordance
    with the applicable financial reporting framework (IFRS, PSAK, etc.) and
    that all audit adjustments have been properly reflected.  It holds two
    checklists transcribed from the client's WR.160/WR.160.1 sheets: a
    completeness checklist of the financial statement components that must
    be present (cover page, the four primary statements, and the Notes to
    the Financial Statements breakdown -- ``checklist_ids``, populated from
    the ``general_audit_ws_e59c663.item`` master), and a review procedure
    checklist of the steps performed before confirming the statements
    (footing/cross-footing, format review, etc. -- ``review_checklist_ids``,
    populated from the ``general_audit_ws_e59c663.review_item`` master).
    ``mixin.checklist`` only auto-injects one checklist tab per class, so
    the second tab is inserted manually in ``fields_view_get`` below.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 700/SA 700 (Forming an Opinion);
    ISA 450/SA 450 (Evaluation of Misstatements).
    """

    _name = "general_audit_ws_e59c663"
    _description = "Draft Financial Statements (e59c663)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_draft_reporting." "worksheet_type_e59c663"
    )
    _checklist_model_name = "general_audit_ws_e59c663.checklist"
    _item_model_name = "general_audit_ws_e59c663.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_e59c663.checklist",
        help="Checklist lines for this worksheet.",
    )
    review_checklist_ids = fields.One2many(
        string="Review Procedure Checklist",
        comodel_name="general_audit_ws_e59c663.review_checklist",
        inverse_name="worksheet_id",
        help="Review procedure checklist lines (WR.160) for this worksheet.",
    )

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        """Insert the "Review Procedure Checklist" (WR.160) page.

        ``mixin.checklist`` (see ``_checklist_create_page``) already
        injects the "Checklist" (WR.160.1) page into the notebook via
        its own ``fields_view_get`` override, but it only supports one
        auto-injected checklist/item model pair per class. This
        override runs after that injection (through ``super()``) and
        inserts a second page, for the review procedure checklist,
        right after it. This is the "manual xpath" insertion referred
        to in the class docstring above, done in Python (via
        ``lxml.etree``, mirroring ``MixinChecklist.fields_view_get``)
        because the WR.160.1 page only exists in the rendered result
        of this method -- it is not a stored view record, so a
        declarative XML ``<xpath>`` cannot target it.

        :param int view_id: id of the view or None
        :param str view_type: type of view to return
        :param bool toolbar: true to include contextual actions
        :param submenu: deprecated
        :return: composition of the requested view
        :rtype: dict
        """
        res = super().fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu,
        )

        if view_type != "form" or not res.get("arch"):
            return res

        try:
            doc = etree.XML(res["arch"])
            checklist_pages = doc.xpath("//page[@name='checklist']")
            already_present = doc.xpath("//page[@name='review_checklist']")
            if not checklist_pages or already_present:
                return res

            tmpl = self.env.ref(
                "ssi_general_audit_worksheet_draft_reporting"
                ".general_audit_ws_e59c663_review_checklist_page",
                raise_if_not_found=False,
            )
            if not tmpl:
                return res

            review_page = etree.XML(tmpl._render({}))
            checklist_pages[0].addnext(review_page)

            # ``review_checklist_ids`` (and its embedded tree/form) is
            # inserted after every other ``fields_view_get`` override in
            # the MRO has already run its own postprocessing pass (this
            # override sits outermost), so it is never picked up by any
            # of them. Re-run postprocessing here -- mirroring
            # ``ssi_decorator_mixin.fields_view_get`` -- so the new page
            # gets ``modifiers`` and its o2m sub-views end up in
            # ``result["fields"]``, exactly like the "checklist" page.
            View = self.env["ir.ui.view"]
            if view_id and res.get("base_model", self._name) != self._name:
                View = View.with_context(base_model_name=res["base_model"])
            new_arch, new_fields = View.postprocess_and_fields(doc, self._name)
            res["arch"] = new_arch
            new_fields.update(res["fields"])
            res["fields"] = new_fields
        except Exception as exc:  # noqa: BLE001
            _logger.warning("Failed to insert the review checklist page: %s", exc)

        return res

    def action_populate_review_checklist(self):
        """Populate ``review_checklist_ids`` from the review item master.

        Mirrors ``mixin.checklist.action_populate_checklist`` (add a
        line for every active ``general_audit_ws_e59c663.review_item``
        missing from the worksheet, drop lines whose item is no
        longer in the master), but is written explicitly on this
        class because ``mixin.checklist`` only supports one
        ``_checklist_model_name``/``_item_model_name`` pair per class,
        and this worksheet already uses that pair for the WR.160.1
        completeness checklist (``checklist_ids``).

        :return: True
        :rtype: bool
        """
        checklist_model = self.env["general_audit_ws_e59c663.review_checklist"]
        item_model = self.env["general_audit_ws_e59c663.review_item"]

        for record in self:
            items = item_model.search([])
            checklist_map = {
                line.item_id.id: line for line in record.review_checklist_ids
            }

            for item in items:
                if item.id not in checklist_map:
                    checklist_model.sudo().create(
                        {
                            "worksheet_id": record.id,
                            "item_id": item.id,
                            "sequence": item.sequence,
                        }
                    )

            item_ids = set(items.ids)
            for line in record.review_checklist_ids:
                if line.item_id.id not in item_ids:
                    line.sudo().unlink()

        return True
