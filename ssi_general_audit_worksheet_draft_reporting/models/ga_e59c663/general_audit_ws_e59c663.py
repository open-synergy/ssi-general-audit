# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSe59c663(models.Model):
    """Worksheet — Draft Financial Statements (e59c663).

    Used to review the client's draft financial statements prior to issuing
    the audit opinion.  The auditor confirms the statements are in accordance
    with the applicable financial reporting framework (IFRS, PSAK, etc.) and
    that all audit adjustments have been properly reflected.  It holds two
    checklists transcribed from the client's WR.160/WR.160.1 sheets: a
    review procedure checklist of the steps performed before confirming the
    statements (footing/cross-footing, format review, etc. --
    ``review_checklist_ids``, populated from the
    ``general_audit_ws_e59c663.review_item`` master, shown first) and a
    completeness checklist of the financial statement components that must
    be present (cover page, the four primary statements, and the Notes to
    the Financial Statements breakdown -- ``checklist_ids``, populated from
    the ``general_audit_ws_e59c663.item`` master, shown second).  Both pages
    are declared in this model's own form view (``_checklist_create_page``
    is disabled, matching every other checklist-based worksheet in this
    module) rather than relying on ``mixin.checklist``'s single
    auto-injected page, since a model can only auto-inject one.

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
    _checklist_create_page = False

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
