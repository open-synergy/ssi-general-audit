# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSeABDAADDetail(models.Model):
    _name = "general_audit_ws_eabdaad.detail"
    _inherit = "general_audit_ws_eabdaad.detail"

    toc_attribute_id = fields.Many2one(
        string="ToC Attribute",
        comodel_name="general_audit_ws_e3f4a5b.attribute",
        ondelete="restrict",
        help=(
            "Test of Control attribute this control key relies on; "
            "ToC Analysis and ToC Reference are pulled from this link."
        ),
    )
    toc_analysis = fields.Selection(
        related="toc_attribute_id.conclusion",
        selection=[
            ("effective", "Effective"),
            ("not_effective", "Not Effective"),
        ],
        store=True,
        readonly=True,
        required=False,
        help="Assessment result pulled directly from the linked Test of Control attribute.",
    )
    toc_reference = fields.Char(
        related="toc_attribute_id.worksheet_id.name",
        store=True,
        readonly=True,
        help="Document reference of the linked Test of Control worksheet.",
    )
