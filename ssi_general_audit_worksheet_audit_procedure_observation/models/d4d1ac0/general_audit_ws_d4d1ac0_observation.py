# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd4d1ac0Question(models.Model):
    """
    Individual Observation Line for WS-D4D1AC0.

    Each record captures a single subject-level observation made during an
    Observation audit procedure session (``general_audit_ws_d4d1ac0``).

    An observation session typically covers one process or control activity, but
    it is common to record multiple distinct observations — for example, noting
    the sequence of steps followed, deviations from established procedures, or
    control gaps identified. Each line therefore carries a **subject** (which
    aspect is being observed) and the **observation** (what was actually seen).

    Lines are ordered by ``sequence`` to preserve the chronological or logical
    order in which observations were made during the session.
    """

    _name = "general_audit_ws_d4d1ac0.observation"
    _description = "Inquiry Audit Procedure - Observation (d4d1ac0)"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_d4d1ac0",
        string="Worksheet",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help="The sequence order of the question in the inquiry procedure.",
    )
    subject = fields.Text(
        string="Subject",
        required=True,
        help="The subject of the observation made during the audit procedure.",
    )
    observation = fields.Text(
        string="Observation",
        required=True,
        help="The observation made during the audit procedure.",
    )
