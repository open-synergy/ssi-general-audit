# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval as eval  # pylint: disable=redefined-builtin


class GeneralAuditWsB66777dDetail(models.Model):
    """One row of the "Details" summary table on WS.090.2 (b66777d).

    Stores a single Property / Python Code / Value line. The 11 fixed
    rows are populated exactly once, when their parent worksheet is
    created (see ``general_audit_ws_b66777d.create()``) -- they are a
    snapshot of the linked General Audit at that moment, not a
    live-reactive summary: editing the General Audit afterwards does
    not update these rows again.

    Not exposed for manual editing: every group's
    create/write/unlink permission on this model is 0 in
    ``security/ir.model.access.csv``, so only the ``sudo()``-wrapped
    populate logic inside ``general_audit_ws_b66777d.create()`` can
    write to it.
    """

    _name = "general_audit_ws_b66777d.detail"
    _description = "Independent Auditor Report (b66777d) - Details"

    worksheet_id = fields.Many2one(
        string="Worksheet",
        comodel_name="general_audit_ws_b66777d",
        required=True,
        ondelete="cascade",
        help=("Independent Auditor's Report worksheet this Details row " "belongs to."),
    )
    property = fields.Char(
        string="Property",
        required=True,
        help=(
            "Label of this Details row (e.g. 'Revenue', "
            "'Konsolidasi'). Free text, not a selection -- the 11 "
            "rows are seeded automatically, never typed by a user."
        ),
    )
    python_code = fields.Text(
        string="Python Code",
        required=True,
        help=(
            "Python snippet evaluated once (on worksheet creation) to "
            "derive this row's Value. Must assign its result to a "
            "variable named 'result'. Available names: 'env' and "
            "'document' (this detail record itself)."
        ),
    )
    value_type = fields.Selection(
        string="Value Type",
        selection=[
            ("char", "Text"),
            ("amount", "Amount"),
        ],
        required=True,
        help=(
            "Which of Value (Text) / Value (Amount) actually holds "
            "the result of python_code for this row; set once when "
            "the row is seeded, not inferred from python_code."
        ),
    )
    value_char = fields.Char(
        string="Value (Text)",
        readonly=True,
        compute="_compute_value",
        store=True,
        compute_sudo=True,
        help="Result of python_code, filled in when value_type is 'char'.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="worksheet_id.general_audit_id.currency_id",
        compute_sudo=True,
        help=(
            "Currency of the linked General Audit, used only so "
            "Value (Amount) renders with the correct currency symbol."
        ),
    )
    value_amount = fields.Monetary(
        string="Value (Amount)",
        readonly=True,
        compute="_compute_value",
        store=True,
        compute_sudo=True,
        currency_field="currency_id",
        help="Result of python_code, filled in when value_type is 'amount'.",
    )

    def _get_localdict(self):
        """Build the ``safe_eval`` namespace for ``python_code``.

        Same shape as ``general_audit.computation._get_extrapolation_
        localdict``: only ``env`` and ``document`` (this record) are
        exposed to the snippet.

        :return: localdict for safe_eval
        :rtype: dict
        """
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    @api.depends(
        "python_code",
        "value_type",
    )
    def _compute_value(self):
        """Evaluate ``python_code`` into ``value_char``/``value_amount``.

        Depending only on ``python_code``/``value_type`` (both set
        exactly once, together, when a row is created -- see
        ``general_audit_ws_b66777d.create()``) is deliberate: it makes
        this compute fire exactly once per row, matching the "snapshot,
        not live" design in the issue's Keputusan Desain, without
        needing a separate flag to suppress recomputation.

        ``python_code`` is executed with ``safe_eval(mode="exec",
        nocopy=True)``, the same mechanism as
        ``general_audit.computation._recompute_audited``. Any
        exception during evaluation is swallowed and the row falls
        back to an empty value (``""``/``0.0``) rather than blocking
        ``create()`` -- a malformed or overly defensive snippet must
        never stop a worksheet from being created.

        :return: None
        """
        for record in self:
            result_char = ""
            result_amount = 0.0
            try:
                localdict = record._get_localdict()
                eval(
                    record.python_code,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
                if record.value_type == "amount":
                    result_amount = result
                else:
                    result_char = result
            except Exception:
                pass
            record.value_char = result_char
            record.value_amount = result_amount
