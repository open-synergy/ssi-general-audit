# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsA3c9d2eChecklist(models.Model):
    """Analytical procedure category line (a3c9d2e).

    One line per mandatory category loaded onto the worksheet (e.g.
    "Analytical Procedures for Sales Revenue"). Holds the reference to
    the supporting working paper (``ref_document``) and the specific
    procedures performed (``procedure_ids``, added freely by the
    auditor rather than populated from a master list — each procedure
    carries its own result). Also carries the per-category conclusion
    (``conclusion``) and its supporting evidence (``attachment_ids``),
    shown on the worksheet's "Analytical Procedure Cycle Conclusion"
    tab.
    """

    _name = "general_audit_ws_a3c9d2e.checklist"
    _inherit = [
        "mixin.checklist.value",
    ]
    _description = "Analytical Procedures – Cycle (a3c9d2e) - Category Line"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_a3c9d2e",
        required=True,
        ondelete="cascade",
        help="Parent Analytical Procedures – Cycle worksheet for this category.",
    )
    item_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_ws_a3c9d2e.item",
        required=True,
        help="Analytical procedure category master this line refers to.",
    )
    ref_document = fields.Char(
        string="Ref Document",
        help="Reference to the supporting working paper for this category.",
    )
    procedure_ids = fields.One2many(
        string="Items",
        comodel_name="general_audit_ws_a3c9d2e.checklist_procedure",
        inverse_name="checklist_id",
        help=(
            "Specific analytical procedures performed for this category, "
            "added manually by the auditor (not populated from a master list)."
        ),
    )
    conclusion = fields.Char(
        string="Conclusion",
        help="Free-text conclusion for this analytical procedure category.",
    )
    attachment_ids = fields.Many2many(
        string="Attachments",
        comodel_name="ir.attachment",
        relation="rel_general_audit_ws_a3c9d2e_checklist_2_attachment",
        column1="checklist_id",
        column2="attachment_id",
        domain="[('res_model', '=', 'general_audit_ws_a3c9d2e'), "
        "('res_id', '=', worksheet_id)]",
        help=(
            "Files attached as supporting evidence for this category's "
            "conclusion. Only attachments linked to this worksheet can be "
            "selected."
        ),
    )
