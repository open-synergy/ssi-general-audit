# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd1ecfb7Step(models.Model):
    """
    Individual Step Line for WS-D1ECfb7 (Re-performance).

    Each record captures a single step in the procedure or control that the
    auditor independently re-executed, together with the outcome of
    re-performing that particular step.

    The lines are ordered by ``sequence`` to preserve the logical end-to-end
    order of the re-performed procedure, matching Section C of the
    RR.SS.X.05 Reperformance working-paper template
    (TAHAPAN PROSEDUR/PENGENDALIAN YANG DIUJI).
    """

    _name = "general_audit_ws_d1ecfb7.step"
    _description = "Reperformance Audit Procedure - Step (d1ecfb7)"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_d1ecfb7",
        string="Worksheet",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help="The sequence order of the step in the re-performance procedure.",
    )
    procedure_step = fields.Text(
        string="Procedure / Control Step",
        required=True,
        help="Description of the individual procedure or control step that was re-executed.",
    )
    reperformance_result = fields.Html(
        string="Re-performance Result",
        required=False,
        help="Outcome of independently re-executing this procedure or control step.",
    )
