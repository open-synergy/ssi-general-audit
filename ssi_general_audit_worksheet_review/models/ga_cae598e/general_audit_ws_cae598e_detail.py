# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWScae598eODetail(models.Model):
    _name = "general_audit_ws_cae598e.detail"
    _description = "Audit Evidence Evaluation Detail (cae598e) - Detail"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_cae598e",
        required=True,
        ondelete="cascade",
        help="Parent worksheet to which this detail line belongs.",
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help="State of the parent worksheet.",
    )
    detail_id = fields.Many2one(
        comodel_name="general_audit_ws_bcc0d76.detail",
        ondelete="restrict",
        help=(
            "Reference to the Audit Quality (bcc0d76) detail that is being evaluated "
            "for sufficiency, completeness, and potential impacts."
        ),
    )
    parent_type_id = fields.Many2one(
        related="detail_id.parent_type_id",
        help="Type/category of the source worksheet detail.",
    )
    code_internal = fields.Char(
        related="detail_id.code_internal",
        help="Internal code of the source worksheet type.",
    )
    sequence = fields.Integer(
        related="detail_id.sequence",
        help="Ordering sequence inherited from the source worksheet type.",
    )
    review_result = fields.Selection(
        related="detail_id.review_result",
        help="Review result carried over from the Audit Quality detail.",
    )
    evidence_sufficiency = fields.Selection(
        string="Evidence Sufficiency",
        selection=[
            ("sufficient", "Sufficient"),
            ("insufficient", "Insufficient"),
        ],
        help=(
            "Whether the audit evidence obtained is sufficient to support the conclusion "
            "for the area under review."
        ),
    )
    evidence_completeness = fields.Selection(
        string="Evidence Completeness",
        selection=[
            ("complete", "Complete"),
            ("incomplete", "Incomplete"),
        ],
        help=(
            "Whether the audit evidence covers all required assertions and procedures "
            "for the area under review."
        ),
    )
    impact_misstatement = fields.Selection(
        string="Misstatement Impact",
        selection=[
            ("none", "None"),
            ("exists", "Exists"),
        ],
        help=(
            "Indicates if identified issues may result in a "
            "misstatement of the financial statements."
        ),
    )
    impact_pervasive = fields.Selection(
        string="Pervasive Impact",
        selection=[
            ("none", "None"),
            ("exists", "Exists"),
        ],
        help=(
            "Indicates if the potential impact is pervasive (widespread) "
            "across the financial statements."
        ),
    )
