# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa0319a2Detail(models.Model):
    _name = "general_audit_ws_a0319a2.detail"
    _description = "Findings That Influence Opinion (a0319a2) - Detail"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_a0319a2",
        required=True,
        ondelete="cascade",
        help=(
            "Parent worksheet to which this detail belongs. Used to group and "
            "manage findings that influence the audit opinion."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help="Display order of this detail within the worksheet.",
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help="Current state of the parent worksheet (related).",
    )
    risk = fields.Selection(
        selection=[
            ("major", "Major"),
            ("minor", "Minor"),
        ],
        help=(
            "Risk severity classification of the finding: 'major' indicates high "
            "impact/significance; 'minor' indicates lower impact."
        ),
    )
    condition = fields.Text(
        help=(
            "Condition: what was found/observed during the audit that constitutes "
            "the issue."
        ),
    )
    criteria = fields.Text(
        help=(
            "Criteria: the requirement, policy, standard, or expectation that "
            "should have been met."
        ),
    )
    cause = fields.Text(
        help=(
            "Cause: underlying reason(s) why the condition occurred (e.g., process "
            "gap, control failure, human error)."
        ),
    )
    effect = fields.Text(
        help=(
            "Effect: the impact or potential impact resulting from the condition "
            "on the financial statements or controls."
        ),
    )
    proposed_adjustment = fields.Text(
        help=(
            "Proposed adjustment (if any): auditor's recommended journal entries "
            "or actions to address the finding."
        ),
    )
