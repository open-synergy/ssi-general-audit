# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSae598e6Control(models.Model):
    """Finding line in the Management Letter worksheet (ae598e6).

    References an escalated audit finding from the Audit Result Discussion
    (``influence_id`` → bc3e272.influence → a0319a2.detail) and captures the
    formal management-letter content: finding description, root cause, effect,
    and the recommended corrective action to be communicated to management.
    """

    _name = "general_audit_ws_ae598e6.influence"
    _description = "Management Letter (ae598e6) - " "Findings That Influence Opinion"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae598e6",
        required=True,
        ondelete="cascade",
        help="Parent worksheet to which this finding line belongs.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help="Sequence used to order the lines in the report.",
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help="State of the parent worksheet.",
    )
    influence_id = fields.Many2one(
        comodel_name="general_audit_ws_bc3e272.influence",
        ondelete="restrict",
        help="Reference to the finding (bc3e272) that may influence the audit opinion.",
    )
    detail_id = fields.Many2one(
        related="influence_id.detail_id",
        help="Underlying detail record of the selected finding.",
    )
    risk = fields.Selection(
        related="detail_id.risk",
        help="Risk level associated with this finding, taken from the detail.",
    )
    condition = fields.Text(
        related="detail_id.condition",
        help="Observed condition as recorded on the underlying detail.",
    )
    criteria = fields.Text(
        help="Criteria or benchmark used to evaluate the condition.",
    )
    cause = fields.Text(
        help="Root cause contributing to the condition.",
    )
    effect = fields.Text(
        help="Impact or potential consequence resulting from the condition.",
    )
    proposed_adjustment = fields.Text(
        help="Proposed journal or adjustment to address the finding, if any.",
    )
