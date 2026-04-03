# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd33420fDetail(models.Model):
    """Detail line for WR.110.2 — individual internal control deficiency.

    Documents one control deficiency using the standard 5-C audit finding
    format: Condition, Criteria, Cause, Effect, and Recommendation.
    The ``risk`` field classifies severity (major / minor) to assist the
    auditor in fulfilling the written-communication requirements of
    ISA 265 / SA 265 (significant deficiencies to TCWG; other deficiencies
    to management).
    """

    _name = "general_audit_ws_d33420f.detail"
    _description = "Control Deficiencies (d33420f) - Detail"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_d33420f",
        required=True,
        ondelete="cascade",
        help=(
            "Parent worksheet to which this control deficiency detail belongs. "
            "Used to group and manage control deficiency records."
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
            "Risk severity classification of the control deficiency: 'major' "
            "indicates high impact/significance; 'minor' indicates lower impact."
        ),
    )
    condition = fields.Text(
        help=(
            "Condition: what was found/observed during the audit that constitutes "
            "the control issue."
        ),
    )
    criteria = fields.Text(
        help=(
            "Criteria: the requirement, policy, standard, or expectation that "
            "should have been met by the control."
        ),
    )
    cause = fields.Text(
        help=(
            "Cause: underlying reason(s) why the deficiency occurred (e.g., "
            "process gap, control failure, human error)."
        ),
    )
    effect = fields.Text(
        help=(
            "Effect: the impact or potential impact resulting from the deficiency "
            "on the financial statements or controls."
        ),
    )
    proposed_adjustment = fields.Text(
        help=(
            "Proposed adjustment (if any): auditor's recommended entries or "
            "actions to remediate the control deficiency."
        ),
    )
