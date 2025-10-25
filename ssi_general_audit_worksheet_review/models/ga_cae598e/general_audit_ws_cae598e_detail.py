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
    )
    state = fields.Selection(
        related="worksheet_id.state",
    )
    detail_id = fields.Many2one(
        comodel_name="general_audit_ws_bcc0d76.detail",
        ondelete="restrict",
    )
    parent_type_id = fields.Many2one(
        related="detail_id.parent_type_id",
    )
    code_internal = fields.Char(
        related="detail_id.code_internal",
    )
    sequence = fields.Integer(
        related="detail_id.sequence",
    )
    review_result = fields.Selection(
        related="detail_id.review_result",
    )
    evidence_sufficiency = fields.Selection(
        string="Evidence Sufficiency",
        selection=[
            ("sufficient", "Sufficient"),
            ("insufficient", "Insufficient"),
        ],
    )
    evidence_completeness = fields.Selection(
        string="Evidence Completeness",
        selection=[
            ("complete", "Complete"),
            ("incomplete", "Incomplete"),
        ],
    )
    impact_misstatement = fields.Selection(
        string="Misstatement Impact",
        selection=[
            ("none", "None"),
            ("exists", "Exists"),
        ],
    )
    impact_pervasive = fields.Selection(
        string="Pervasive Impact",
        selection=[
            ("none", "None"),
            ("exists", "Exists"),
        ],
    )
